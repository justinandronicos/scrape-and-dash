from yaml import safe_load
from typing import Iterator
from json import loads
from scrapy.http import response

# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging
from scrapy import Request, Spider
from scrapy.loader import ItemLoader

from models_items.items import RankedProductItem
from utilities import best_selling_url_builder, highest_rated_url_builder

import logging
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess

# load config file
cfg = safe_load(open("config.yaml"))

rated_list = {}
selling_list = {}

num_results = 0


class NLCategorySpider(Spider):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     return cls(settings.getbool("LOG_ENABLED"))

    name = cfg["nl_CategorySpider"]["name"]
    allowed_domains = cfg["nl_CategorySpider"]["allowed_domains"]

    custom_settings = {"ITEM_PIPELINES": {"pipelines.StoreRankedProductsPipeline": 100}}

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename=f"{cfg['scraper_log_path']}/nl_ranked_product_log.txt",
    #     format="%(levelname)s: %(message)s",
    #     level=logging.ERROR,
    # )

    logging.getLogger("scrapy").propagate = False

    def start_requests(self) -> Iterator[Request]:
        best_selling_url_dict = best_selling_url_builder("nl")
        highest_rated_url_dict = highest_rated_url_builder("nl")
        for category, url in best_selling_url_dict.items():
            filter = "best_selling"
            yield Request(
                url=url,
                callback=self.parse,
                meta={"filter": filter, "category": category, "max_results": 50},
            )
        for category, url in highest_rated_url_dict.items():
            filter = "highest_rated"
            yield Request(
                url=url,
                callback=self.parse,
                meta={"filter": filter, "category": category, "max_results": 50},
            )

    def parse(self, response: response) -> Iterator[RankedProductItem]:
        filter = response.meta.get("filter")
        category = response.meta.get("category")

        text_data = response.body.decode("utf8")
        json_string = text_data[text_data.index("{") :]
        json_data = loads(json_string)

        global num_results

        num_results += len(json_data["results"])

        # print(f"CATEGORY: {category}, length {len(json_data['results'])}")

        # Results per page has been set to 51 because API returns n-1 results per page for some categories
        results = json_data["results"]
        if len(results) > 50:
            del results[-1]

        for index, product_result in enumerate(results):
            uid = product_result["uid"]
            name = product_result["name"].replace("&amp;", "&")
            category = category
            ranking = index + 1
            # brand = product_result["brand"]
            # product_name = product_result["name"].replace("&amp;", "&")

            ranked_product = RankedProductItem()

            ranked_product["code"] = uid + "/" + str(1)  # Will match first variant only

            ranked_product["category"] = category
            ranked_product["ranking"] = ranking
            ranked_product["filter"] = filter
            ranked_product["name"] = name

            if filter == "best_selling":
                # > best_selling_pipeline
                if category not in selling_list.keys():
                    selling_list[category] = [ranked_product]

                else:
                    selling_list[category].append(ranked_product)

            elif filter == "highest_rated":
                rating = float(product_result["rating"])  # 5 star rating (float)
                review_count = product_result["ratingCount"]
                ranked_product["rating"] = rating
                ranked_product["review_count"] = review_count

                # > highest_rated_pipeline
                if category not in rated_list.keys():
                    rated_list[category] = [ranked_product]
                else:
                    rated_list[category].append(ranked_product)

            yield ranked_product


# configure_logging()

# process = CrawlerProcess()
# # Run spiders sequentially
# process.crawl(NLCategorySpider)
# process.start()  # the script will block here until all crawling jobs are finished

# print(f"Best Sellers: {selling_list} \n\n")
# print(f"Highest Rated: {rated_list}")
print(f"Num selling: {len(selling_list)}. \n")
print(f"Num Rated: {len(rated_list)} \n")
print(f"Total results: {num_results} \n")

for key in selling_list.keys():
    print(f"Category: {key}\t Entries: {len(selling_list[key])} \n")

print("Rated list \n")
for key in rated_list.keys():
    print(f"Category: {key}\t Entries: {len(rated_list[key])} \n")

print(f"Selling:\t{sum(len(v) for v in selling_list.values())}\n")
print(f"Rated:\t{sum(len(v) for v in selling_list.values())}\n")
