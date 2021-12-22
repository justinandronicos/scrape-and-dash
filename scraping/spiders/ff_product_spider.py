# from __future__ import annotations
import yaml
from typing import Iterator, Union
import json
from scrapy.http import response
import logging
from scrapy.utils.log import configure_logging


# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from decimal import Decimal

from models_items.items import ProductItem, BrandItem
from utilities import ff_url_builder
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
# # Dictionary of brands with corresponding links as values
# brands_links = {}


### FOR DEBGUGGING ###
# Check whether all results have been scraped, including extra pages for some brands
# (prod_list at end should = len(brands_links) + count )
prod_list = []
count = 0  # counts total extra pages added (non first pages)
# List of brands skipped due to no results on page (either out of stock or error)
skipped_brands = []
empty_count = 0

product_list = []


class FFProductSpider(Spider):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     return cls(settings.getbool("LOG_ENABLED"))

    name = cfg["ff_ProductSpider"]["name"]
    allowed_domains = cfg["ff_ProductSpider"]["allowed_domains"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pipelines.StoreBrandsPipeline": 100,
            "pipelines.StoreProductsPipeline": 200,
            "pipelines.StorePricesPipeline": 300,
        }
    }

    logging.getLogger("scrapy").propagate = False

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename=f"{cfg['scraper_log_path']}/ff_product_log.txt",
    #     format="%(levelname)s: %(message)s",
    #     level=logging.ERROR,
    # )

    def start_requests(self) -> Iterator[Request]:
        session = get_session()
        website_name = cfg["website_names"]["ff"]
        brand_url_dict: dict = (
            session.query(BrandUrlDict).filter_by(website=website_name).first().data
        )
        brand_set: set = set()
        api_url = ff_url_builder(offset=0)
        yield Request(
            url=api_url,
            callback=self.parse,
            meta={
                "total_results": 0,
                "max_results": 500,
                "offset": 0,
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
        global product_list

        total_results = response.meta.get("total_results")
        current_offset = response.meta.get("offset")
        max_results = response.meta.get("max_results")
        site_url = response.url[: response.url.rfind("data")]
        brand_url_dict = response.meta.get("brand_url_dict")
        brand_set = response.meta.get("brand_set")

        print(f"procesing: {response.url}")
        text_data = response.body.decode("utf8")
        json_string = text_data
        json_data = json.loads(json_string)

        # Set total_results for first api call
        if total_results == 0:
            total_results = json_data["results_total"]

        # # Check if no products listed for brand
        # if len(json_data["products"]) == 0:
        #     empty_count += 1
        #     skipped_brands.append(response)
        #     print("\n\n\n\n ERROR FROM RESPONSE \n \n \n" + str(response))
        #     return

        prod_list.append(json_data)
        results_list = json_data["products"]

        for product_result in results_list:
            try:
                # brand is single key dictionary with brand_key: Brand
                brand = list(product_result["brand"].values())[0]
                id = product_result["id"]
                product_name = product_result["name"]
                in_stock = product_result["is_in_stock"]
                product_url = site_url + product_result["url_key"]
                retail_price = Decimal(
                    product_result["min_regular_price"]["display"].replace("$", "")
                )
                current_price = Decimal(
                    product_result["min_special_price"]["display"].replace("$", "")
                )
                # Check if sale price
                if float(current_price) < float(retail_price):
                    on_sale = True
                else:
                    on_sale = False
            except KeyError:
                empty_count += 1
                print(product_result)

            variant_label = ""

            # Check if brand has been added to brand_table
            if brand not in brand_set:
                brand_set.add(brand)
                brand_item = BrandItem()
                brand_item["name"] = brand
                try:
                    brand_item["url"] = brand_url_dict[brand]
                except KeyError:
                    brand_item["url"] = None

                yield brand_item

            product = ProductItem()

            product["code"] = id
            product["brand"] = brand
            product["product_name"] = product_name
            product["variant"] = variant_label
            product["retail_price"] = retail_price
            product["on_sale"] = on_sale
            product["current_price"] = current_price
            product["in_stock"] = in_stock
            product["product_url"] = product_url

            product_list.append(product)

            # products_prices[id] = product

            yield product

        # If more results left, crawl the next batch of 500 results
        results_left = total_results - (current_offset + len(results_list))
        if results_left > 0:
            count += 1  # Check all extra pages have been scraped
            new_offset = current_offset + max_results
            next_url = ff_url_builder(offset=new_offset)
            print("Found url: {}".format(next_url))  # Write a debug statement
            yield Request(
                url=next_url,
                callback=self.parse,
                meta={
                    "total_results": total_results,
                    "max_results": max_results,
                    "offset": new_offset,
                    "brand_url_dict": brand_url_dict,
                    "brand_set": brand_set,
                },
            )  # Return a call to the function "parse"


# from scrapy.crawler import CrawlerProcess

# process = CrawlerProcess()
# # Run spiders sequentially
# process.crawl(FFProductSpider)
# process.start()  # the script will block here until all crawling jobs are finished
print(f"\n Num products= {len(product_list)}\n")

# # Run spiders sequentially
# @defer.inlineCallbacks
# def crawl():
#     yield runner.crawl(FFBrandSpider)
#     yield runner.crawl(FFProductSpider)
#     reactor.stop()

# crawl()
# reactor.run()  # the script will block here until the last crawl call is finished

print("\nExtra Pages = " + str(count))
# if len(brands_links) + count == len(prod_list):
#     print("Successfully scraped all pages")
print("Prod Length = " + str(len(product_list)))
# print("Num Brands = " + str(len(brands_links)))
# print(brands_links)
# print("\n" + str(empty_count) + " Empty Brands =", skipped_brands)

# print("\n\n")
# print("Total results: ")
# print(sum(len(v) for v in products_prices.values()))

# print(products_prices.keys())

print(" \n \n Empty Count = " + str(empty_count))


# for brand in skipped_brands:
#     print(brand)
