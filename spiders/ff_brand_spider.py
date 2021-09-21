from typing import Iterator
import yaml
from scrapy.http import response
from scrapy import Spider
from items import BrandItem
import logging
from scrapy.utils.log import configure_logging

# load config file
cfg = yaml.safe_load(open("config.yaml"))

# Dictionary of brands with corresponding links as values
brands_links = {}


class FFBrandSpider(Spider):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     return cls(settings.getbool("LOG_ENABLED"))

    name = cfg["ff_BrandSpider"]["name"]
    allowed_domains = cfg["ff_BrandSpider"]["allowed_domains"]
    start_urls = cfg["ff_BrandSpider"]["start_urls"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pipelines.StoreBrandUrlDictPipeline": 100,
        }
    }

    # configure_logging(install_root_handler=False)
    # logging.basicConfig(
    #     filename="logs/ff_brand_log.txt",
    #     format="%(levelname)s: %(message)s",
    #     level=logging.ERROR,
    # )

    logging.getLogger("scrapy").propagate = False

    # Returns dictonary of (brand:link) pairs with only brands that match brands_dict
    def parse(self, response: response) -> Iterator[dict[str, str]]:
        print("procesing:" + response.url)

        brand_nodes = response.xpath(cfg["ff_BrandSpider"]["brand_nodes_xpath"])
        brands_list = brand_nodes.xpath(
            cfg["ff_BrandSpider"]["brands_list_xpath"]
        ).getall()

        links_list = brand_nodes.xpath(
            cfg["ff_BrandSpider"]["links_list_selector"]
        ).getall()

        for i, brand in enumerate(brands_list):
            # brand_item = BrandItem()
            # brand_item["name"] = brand.strip()
            # brand_item["url"] = links_list[i]
            brands_links[brand.strip()] = links_list[i]
            # yield brand_item
        yield brands_links


# from scrapy.crawler import CrawlerProcess

# process = CrawlerProcess()
# # Run spiders sequentially
# process.crawl(FFBrandSpider)
# process.start()  # the script will block here until all crawling jobs are finished

# print(f"\nNum = {len(brands_links)}\n")
