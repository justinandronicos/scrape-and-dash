import yaml
import csv
from decimal import Decimal
from typing import Dict, List, Tuple, Set, Union, BinaryIO
from io import TextIOWrapper
from sqlalchemy.orm import sessionmaker
from items import ProductItem
from models import (
    create_table,
    db_connect,
    WMBrand,
    WMProduct,
    WMCurrentPrice,
    WMHistoricalPrice,
)
import logging
import hashlib
import scrapy

# load config file
cfg = yaml.safe_load(open("config.yaml"))

# Scrape wholesome with:
# brand_nodes = response.xpath("//div[@class = 'content']//a/p[@class='label']")
# brands_list = brand_nodes.xpath("./text()").extract()


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


def best_selling_url_builder(website: str) -> Dict[str, str]:
    """Helper function to get dict of category and corresponding request url for best selling list according to website

    Args:
        website (str): Code for website (nl, ff)

    Returns:
        Dict[str, str]: Dict of {category: complete GET request string}
    """
    cat_url_dict: Dict[str, str] = {}
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


def highest_rated_url_builder(website: str) -> Dict[str, str]:
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


def check_hash(fpath: BinaryIO) -> str:
    """Calculate hash of file to check whether it has been updated

    Args:
        fname (BinaryIO): path of file to calculate hash for

    Returns:
        str: str containing hexdigest of hash
    """
    hash_md5: hashlib._Hash = hashlib.md5()
    with open(fpath, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def wm_file_parser() -> Tuple[Set[str], List[ProductItem]]:
    """Parses CSV of WM products

    Args: None

    Returns:
        Tuple(Set, List): Tuple contains (Set of brands, List of ProductItems)
    """
    brands_set: Set[str] = set()
    product_list = []
    with open(cfg["wm_product_file"]) as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)  # Skip headers on first line
        for product_row in reader:
            brand = product_row[1]
            product_name = product_row[2]
            if product_name == "" or product_name == "Description":
                continue  # Skip any extra header lines or with missing description

            try:
                wm_price = Decimal(product_row[3].replace(",", ""))
                retail_price = Decimal(product_row[4].replace(",", ""))
                code = product_row[0].replace(",", "")
            except Exception:
                logging.log(
                    logging.INFO,
                    f"Skipped line with missing values: {product_name}, {product_row[3]}, {product_row[4]}",
                )

            # These may be used in future
            on_sale = False
            in_stock = True
            variant = ""
            product_url = ""

            brands_set.add(brand)

            product = ProductItem()

            # product.id = code
            # product.brand = brand
            # product.product_name = product_name
            # product.variant = variant
            # product.retail_price = retail_price
            # product.on_sale = on_sale
            # product.current_price = wm_price
            # product.in_stock = in_stock
            # product.product_url = product_url

            product["code"] = code
            product["brand"] = brand
            product["product_name"] = product_name
            product["variant"] = variant
            product["retail_price"] = retail_price
            product["on_sale"] = on_sale
            product["current_price"] = wm_price
            product["in_stock"] = in_stock
            product["product_url"] = product_url

            product_list.append(product)

            # products_dict[code] = {
            #     "brand": product_brand,
            #     "product_name": product_brand + " " + product_name,
            #     "variant:": variant,
            #     "retail_price": retail_price,
            #     "on_sale": on_sale,
            #     "current_price": wm_price,
            #     "in_stock": in_stock,
            #     "product_url": product_url,
            # }
    return brands_set, product_list


def wm_brands_pipeline(wm_brands: Set[str]) -> None:
    """Save WM Brands in the database

    Args:
        wm_brands (Set): Set of all wm brands parsed from product csv file
    """
    logging.basicConfig(
        filename="logs/wm_brand_log.txt",
        format="%(levelname)s: %(message)s",
        level=logging.INFO,
    )

    # Initializes database connection and sessionmaker
    # Creates tables
    engine = db_connect()
    create_table(engine)
    Session = sessionmaker(bind=engine)
    # Save WM Brands in the database
    session = Session()

    brand_table = WMBrand
    for brand in wm_brands:
        brand_obj = WMBrand()
        brand_obj.name = brand
        brand_obj.url = None

        # check whether the brand exists
        existing_brand = (
            session.query(brand_table).filter_by(name=brand_obj.name).first()
        )
        if existing_brand is not None:
            logging.log(logging.INFO, f"Duplicate brand item found: {brand}")
            session.close()

        else:
            try:
                session.add(brand_obj)
                session.commit()

            except Exception:
                session.rollback()
                raise

            finally:
                session.close()


