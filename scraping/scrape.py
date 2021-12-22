import os
import sys

dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(dir))

from models_items import models

from spiders.nl_product_spider import NLProductSpider
from spiders.ff_brand_spider import FFBrandSpider
from spiders.nl_brand_spider import NLBrandSpider
from spiders.ff_product_spider import FFProductSpider
from spiders.nl_category_spider import NLCategorySpider
from spiders.ff_category_spider import FFCategorySpider
from spiders.gm_product_spider import GMProductSpider
from spiders.gm_brand_spider import GMBrandSpider

# import wm_parser
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerProcess
import logging

# from models import db_connect, create_table

# Nested dictionary of form {id: {brand, product_name, variant, retail_price, on_sale, current_price, in_stock, product_url}}
# Access product prices with wm_products_prices[product_id]
wm_products_prices = {}

# Nested dictionary of form {id: {brand, product_name, variant, retail_price, on_sale, current_price, in_stock, product_url}}
# Access product prices with nl_products_prices[product_id]
nl_products_prices = {}

# Nested dictionary of form {id: {brand, product_name, variant, retail_price, on_sale, current_price, in_stock, product_url}}
# Access product prices with ff_products_prices[product_id]
ff_products_prices = {}

# spider_list = [
#     NLBrandSpider,
#     FFBrandSpider,
#     NLProductSpider,
#     FFProductSpider,
#     NLCategorySpider,
#     FFCategorySpider,
# ]
# runner_list = [(CrawlerRunner(), spider) for spider in spider_list]


def main():
    engine = models.db_connect()
    models.create_table(engine)

    configure_logging()
    # wm_parser.main()

    # runner.crawl(NLBrandSpider)
    # runner.crawl(FFBrandSpider)
    # runner.crawl(GMBrandSpider)
    # runner.crawl(NLProductSpider)
    # runner.crawl(FFProductSpider)
    # runner.crawl(GMProductSpider)
    # runner.crawl(NLCategorySpider)
    # runner.crawl(FFCategorySpider)
    # d = runner.join()
    # d.addBoth(lambda _: reactor.stop())
    # reactor.run()

    runner = CrawlerRunner()
    logging.getLogger("scrapy").propagate = False

    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(NLBrandSpider)
        yield runner.crawl(FFBrandSpider)
        yield runner.crawl(GMBrandSpider)
        yield runner.crawl(NLProductSpider)
        yield runner.crawl(FFProductSpider)
        yield runner.crawl(GMProductSpider)
        yield runner.crawl(NLCategorySpider)
        yield runner.crawl(FFCategorySpider)
        reactor.stop()

    crawl()
    reactor.run()

    # runner.crawl(NLProductSpider)
    # runner.crawl(FFProductSpider)
    # runner.crawl(GMProductSpider)
    # runner.crawl(NLCategorySpider)
    # runner.crawl(FFCategorySpider)
    # reactor.stop()

    # process = CrawlerProcess()
    # # Run spiders simultaneously
    # process.crawl(NLBrandSpider)
    # process.crawl(FFBrandSpider)
    # process.crawl(NLProductSpider)
    # process.crawl(FFProductSpider)
    # process.crawl(GMProductSpider)
    # process.crawl(NLCategorySpider)
    # process.crawl(FFCategorySpider)
    # process.start()  # the script will block here until all crawling jobs are finished

    # wm_brands, wm_products = wm_file_parser()
    # nl_products_prices = nl_product_spider.products_prices
    # ff_products_prices = ff_product_spider.products_prices

    # nl_brands = nl_brand_spider.brands_links
    # ff_brands = ff_brand_spider.brands_links
    # print("\n\nfinito\n\n")
    # print("nl products: " + str(len(nl_products_prices)))

    # print("\n\nfinito\n\n")
    # print("ff products: " + str(len(ff_products_prices)))

    # print("\n\nfinito\n\n")
    # print("nl brands: " + str(len(nl_brands)))c

    # print("\n\nfinito\n\n")
    # print("ff brands: " + str(len(ff_brands)))

    # print("\n\n")
    # nl_prod_list = list(nl_products_prices.values())
    # ff_prod_list = list(ff_products_prices.values())
    # nl_brands_from_prods = {product["brand"] for product in nl_prod_list}
    # ff_brands_from_prods = {product["brand"] for product in ff_prod_list}

    # import numpy as np

    # nl_brand_diff = np.setdiff1d(list(nl_brands.keys()), list(nl_brands_from_prods))
    # print(nl_brand_diff)
    # print("\n")
    # ff_brand_diff = np.setdiff1d(list(ff_brands.keys()), list(ff_brands_from_prods))
    # print(ff_brand_diff)
    # print("\n\n")
    # print(len(nl_brands) - len(nl_brands_from_prods))
    # print("\n")
    # print(len(ff_brands) - len(ff_brands_from_prods))
    # print("\n\n")

    # if (
    #     len(nl_products_prices)
    #     + nl_product_spider.empty_count
    #     - nl_product_spider.extra_variant_count
    # ) == 5226:
    #     print("Successfully scraped nl products")

    # print("\n")

    # if (len(ff_products_prices) + ff_product_spider.empty_count) == 8512:
    #     print("Successfully scraped ff products")


if __name__ == "__main__":
    # handler = logging.FileHandler("logs/sqlalchemy_log.txt")
    # handler.setLevel(logging.DEBUG)
    # logging.getLogger("sqlalchemy").addHandler(handler)
    import time

    start_time = time.time()
    main()
    print("\n\n--- %s seconds ---" % (time.time() - start_time))

    # print(nl_products_prices.keys())

    # print(nl_products_prices["10594501"])
    # print("\n\n")

    # print([key for key in nl_products_prices.keys() if "21636" in key])
    # print("\n\n")
    # print([key for key in nl_products_prices.keys() if "354701" in key])

    # print(nl_products_prices["35470123"])
    # print("\n\n")
