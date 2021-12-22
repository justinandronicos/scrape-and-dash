import yaml
from scrapy.http import response
from scrapy import Spider
from typing import Iterator
from models_items.items import BrandItem
import logging
from scrapy.utils.log import configure_logging

# import redis
# import json

# Establish a connection to the Redis database at redis://localhost:6379
# r = redis.Redis(host="localhost", port=6379)

# load config file
cfg = yaml.safe_load(open("config.yaml"))

# Dictionary of brands with corresponding links as values
brands_links = {}


class GMBrandSpider(Spider):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     return cls(settings.getbool("LOG_ENABLED"))

    name = cfg["gm_BrandSpider"]["name"]
    allowed_domains = cfg["gm_BrandSpider"]["allowed_domains"]
    start_urls = cfg["gm_BrandSpider"]["start_urls"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pipelines.StoreBrandUrlDictPipeline": 100,
        }
    }

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename=f"{cfg['scraper_log_path']}/ff_brand_log.txt",
    #     format="%(levelname)s: %(message)s",
    #     level=logging.ERROR,
    # )

    def __init__(self):
        logging.getLogger("scrapy").propagate = False

    # Returns dictonary of (brand:link) pairs with only brands that match brands_dict
    def parse(self, response: response) -> Iterator[dict[str, str]]:
        print(f"procesing: {response.url}")

        brand_nodes = response.xpath(cfg["gm_BrandSpider"]["brand_nodes_xpath"])
        brands_list = brand_nodes.xpath(
            cfg["gm_BrandSpider"]["brands_list_xpath"]
        ).getall()

        links_list = brand_nodes.xpath(
            cfg["gm_BrandSpider"]["links_list_selector"]
        ).getall()
        (base_url,) = cfg["gm_BrandSpider"]["allowed_domains"]

        for i, brand in enumerate(brands_list):
            # brand_item = BrandItem()
            # brand_item["name"] = brand.strip()
            # brand_item["url"] = base_url + links_list[i]
            brands_links[brand.strip()] = base_url + links_list[i]
            # yield brand_item
        yield brands_links


# from scrapy.crawler import CrawlerProcess

# process = CrawlerProcess()
# # Run spiders sequentially
# process.crawlGMBrandSpider)
# process.start()  # the script will block here until all crawling jobs are finished
# print(len(brands_links))
# dict_name = cfg["gm_BrandSpider"]["name"]
# r.hmset(dict_name, brands_links)
# new_data = {key.decode(): val.decode() for key, val in r.hgetall(dict_name).items()}
# print(new_data)

# print(f"\nNum = {len(brands_links)}\n")

# print(brands_links.items())
