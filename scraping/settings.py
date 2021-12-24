import logging
from scrapy.utils.log import configure_logging

configure_logging(install_root_handler=False)
logging.basicConfig(
    filename="logs/log.txt", format="%(levelname)s: %(message)s", level=logging.INFO
)

# USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
# USER_AGENT: "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
# ITEM_PIPELINES = {
#     "pipelines.StoreBrandsPipeline": 100,
# }

# logging.getLogger("scrapy").setLevel(logging.WARNING)

logging.getLogger("scrapy").propagate = False
COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
DOWNLOAD_DELAY = 1.0  # Minimum 1 second per request
AUTOTHROTTLE_DEBUG = True

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
    "scrapy.downloadermiddlewares.retry.RetryMiddleware": None,
    "scrapy_fake_useragent.middleware.RandomUserAgentMiddleware": 400,
    "scrapy_fake_useragent.middleware.RetryUserAgentMiddleware": 401,
}

FAKEUSERAGENT_PROVIDERS = [
    "scrapy_fake_useragent.providers.FakeUserAgentProvider",  # this is the first provider we'll try
    "scrapy_fake_useragent.providers.FakerProvider",  # if FakeUserAgentProvider fails, we'll use faker to generate a user-agent string for us
    "scrapy_fake_useragent.providers.FixedUserAgentProvider",  # fall back to USER_AGENT value
]
USER_AGENT = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
