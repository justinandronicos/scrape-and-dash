import yaml
from scrapy.http import response
from scrapy import Spider
from typing import Iterator
from items import BrandItem
import logging
from scrapy.utils.log import configure_logging

# load config file
cfg = yaml.safe_load(open("config.yaml"))

# # Dictionary of brands with corresponding links as values
# brands_links = {}


class NLBrandSpider(Spider):
    # @classmethod
    # def from_crawler(cls, crawler):
    #     settings = crawler.settings
    #     return cls(settings.getbool("LOG_ENABLED"))

    # def __init__(self, settings):
    #     self.settings = settings

    name = cfg["nl_BrandSpider"]["name"]
    allowed_domains = cfg["nl_BrandSpider"]["allowed_domains"]
    start_urls = cfg["nl_BrandSpider"]["start_urls"]

    custom_settings = {
        "ITEM_PIPELINES": {
            "pipelines.StoreBrandsPipeline": 100,
        }
    }

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename="logs/nl_brand_log.txt",
        format="%(levelname)s: %(message)s",
        level=logging.ERROR,
    )

    def parse(self, response: response) -> Iterator[BrandItem]:

        print("procesing:" + response.url)

        brand_nodes = response.xpath(cfg["nl_BrandSpider"]["brand_nodes_xpath"])
        brands_list = brand_nodes.xpath(
            cfg["nl_BrandSpider"]["brands_list_xpath"]
        ).getall()

        links_list = response.css(cfg["nl_BrandSpider"]["links_list_selector"]).getall()
        (base_url,) = cfg["nl_BrandSpider"]["allowed_domains"]

        for i, brand in enumerate(brands_list):
            brand_item = BrandItem()
            brand_item["name"] = brand.strip()
            brand_item["url"] = base_url + links_list[i]
            # brands_links[brand] = links_list[i]
            yield brand_item


# from scrapy.crawler import CrawlerProcess

# process = CrawlerProcess()
# # Run spiders sequentially
# process.crawl(NLBrandSpider)
# process.start()  # the script will block here until all crawling jobs are finished

# print(f"\nNum = {len(brands_links)}\n")