def wm_products_pipeline(product_list: List[ProductItem]) -> None:
    """Save WM Products in the database

    Args:
        products_list (List): List of ProductItems parsed from wm product csv
    """
    logging.basicConfig(
        filename="logs/wm_product_log.txt",
        format="%(levelname)s: %(message)s",
        level=logging.INFO,
    )

    engine = db_connect()
    create_table(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    product_table = WMProduct
    for product in product_list:
        product_obj = WMProduct()
        product_obj.code = product["code"]
        product_obj.name = product["product_name"]
        product_obj.brand_id = (
            session.query(WMBrand).filter_by(name=product["brand"]).first().id
        )
        product_obj.variant = None
        # product_obj.retail_price = product_dict["retail_price"]
        # product_obj.on_sale = product_dict["on_sale"]
        # product_obj.current_price = product_dict["current_price"]
        # product_obj.in_stock = product_dict["in_stock"]
        product_obj.url = None

        # check whether the product already exists in db
        existing_product = (
            session.query(product_table).filter_by(code=product_obj.code).first()
        )
        if existing_product is not None:  # the current product exists
            logging.log(
                logging.INFO,
                f"Duplicate product item found: {product['product_name']},\t code: {product['code']}",
            )
            session.close()

        else:
            try:
                session.add(product_obj)
                session.commit()

            except Exception:
                session.rollback()
                raise

            finally:
                session.close()


# import tracemalloc


def main():
    # tracemalloc.start()
    # ... run your application ...
    brands, products = wm_file_parser()
    print("\n")
    print(len(brands))
    print("\n")
    print("\n")
    print(len(products))
    print("\n")

    wm_brands_pipeline(brands)
    wm_products_pipeline(products)

    # snapshot = tracemalloc.take_snapshot()
    # top_stats = snapshot.statistics("lineno")

    # print("[ Top 10 ]")
    # for stat in top_stats[:10]:
    #     print(stat)


if __name__ == "__main__":
    main()

# wm_brands = {}
# # Returns Dict of of processed WM brands for easier matching (lowercase & remove commas/white space)
# #  with values of actual matching WM brands
# def get_wm_brands(wm_brands):
#     with open(cfg["wm_product_file"], newline="") as f:
#         reader = csv.reader(f)
#         next(reader)  # skip headers
#         for product_line in reader:
#             brand = product_line[1]
#             if brand not in wm_brands:
#                 wm_brands[
#                     brand.lower().replace("'", "").replace(" ", "").replace(".", "")
#                 ] = brand
#     return wm_brands

# get_wm_brands(wm_brands)
# print(wm_brands)


# # Swaps out brand names in WM product titles for easier matching
# # matched_brands = dict of Current site brand name: WM equivalent brand name
# def product_matcher(target_products, matched_brands):
#     wm_brands = sorted(matched_brands.values(), key=str.casefold)
#     target_brands = sorted(target_products.keys(), key=str.casefold)
#     processed_products = {}

#     print(wm_brands)
#     print("\n")
#     print(target_brands)

#     for i, brand in enumerate(target_brands):
#         for product_title in target_products[brand]:
#             # print("PROD TITLE = " + product_title + "\t" + brand + "\t" + wm_brands[i])
#             new_title = product_title.replace(brand, wm_brands[i])
#             product_values = target_products[brand].get(product_title)
#             # print("NEW TITLE = " + new_title)
#             # print(target_products[brand].get(product_title))
#             # print(product_values)
#             if brand not in processed_products.keys():
#                 processed_products[brand] = {new_title: product_values}
#             else:
#                 processed_products[brand][new_title] = product_values

#     return processed_products


# # Returns matching brand
# def brand_matcher(wm_brands, brand):
#     brand.lower().replace("'", "").replace(".", "").rstrip("s")

# # Helper function to match brand_names between sites for easier product matching
# # Swaps name in name_swap_file via index (each brand on new line, comma seperated between each site)
# # Returns dict of target_brand: equivalent_wm_brand_name
# def brand_renamer(target_match):
#     name_swap_file = "name_swaps.csv"
#     brand_swaps = {}
#     with open(name_swap_file) as f:
#         reader = csv.reader(f, delimiter=",")
#         for brand_row in reader:
#             # print(print("Brand_Row =" + str(brand_row)))
#             target_brand = brand_row[target_match].strip()
#             # print("Target_brand =" + target_brand)
#             if target_brand != "":
#                 brand_swaps[target_brand] = brand_row[0]
#             # target_match = int corresponding to index/column to swap to
#     # print("Brand Swaps = " + str(brand_swaps))
#     return brand_swaps
