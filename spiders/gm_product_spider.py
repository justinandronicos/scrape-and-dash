# from __future__ import annotations
import yaml
from typing import Iterator, Union
import json
from scrapy.http import response
import logging
from scrapy.utils.log import configure_logging
from sqlalchemy.orm import sessionmaker
from models import BrandUrlDict


# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
from scrapy import Request, Spider
from scrapy.loader import ItemLoader
from decimal import Decimal

from items import BrandItem, ProductItem
from utilities import get_session, prod_url_builder

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
extra_variant_count = 0

product_list = []


class GMProductSpider(Spider):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     return cls(settings.getbool("LOG_ENABLED"))

    name = cfg["gm_ProductSpider"]["name"]
    allowed_domains = cfg["gm_ProductSpider"]["allowed_domains"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pipelines.StoreBrandsPipeline": 100,
            "pipelines.StoreProductsPipeline": 200,
            "pipelines.StorePricesPipeline": 300,
        }
    }

    def __init__(self):
        logging.getLogger("scrapy").propagate = False

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename="logs/gm_product_log.txt",
    #     format="%(levelname)s: %(message)s",
    #     level=logging.ERROR,
    # )

    def start_requests(self) -> Iterator[Request]:
        session = get_session()
        website_name = cfg["website_names"]["gm"]
        brand_url_dict: dict = (
            session.query(BrandUrlDict).filter_by(website=website_name).first().data
        )
        # brand_url_dict = json.loads(brand_url_json.data)
        for brand, brand_url in brand_url_dict.items():
            api_url = prod_url_builder(website="gm", brand_url=brand_url)
            # api_url = (
            #     "https://" + self.allowed_domains[0] + brand_url + "/products.json"
            # )
            yield Request(
                url=api_url,
                callback=self.parse,
                meta={"brand": brand, "brand_url": brand_url, "total_results": 0},
            )

    def parse(
        self, response: response
    ) -> Union[Iterator[BrandItem], Iterator[ProductItem]]:
        global count
        global empty_count
        global skipped_brands
        global product_list
        global extra_variant_count

        total_results = response.meta.get("total_results")
        brand = response.meta.get("brand")
        brand_url = response.meta.get("brand_url")

        print("procesing: " + response.url)
        text_data = response.body.decode("utf8")
        json_string = text_data
        json_data = json.loads(json_string)
        results_list = json_data["products"]

        total_results += len(results_list)

        prod_list.append(json_data)

        for product_result in results_list:
            variant_list = product_result["variants"]
            variant_count = 1
            for product_variant in variant_list:
                extra_variant_count = len(variant_list) - 1
                try:
                    id = str(product_result["id"]) + "/" + str(variant_count)
                    variant_title = product_variant["title"]
                    prod_title = product_result["title"]
                    product_name = (
                        prod_title + " - " + variant_title
                        if (
                            variant_title is not None
                            and variant_title != "Default Title"
                            and prod_title != variant_title
                        )
                        else product_result["title"]
                    )

                    variant_size = product_variant["grams"]
                    variant_label = str(variant_size) + "g" if variant_size > 0 else ""

                    retail_price = Decimal(product_variant["price"])
                    current_price = Decimal(product_variant["price"])
                    in_stock = product_variant["available"]

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

                product = ProductItem()

                product["code"] = id
                product["brand"] = brand
                product["product_name"] = product_name
                product["variant"] = variant_label
                product["retail_price"] = retail_price
                product["on_sale"] = on_sale
                product["current_price"] = current_price
                product["in_stock"] = in_stock
                product["product_url"] = ""

                product_list.append(product)

                brand_item = BrandItem()
                brand_item["name"] = brand
                brand_item["url"] = brand_url

                # products_prices[id] = product

                yield brand_item
                yield product


# from scrapy.crawler import CrawlerProcess

# process = CrawlerProcess()
# # Run spiders sequentially
# process.crawl(GMProductSpider)
# process.start()  # the script will block here until all crawling jobs are finished
# print(f"\n Num products= {len(product_list)}\n")

# crawl()
# reactor.run()  # the script will block here until the last crawl call is finished
print("\nExtra Variants = " + str(extra_variant_count))
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
