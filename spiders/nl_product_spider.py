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
from utilities import prod_url_builder
from items import ProductItem

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
            "pipelines.StoreProductsPipeline": 100,
            "pipelines.StorePricesPipeline": 200,
        }
    }

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename="logs/nl_product_log.txt",
    #     format="%(levelname)s: %(message)s",
    #     level=logging.ERROR,
    # )

    logging.getLogger("scrapy").propagate = False

    def start_requests(self) -> Iterator[Request]:
        api_url = prod_url_builder(website="nl", page_number=1)
        yield Request(
            url=api_url,
            callback=self.parse,
            meta={"total_results": 0, "max_results": 500, "page_number": 1},
        )

    def parse(
        self, response: response
    ) -> Union[Iterator[ProductItem], Iterator[Request]]:
        global count
        global empty_count
        global skipped_brands
        global extra_variant_count
        global product_list

        total_results = response.meta.get("total_results")
        current_page = response.meta.get("page_number")
        max_results = response.meta.get("max_results")

        print("procesing:" + response.url)

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

        for product_result in json_data["results"]:
            uid = product_result["uid"]
            brand = product_result["brand"]
            product_name = product_result["name"].replace("&amp;", "&")
            product_url = product_result["url"]
            variant_list = json.loads(
                product_result["matrix_options"].replace("&quot;", '"')
            )

            variant_count = 1

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

                # loader = ItemLoader(item=ProductItem(), response=response)
                # loader.add_value("id", id)
                # loader.add_value("brand", brand)
                # loader.add_value(
                #     "product_name", brand + " " + product_name + " - " + variant_label
                # )
                # loader.add_value("variant", variant_label)
                # loader.add_value("retail_price", retail_price)
                # loader.add_value("on_sale", on_sale)
                # loader.add_value("current_price", current_price)
                # loader.add_value("in_stock", in_stock)
                # loader.add_value("product_url", product_url)
                # product = loader.load_item()
                # products_prices[id] = product

                product = ProductItem()

                product["code"] = id
                product["brand"] = brand
                product["product_name"] = (
                    brand + " " + product_name + " - " + variant_label
                )
                product["variant"] = variant_label
                product["retail_price"] = retail_price
                product["on_sale"] = on_sale
                product["current_price"] = current_price
                product["in_stock"] = in_stock
                product["product_url"] = product_url

                product_list.append(product)

                yield product

            # products_prices[id] = {
            #     "brand": brand,
            #     "product_name": brand + " " + product_name + " - " + label_size,
            #     "size": label_size,
            #     "retail_price": retail_price,
            #     "on_sale": on_sale,
            #     "current_price": current_price,
            #     "in_stock": in_stock,
            #     "product_url": product_url,
            # }

            # if brand not in products_prices.keys():
            #     products_prices[brand] = {
            #         id: {
            #             "product_name": brand
            #             + " "
            #             + product_name
            #             + " - "
            #             + label_size,
            #             "retail_price": retail_price,
            #             "on_sale": on_sale,
            #             "current_price": current_price,
            #             "in_stock": in_stock,
            #             "product_url": product_url,
            #         }
            #     }
            # else:
            #     products_prices[brand][id] = {
            #         "product_name": brand + " " + product_name + " - " + label_size,
            #         "retail_price": retail_price,
            #         "on_sale": on_sale,
            #         "current_price": current_price,
            #         "in_stock": in_stock,
            #         "product_url": product_url,
            #     }

            #     brand = product_result["brand"]
            #     id = product_result["uid"]
            #     product_name = product_result["name"]
            #     retail_price = Decimal(product_result["retail_price"])
            #     product_url = product_result["url"]
            #     in_stock = int(product_result["inventory_count"]) > 0
            #     # Check for ss_on_sale entry
            #     if product_result["ss_sale"] == "1":
            #         on_sale = True
            #     elif product_result["ss_sale"] == "0":
            #         on_sale = False
            # except KeyError:
            #     empty_count += 1
            #     print(product_result)
            # current_price = Decimal(product_result["price"])

        # If more results left, crawl the next batch of 500 results
        total_pages = json_data["pagination"]["totalPages"]
        pages_left = total_pages - current_page
        if pages_left > 0:
            count += 1  # Check all extra pages have been scraped
            new_page = current_page + 1
            next_url = prod_url_builder(website="nl", page_number=new_page)
            print("Found url: {}".format(next_url))  # Write a debug statement
            yield Request(
                url=next_url,
                callback=self.parse,
                meta={
                    "total_results": total_results,
                    "max_results": max_results,
                    "page_number": new_page,
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
