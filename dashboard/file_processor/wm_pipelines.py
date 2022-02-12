from decimal import Decimal
from sqlalchemy.orm.session import Session
from models_items.items import ProductItem
from models_items.models import (
    WMBrand,
    WMProduct,
    WMCurrentPrice,
    WMHistoricalPrice,
)
import logging
from datetime import datetime
import os


def wm_brands_pipeline(wm_brands: set[str], session: Session) -> None:
    """Save WM Brands in the database

    Args:
        wm_brands(Set): Set of all wm brands parsed from product csv file
        session(Session): Session object for database
    """
    logging.basicConfig(
        filename=f"{os.getcwd()}/dashboard/file_processor/logs/wm_log.txt",
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
    # logging.basicConfig(
    #     filename="wm_product_log.txt",
    #     format="%(levelname)s: %(message)s",
    #     level=logging.INFO,
    # )

    product_table = WMProduct
    for product in product_list:
        product_obj = WMProduct()
        product_obj.code = product.code
        product_obj.name = product.product_name
        product_obj.brand_id = (
            session.query(WMBrand).filter_by(name=product.brand).first().id
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
                f"Duplicate product item found: {product.product_name},\t code: {product.code}",
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
    - Else if exists and current price timestamp past threshold (>=24hrs) then update current price table and move old current price to historical prices table
    Args:
        products_list (List): List of ProductItems parsed from wm product csv
        session(Session): Session object for database
    """

    # logging.basicConfig(
    #     filename="wm_price_log.txt",
    #     format="%(levelname)s: %(message)s",
    #     level=logging.INFO,
    # )

    current_price_table, product_table = (
        WMCurrentPrice,
        WMProduct,
    )

    for product in product_list:
        price_object = WMCurrentPrice()
        try:
            price_object.product_id = (
                session.query(product_table).filter_by(code=product.code).first().id
            )
        except Exception:
            print(f"Could not find product: {product.code}\t {product.product_name}")

        current_dtime = datetime.now()
        price_object.time_stamp = current_dtime.isoformat(timespec="seconds")
        price_object.retail_price = product.retail_price
        price_object.on_sale = product.on_sale
        price_object.current_price = product.current_price
        price_object.in_stock = product.in_stock

        # check whether the price exists in current price table
        existing_price_obj = (
            session.query(current_price_table)
            .filter_by(product_id=price_object.product_id)
            .first()
        )
        if existing_price_obj is not None:
            # Check if current price is at least 24hours old
            # insertion_date = datetime.fromisoformat(existing_price_obj.time_stamp)
            time_between_insertion = current_dtime - existing_price_obj.time_stamp
            if time_between_insertion.days >= 1:
                # if time_between_insertion.total_seconds() >= 86400:
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
