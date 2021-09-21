import yaml
from typing import BinaryIO
from io import TextIOWrapper
import hashlib
from sqlalchemy.orm import sessionmaker
from models import db_connect, create_table

# load config file
cfg = yaml.safe_load(open("config.yaml"))


def prod_url_builder(website: str, offset: int = None, page_number: str = None) -> str:
    """Helper function called by NLProductSpider/FFProductSpider class in nl_product_spider and ff_product_spider to build Nl/FF url GET request string for all products

    Args:
        website (str): Code for website (nl, ff)
        offset (int, optional): Sets start point for ff api request. Defaults to None.
        page_number (str, optional): Sets page number for nl api request. Defaults to None.

    Returns:
        str: Complete GET request string
    """
    api_url: str
    if website == "nl":
        api_url = cfg["nl_api_url"] + "&resultsPerPage=500&page=" + str(page_number)
    elif website == "ff":
        api_url = (
            cfg["ff_api_url"]
            + cfg["ff_category_filter_key"]
            + str(2)  # cat_id=2 returns all products
            + "&max=500&offset="
            + str(offset)
        )
    return api_url


def best_selling_url_builder(website: str) -> dict[str, str]:
    """Helper function to get dict of category and corresponding request url for best selling list according to website

    Args:
        website (str): Code for website (nl, ff)

    Returns:
        Dict[str, str]: Dict of {category: complete GET request string}
    """
    cat_url_dict: dict[str, str] = {}
    api_url: str
    if website == "nl":
        api_url = (
            cfg["nl_api_url"]
            + "&resultsPerPage="
            + str(cfg["nl_category_results_per_page"])
            + cfg["nl_best_selling_key"]
            + cfg["nl_category_filter_key"]
        )
        for category, value in cfg["nl_category_values"].items():
            cat_url_dict[category] = api_url + value

    elif website == "ff":
        api_url = (
            cfg["ff_api_url"]
            + "max="
            + str(cfg["ff_category_results_per_page"])
            + "&offset=0"
            + cfg["ff_best_selling_key"]
            + cfg["ff_category_filter_key"]
        )
        for category, value in cfg["ff_category_values"].items():
            cat_url_dict[category] = api_url + str(value)

    return cat_url_dict


def highest_rated_url_builder(website: str) -> dict[str, str]:
    """Helper function to get dict of category and corresponding request url for highest rated list according to website

    Args:
        website (str): Code for website (nl, ff)

    Returns:
        Dict[str, str]: Dict of {category: complete GET request string}
    """
    cat_url_dict = {}
    api_url: str
    if website == "nl":
        api_url = (
            cfg["nl_api_url"]
            + "&resultsPerPage="
            + str(cfg["nl_category_results_per_page"])
            + cfg["nl_highest_rated_key"]
            + cfg["nl_category_filter_key"]
        )
        for category, value in cfg["nl_category_values"].items():
            cat_url_dict[category] = api_url + value

    elif website == "ff":
        api_url = (
            cfg["ff_api_url"]
            + "max="
            + str(cfg["ff_category_results_per_page"])
            + "&offset=0"
            + cfg["ff_highest_rated_key"]
            + cfg["ff_category_filter_key"]
        )
        for category, value in cfg["ff_category_values"].items():
            cat_url_dict[category] = api_url + str(value)

    return cat_url_dict


import sys


def get_hash(fpath: BinaryIO) -> bytes:
    """Calculate hash of file to check whether it has been updated

    Args:
        fname(BinaryIO): path of file to calculate hash for

    Returns:
        binary string: binary string containing hexdigest of hash
    """
    hash_md5: hashlib._Hash = hashlib.md5()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    complete_hash = hash_md5.hexdigest()
    return complete_hash.encode("ascii")


def get_session():
    """Initializes database connection and sessionmaker

    Returns:
        Session: Session object for database
    """
    engine = db_connect()
    # create_table(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
