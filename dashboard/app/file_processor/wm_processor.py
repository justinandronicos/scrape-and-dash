from typing import BinaryIO, Union
import hashlib
import yaml
from decimal import Decimal
from sqlalchemy.orm.session import Session
from models_items.items import ProductItem
import logging
from datetime import datetime
from io import StringIO, BytesIO
import pandas as pd
from file_processor.wm_pipelines import (
    wm_brands_pipeline,
    wm_products_pipeline,
    wm_price_pipeline,
)
from models_items.models import WMPriceFileInfo

from app import session


# load config file
cfg = yaml.safe_load(open("config.yaml"))


def get_hash(contents_stream: BinaryIO) -> bytes:
    """Calculate hash of file to check whether it has been updated

    Args:
        contents_stream(BinaryIO): binary stream of file to calculate hash for

    Returns:
        binary string: binary string containing hexdigest of hash
    """
    hash_md5: hashlib._Hash = hashlib.md5()
    for chunk in iter(lambda: contents_stream.read(4096), b""):
        hash_md5.update(chunk)
    complete_hash = hash_md5.hexdigest()
    return complete_hash.encode("ascii")


def file_parser(
    df: pd.DataFrame, session: Session, file_hash: bytes
) -> tuple[set[str], list[ProductItem]]:
    """Parses CSV or Excel file of WM products

    Args:
        file_path(str): Path of wm product file to parse
        session(Session): Sessiob object for database
        file_hash(bytes): byte string containing hexdigest of file hash

    Returns:
        Tuple(Set, List): Tuple contains (Set of brands, List of ProductItems)
    """

    brands_set: set[str] = set()
    product_list: list = []
    for product_row in df.itertuples(index=False):
        brand = product_row[1]
        product_name = product_row[2]
        if product_name == "" or product_name == "Description":
            continue  # Skip any extra header lines or with missing description

        try:
            wm_price = Decimal(product_row[3])
            retail_price = Decimal(product_row[4])
            code = product_row[0]
        except Exception:
            print(
                f"Skipped line with missing values: {product_name}, {product_row[3]}, {product_row[4]}"
            )
            # logging.log(
            #     logging.INFO,
            #     f"Skipped line with missing values: {product_name}, {product_row[3]}, {product_row[4]}",
            # )

        # These may be used in future
        on_sale = False
        in_stock = True
        variant = None
        product_url = None

        brands_set.add(brand)

        product = ProductItem(
            code=code,
            brand=brand,
            product_name=product_name,
            variant=variant,
            retail_price=retail_price,
            on_sale=on_sale,
            current_price=wm_price,
            in_stock=in_stock,
            product_url=product_url,
        )

        # product["code"] = code
        # product["brand"] = brand
        # product["product_name"] = product_name
        # product["variant"] = variant
        # product["retail_price"] = retail_price
        # product["on_sale"] = on_sale
        # product["current_price"] = wm_price
        # product["in_stock"] = in_stock
        # product["product_url"] = product_url

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


# import tracemalloc


def process_file(
    content: Union[StringIO, BytesIO], filename: str, file_hash: bytes
) -> pd.DataFrame:
    # tracemalloc.start()
    # ... run your application ...

    # Read columns as strings to preserve price to Decimal conversion
    df = pd.read_csv(content, dtype=str)
    brands, products = file_parser(df, session, file_hash)

    print(f"\n Brands: {len(brands)}")
    print(f"\n Products: {len(products)}")

    wm_brands_pipeline(brands, session)
    wm_products_pipeline(products, session)
    wm_price_pipeline(products, session)
    return df


# else:
# print(f"File already used: {file_hash}, {filename}")

# snapshot = tracemalloc.take_snapshot()
# top_stats = snapshot.statistics("lineno")

# print("[ Top 10 ]")
# for stat in top_stats[:10]:
#     print(stat)


# if __name__ == "__main__":
#     main()
