from utilities import get_hash
import yaml
import csv
from decimal import Decimal
from sqlalchemy.orm.session import Session
from items import ProductItem
from models import (
    get_session,
    WMBrand,
    WMProduct,
    WMCurrentPrice,
    WMHistoricalPrice,
    WMPriceFileInfo,
)
import logging
from datetime import datetime

# load config file
cfg = yaml.safe_load(open("config.yaml"))

# Scrape wm with:
# brand_nodes = response.xpath("//div[@class = 'content']//a/p[@class='label']")
# brands_list = brand_nodes.xpath("./text()").extract()


def wm_file_parser(
    file_path: str, session: Session, file_hash: bytes
) -> tuple[set[str], list[ProductItem]]:
    """Parses CSV of WM products

    Args:
        file_path(str): Path of wm product file to parse
        session(Session): Sessiob object for database
        file_hash(bytes): byte string containing hexdigest of file hash

    Returns:
        Tuple(Set, List): Tuple contains (Set of brands, List of ProductItems)
    """

    brands_set: set[str] = set()
    product_list: list = []
    with open(file_path) as f:
        reader = csv.reader(f, delimiter=",")
        next(reader)  # Skip headers on first line
        for product_row in reader:
            if not product_row:  # Skip blank lines
                continue
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
    file_info_obj = WMPriceFileInfo()
    file_info_obj.hash = file_hash
    file_info_obj.total_products = len(product_list)
    file_info_obj.time_stamp = datetime.now().isoformat(timespec="seconds")

    try:
        session.add(file_info_obj)
        session.commit()

    except Exception:
        session.rollback()
        raise

    finally:
        session.close()

    return brands_set, product_list


def wm_brands_pipeline(wm_brands: set[str], session: Session) -> None:
    """Save WM Brands in the database

    Args:
        wm_brands(Set): Set of all wm brands parsed from product csv file
        session(Session): Session object for database
    """
    logging.basicConfig(
        filename="logs/wm_brand_log.txt",
        format="%(levelname)s: %(message)s",
        level=logging.INFO,
    )

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


def wm_products_pipeline(product_list: list[ProductItem], session: Session) -> None:
    """Save WM Products in the database

    Args:
        products_list (list): List of ProductItems parsed from wm product csv
        session(Session): Session object for database
    """
    logging.basicConfig(
        filename="logs/wm_product_log.txt",
        format="%(levelname)s: %(message)s",
        level=logging.INFO,
    )

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


def wm_price_pipeline(product_list: list[ProductItem], session: Session) -> None:
    """Save wm prices in the database
    - If product does not exist yet in current price > saves in current price table
    - Else if exists and current price timestamp past threshold (>1day?) then update current price table and move old current price to historical prices table
    Args:
        products_list (List): List of ProductItems parsed from wm product csv
        session(Session): Session object for database
    """

    logging.basicConfig(
        filename="logs/wm_price_log.txt",
        format="%(levelname)s: %(message)s",
        level=logging.INFO,
    )

    current_price_table, product_table = (
        WMCurrentPrice,
        WMProduct,
    )

    for product in product_list:
        price_object = WMCurrentPrice()
        try:
            price_object.product_id = (
                session.query(product_table).filter_by(code=product["code"]).first().id
            )
        except Exception:
            print(f"Could not find product: {product['code']}\t {product['name']}")

        price_object.time_stamp = datetime.now().isoformat(timespec="seconds")
        price_object.retail_price = product["retail_price"]
        price_object.on_sale = product["on_sale"]
        price_object.current_price = product["current_price"]
        price_object.in_stock = product["in_stock"]

        # check whether the price exists in current price table
        existing_price_obj = (
            session.query(current_price_table)
            .filter_by(product_id=price_object.product_id)
            .first()
        )
        if existing_price_obj is not None:
            # Check if current price is over 24hours old
            # insertion_date = datetime.fromisoformat(existing_price_obj.time_stamp)
            time_between_insertion = datetime.now() - existing_price_obj.time_stamp
            if time_between_insertion.days > 1:
                historical_price = WMHistoricalPrice()

                # for historical, existing in zip(historical_price, existing_price_obj):
                #     setattr(historical_price, historical, existing)

                historical_price.product_id = existing_price_obj.product_id
                historical_price.time_stamp = existing_price_obj.time_stamp
                historical_price.retail_price = existing_price_obj.retail_price
                historical_price.on_sale = existing_price_obj.on_sale
                historical_price.current_price = existing_price_obj.current_price
                historical_price.in_stock = existing_price_obj.in_stock

                # session.query(current_price_table).filter(
                #     product_id=existing_price_obj.product_id
                # ).update(
                #     dict(
                #         time_stamp=price_object.time_stamp,
                #         retail_price=price_object.retail_price,
                #         on_sale=price_object.on_sale,
                #         current_price=price_object.current_price,
                #         in_stock=price_object.in_stock,
                #     )
                # )

                existing_price_obj.product_id = price_object.product_id
                existing_price_obj.time_stamp = price_object.time_stamp
                existing_price_obj.retail_price = price_object.retail_price
                existing_price_obj.on_sale = price_object.on_sale
                existing_price_obj.current_price = price_object.current_price
                existing_price_obj.in_stock = price_object.in_stock

                try:
                    session.add(historical_price)
                    session.commit()

                except:
                    session.rollback()
                    raise

                finally:
                    session.close()

            else:
                logging.log(
                    logging.INFO,
                    f"Update for product_id {price_object.product_id} less than 24hours old, not update was made.",
                )

        else:
            try:
                session.add(price_object)
                session.commit()

            except:
                session.rollback()
                raise

            finally:
                session.close()


# import tracemalloc


def main():
    # tracemalloc.start()
    # ... run your application ...
    wm_file = cfg["wm_product_file"]
    file_hash = get_hash(wm_file)
    session = get_session()
    existing_hash = session.query(WMPriceFileInfo).filter_by(hash=file_hash).first()
    if existing_hash is None:
        brands, products = wm_file_parser(wm_file, session, file_hash)

        print("\n")
        print(len(brands))
        print("\n")
        print("\n")
        print(len(products))
        print("\n")

        wm_brands_pipeline(brands, session)
        wm_products_pipeline(products, session)
        wm_price_pipeline(products, session)

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
