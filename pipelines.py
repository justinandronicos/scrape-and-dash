# from sqlalchemy.sql.expression import and_
from sqlalchemy.sql.expression import union
from items import BrandItem, ProductItem, RankedProductItem
from psycopg2.extras import Json
import yaml
from typing import Union

# from sqlalchemy.ext.declarative import DeclarativeMeta
from scrapy import Spider
from sqlalchemy.orm import sessionmaker
import logging
from datetime import datetime
from models import (
    BrandUrlDict,
    db_connect,
    NLBrand,
    FFBrand,
    GMBrand,
    WMBrand,
    NLProduct,
    FFProduct,
    GMProduct,
    WMProduct,
    NLCurrentPrice,
    FFCurrentPrice,
    GMCurrentPrice,
    WMCurrentPrice,
    NLHistoricalPrice,
    FFHistoricalPrice,
    GMHistoricalPrice,
    WMHistoricalPrice,
    NLBestSelling,
    FFBestSelling,
    NLHighestRated,
    FFHighestRated,
)

cfg = yaml.safe_load(open("config.yaml"))
logging.getLogger("scrapy").propagate = False


class StoreBrandUrlDictPipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker"""
        engine = db_connect()
        # create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item: dict, spider: Spider) -> dict[str, str]:
        """Save brands/urls dict in the database"""
        session = self.Session()
        dict_table = BrandUrlDict
        website_names = cfg["website_names"]
        website_name = (
            website_names["nl"]
            if spider.name == "nl_brands"
            else website_names["ff"]
            if spider.name == "ff_brands"
            else website_names["gm"]
            if spider.name == "gm_brands"
            else None
        )

        existing_dict = (
            session.query(dict_table).filter_by(website=website_name).first()
        )
        if existing_dict is not None:
            existing_dict.data = item
        else:
            brand_url_dict = BrandUrlDict()
            brand_url_dict.website = website_name
            if len(item) is not None:
                brand_url_dict.data = item
            else:
                print("EMPTY DIC")
            session.add(brand_url_dict)

        session.commit()
        session.close()
        return item


class StoreBrandsPipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker"""
        engine = db_connect()
        # create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(
        self, item: Union[BrandItem, ProductItem], spider: Spider
    ) -> Union[BrandItem, ProductItem]:
        """Save Brands in the database
        This method is called for BrandItems
        Skips any ProductItems that are passed
        """

        # Skip any product items
        if not isinstance(item, BrandItem):
            return item

        session = self.Session()

        brand_table, brand = (
            (NLBrand, NLBrand())
            if spider.name == "nl_products"
            else (FFBrand, FFBrand())
            if spider.name == "ff_products"
            else (GMBrand, GMBrand())
            if spider.name == "gm_products"
            else (None, None)
        )

        brand.name = item["name"]
        brand.url = item["url"]

        # check whether the brand exists
        existing_brand = session.query(brand_table).filter_by(name=brand.name).first()
        if existing_brand is not None:
            # Check if url needs to be updated
            if existing_brand.url != brand.url:
                logging.log(
                    logging.INFO,
                    f"Updating url for duplicate brand item: {item['name']}",
                )
                try:
                    existing_brand.url = brand.url
                    session.commit()
                except Exception:
                    session.rollback()
                    raise
                finally:
                    session.close()

            else:
                logging.log(logging.INFO, f"Duplicate brand item found: {item['name']}")
                session.close()
        else:
            try:
                session.add(brand)
                session.commit()

            except Exception:
                session.rollback()
                raise

            finally:
                session.close()

        return item


class StoreProductsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        """
        engine = db_connect()
        # create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(
        self, item: Union[BrandItem, ProductItem], spider: Spider
    ) -> Union[BrandItem, ProductItem]:
        """Save products in the database
        This method is called for every Product Item pipeline component
        Skips any BrandItems that are passed
        """

        # Skip any brand items
        if not isinstance(item, ProductItem):
            return item

        session = self.Session()

        product_table, product, brand_table = (
            (NLProduct, NLProduct(), NLBrand)
            if spider.name == "nl_products"
            else (FFProduct, FFProduct(), FFBrand)
            if spider.name == "ff_products"
            else (GMProduct, GMProduct(), GMBrand)
            if spider.name == "gm_products"
            else (None, None, None)
        )

        product.code = item["code"]
        product.name = item["product_name"]
        try:
            product.brand_id = (
                session.query(brand_table).filter_by(name=item["brand"]).first().id
            )
        except AttributeError:
            print(
                f"brand: {item['brand']}\t prod_table: {product_table}\t prod: {product}\t brand_table: {brand_table}"
            )
            session.close()

        product.variant = item["variant"]
        product.url = item["product_url"]

        # product.retail_price = product_dict["retail_price"]
        # product.on_sale = product_dict["on_sale"]
        # product.current_price = product_dict["current_price"]
        # product.in_stock = product_dict["in_stock"]

        # check whether the product already exists in db
        existing_product = (
            session.query(product_table).filter_by(code=product.code).first()
        )
        if existing_product is not None:  # the current product exists
            logging.log(
                logging.INFO,
                f"Duplicate product item found: {item['product_name']}",
            )
            session.close()

        else:
            try:
                session.add(product)
                session.commit()

            except Exception:
                session.rollback()
                raise

            finally:
                session.close()

        return item


class StorePricesPipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker"""
        engine = db_connect()
        # create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(
        self, item: Union[BrandItem, ProductItem], spider: Spider
    ) -> Union[BrandItem, ProductItem]:
        """Save prices in the database
        - If product does not exist yet in current price > saves in current price table
        - Else if exists and current price timestamp past threshold (>1day?) then update current price table and move old current price to historical prices table
        This method is called for every Product Item pipeline component
        Skips any brand items passed
        """

        # Skip any brand items
        if not isinstance(item, ProductItem):
            return item

        session = self.Session()

        current_price_table, price_object, product_table = (
            (NLCurrentPrice, NLCurrentPrice(), NLProduct)
            if spider.name == "nl_products"
            else (FFCurrentPrice, FFCurrentPrice(), FFProduct)
            if spider.name == "ff_products"
            else (GMCurrentPrice, GMCurrentPrice(), GMProduct)
            if spider.name == "gm_products"
            else (None, None, None)
        )

        try:
            price_object.product_id = (
                session.query(product_table).filter_by(code=item["code"]).first().id
            )
        except Exception:
            print(f"Could not find product: {item['code']}\t {item['name']}")
            session.close()

        price_object.time_stamp = datetime.now().isoformat(timespec="seconds")
        price_object.retail_price = item["retail_price"]
        price_object.on_sale = item["on_sale"]
        price_object.current_price = item["current_price"]
        price_object.in_stock = item["in_stock"]

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
                historical_price = (
                    NLHistoricalPrice()
                    if spider.name == "nl_products"
                    else FFHistoricalPrice()
                    if spider.name == "ff_products"
                    else GMHistoricalPrice()
                    if spider.name == "gm_products"
                    else None
                )

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

                except Exception:
                    session.rollback()
                    raise

                finally:
                    session.close()

            else:
                logging.log(
                    logging.INFO,
                    f"Update for product_id {price_object.product_id} less than 24hours old, no update was made.",
                )
                session.close()

        else:
            try:
                session.add(price_object)
                session.commit()

            except Exception:
                session.rollback()
                raise

            finally:
                session.close()

        return item


class StoreRankedProductsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        """
        engine = db_connect()
        # create_table(engine)
        self.Session = sessionmaker(bind=engine)
        self.cases = {
            ("nl_categories", "best_selling"): (
                NLBestSelling,
                NLProduct,
            ),
            ("nl_categories", "highest_rated"): (
                NLHighestRated,
                NLProduct,
            ),
            ("ff_categories", "best_selling"): (
                FFBestSelling,
                FFProduct,
            ),
            ("ff_categories", "highest_rated"): (
                FFHighestRated,
                FFProduct,
            ),
        }

    def process_item(
        self, item: RankedProductItem, spider: Spider
    ) -> RankedProductItem:
        """Save ranked products (best selling, highest rated) in the database
        This method is called for every RankedProduct Item pipeline component
        List of highest ranking and highest rating are updated if > 24 hours since last update (timestamp), old items still kept in table
        """

        session = self.Session()

        filter = item["filter"]

        ranked_product_table, product_table = self.cases[(spider.name, filter)]
        ranked_product = ranked_product_table()

        ranked_product.category = item["category"]
        ranked_product.ranking = item["ranking"]
        ranked_product.time_stamp = datetime.now().isoformat(timespec="seconds")

        try:
            ranked_product.product_id = (
                session.query(product_table).filter_by(code=item["code"]).first().id
            )
        except Exception:
            print(f"Could not find ranked product: {item['code']}")
            session.close()

        # check whether the product already exists in db
        existing_product = (
            session.query(ranked_product_table)
            .filter(
                (ranked_product_table.product_id == ranked_product.product_id)
                & (ranked_product_table.category == ranked_product.category)
            )
            .first()
        )
        if existing_product is not None:  # the current product exists
            time_between_insertion = datetime.now() - existing_product.time_stamp
            # Check if current ranking is over 24hours old
            if time_between_insertion.days > 1:
                try:
                    session.add(ranked_product)
                    session.commit()

                except Exception:
                    session.rollback()
                    raise

                finally:
                    session.close()

            else:
                logging.log(
                    logging.INFO,
                    f"Duplicate ranked product with code {item['code']} and category: {item['category']} less than 24hours old, no update was made.",
                )
                # logging.log(
                #     logging.INFO,
                #     f"Duplicate ranked product item found with code: {item['code']} and category: {item['category']}",
                # )
                session.close()

        else:
            try:
                session.add(ranked_product)
                session.commit()

            except Exception:
                session.rollback()
                raise

            finally:
                session.close()

        return item
