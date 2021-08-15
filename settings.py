import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename="log.txt", format="%(levelname)s: %(message)s", level=logging.INFO
)

# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
USER_AGENT: "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
# ITEM_PIPELINES = {
#     "pipelines.StoreBrandsPipeline": 100,
# }

logging.getLogger("scrapy").setLevel(logging.WARNING)
