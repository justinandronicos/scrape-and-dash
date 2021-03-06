# from __future__ import annotations
import yaml
from typing import Iterator, Union
import json
from scrapy.http import response
import string
import logging
from scrapy.utils.log import configure_logging

# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from decimal import Decimal

from models_items.items import ProductItem, BrandItem
from utilities import nl_url_builder
from models_items.models import get_session, BrandUrlDict

# load config file
cfg = yaml.safe_load(open("config.yaml"))

# ## Dict of of processed WM brands for easier matching (lowercase & remove commas/white space)
# #  with values of actual matching WM brands
# wm_brands = {}
# # Current site brand name: WM equivalent brand name
# matched_wm_brands = {}
# Nested dictionary of form {id: {brand, product_name, variant, retail_price, on_sale, current_price, in_stock, product_url}}
# Access product prices with products_prices[product_id]
# products_prices = {}


### FOR DEBGUGGING ###
# Check whether all results have been scraped, including extra pages for some brands
# (prod_list at end should = len(brands_links) + count )
prod_list = []
count = 0  # counts total extra pages added (non first pages)
# List of brands skipped due to no results on page (either out of stock or error)
skipped_brands = []
empty_count = 0
extra_variant_count = 0
prod_count = 0

product_list = []


class NLProductSpider(Spider):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     return cls(settings.getbool("LOG_ENABLED"))

    name = cfg["nl_ProductSpider"]["name"]
    allowed_domains = cfg["nl_ProductSpider"]["allowed_domains"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pipelines.StoreBrandsPipeline": 100,
            "pipelines.StoreProductsPipeline": 200,
            "pipelines.StorePricesPipeline": 300,
        }
    }

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename=f"{cfg['scraper_log_path']}/nl_product_log.txt",
    #     format="%(levelname)s: %(message)s",
    #     level=logging.ERROR,
    # )
    configure_logging(install_root_handler=False)
    logging.getLogger("scrapy").propagate = False

    def start_requests(self) -> Iterator[Request]:
        session = get_session()
        website_name = cfg["website_names"]["nl"]
        brand_url_dict: dict = (
            session.query(BrandUrlDict).filter_by(website=website_name).first().data
        )
        brand_set: set = set()
        api_url = nl_url_builder(page_number=1)
        yield Request(
            url=api_url,
            callback=self.parse,
            meta={
                "total_results": 0,
                "max_results": 500,
                "page_number": 1,
                "brand_url_dict": brand_url_dict,
                "brand_set": brand_set,
            },
        )

    def parse(
        self, response: response
    ) -> Union[Iterator[BrandItem], Iterator[ProductItem], Iterator[Request]]:
        global count
        global empty_count
        global skipped_brands
        global extra_variant_count
        global product_list
        # global prod_count

        total_results = response.meta.get("total_results")
        current_page = response.meta.get("page_number")
        max_results = response.meta.get("max_results")
        brand_url_dict = response.meta.get("brand_url_dict")
        brand_set = response.meta.get("brand_set")

        print(f"procesing: {response.url}")

        text_data = response.body.decode("utf8")
        json_string = text_data[text_data.index("{") :]
        json_data = json.loads(json_string)

        # # Check if no products listed for brand
        # if len(json_data["results"]) == 0:
        #     empty_count += 1
        #     skipped_brands.append(response)
        #     print("\n\n\n\n ERROR FROM RESPONSE \n \n \n" + str(response))
        #     return

        prod_list.append(json_data)
        results_list = json_data["results"]

        # prod_count += len(results_list)

        for product_result in results_list:
            uid = product_result["uid"]
            brand = product_result["brand"]
            product_name = product_result["name"].replace("&amp;", "&")
            product_url = product_result["url"]
            variant_list = json.loads(
                product_result["matrix_options"].replace("&quot;", '"')
            )

            variant_count = 1

            # Check if brand has been added to brand_table
            if brand not in brand_set:
                brand_set.add(brand)
                brand_url = brand_url_dict.get(brand)
                brand_item = BrandItem(name=brand, url=brand_url)

                yield brand_item

            # letters = list(string.ascii_uppercase)
            for product_variant in variant_list:
                extra_variant_count = len(variant_list) - 1
                try:
                    id = uid + "/" + str(variant_count)
                    variant_label = product_variant["label"]
                    retail_price = Decimal(product_variant["retail_price"])
                    current_price = Decimal(product_variant["price"])
                    in_stock = int(product_variant["inventory"]) > 0

                    # Check if sale price
                    if float(current_price) < float(retail_price):
                        # if Decimal.compare(current_price, retail_price) == -1:
                        on_sale = True
                    else:
                        on_sale = False
                except KeyError:
                    empty_count += 1
                    print(product_result)

                variant_count += 1

                prod_name = brand + " " + product_name + " - " + variant_label

                product = ProductItem(
                    code=id,
                    brand=brand,
                    product_name=prod_name,
                    variant=variant_label,
                    retail_price=retail_price,
                    on_sale=on_sale,
                    current_price=current_price,
                    in_stock=in_stock,
                    product_url=product_url,
                )

                # product["code"] = id
                # product["brand"] = brand
                # product["product_name"] = (
                #     brand + " " + product_name + " - " + variant_label
                # )
                # product["variant"] = variant_label
                # product["retail_price"] = retail_price
                # product["on_sale"] = on_sale
                # product["current_price"] = current_price
                # product["in_stock"] = in_stock
                # product["product_url"] = product_url

                product_list.append(product)

                # products_prices[id] = product

                yield product

        # If more results left, crawl the next batch of 500 results
        # previous_page = json_data["pagination"]["previousPage"]
        # results_left = total_results - ((previous_page * 500) + len(results_list))
        # if results_left > 0:
        total_pages = json_data["pagination"]["totalPages"]
        total_results = json_data["pagination"]["totalResults"]
        pages_left = total_pages - current_page
        if pages_left > 0:
            count += 1  # Check all extra pages have been scraped
            new_page = current_page + 1
            next_url = nl_url_builder(page_number=new_page)
            print("Found url: {}".format(next_url))  # Write a debug statement
            yield Request(
                url=next_url,
                callback=self.parse,
                meta={
                    "total_results": total_results,
                    "max_results": max_results,
                    "page_number": new_page,
                    "brand_url_dict": brand_url_dict,
                    "brand_set": brand_set,
                },
            )

        # Return a call to the function "parse"
        # total_pages = json_data["pagination"]["totalPages"]
        # current_page = json_data["pagination"]["currentPage"]

        # # If more then 1 page, crawl the rest
        # if current_page < total_pages:
        #     count += 1  # Check all extra pages have been scraped
        #     link = brands_links.get(brand)
        #     current_page += 1
        #     # callback_num = current_page - 1

        #     next_page = nl_url_builder(current_page, brand, link)
        #     print("Found url: {}".format(next_page))  # Write a debug statement
        #     yield scrapy.Request(
        #         next_page, callback=self.parse
        #     )  # Return a call to the function "parse"


# from scrapy.crawler import CrawlerProcess

# process = CrawlerProcess()
# # Run spiders sequentially
# process.crawl(NLProductSpider)
# process.start()  # the script will block here until all crawling jobs are finished
print(f"\n Num products= {len(product_list)}\n")


# crawl()
# reactor.run()  # the script will block here until the last crawl call is finished

print("\nExtra Pages = " + str(count))
# if len(brands_links) + count == len(prod_list):
#     print("Successfully scraped all pages")
# print("Prod Length = " + str(len(products_prices)))
# print("Num Brands = " + str(len(brands_links)))
# print(brands_links)
# print("\n" + str(empty_count) + " Empty Brands =", skipped_brands)

# print("\n\n")
# print("Total results: ")
# print(sum(len(v) for v in products_prices.values()))
# print(products_prices.keys())

print(" \n \n Empty Count = " + str(empty_count))

# new = product_matcher(products_prices, matched_wm_brands)
