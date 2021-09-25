from items import BrandItem, ProductItem, RankedProductItem
import string

# from sqlalchemy.ext.declarative import DeclarativeMeta
from scrapy import Spider
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
import logging
from datetime import datetime
from models import (
    create_table,
    db_connect,
    NLBrand,
    FFBrand,
    WMBrand,
    NLProduct,
    FFProduct,
    WMProduct,
    NLCurrentPrice,
    FFCurrentPrice,
    WMCurrentPrice,
    NLHistoricalPrice,
    FFHistoricalPrice,
    WMHistoricalPrice,
    NLBestSelling,
    FFBestSelling,
    NLHighestRated,
    FFHighestRated,
)


class StoreBrandsPipeline(object):
    def __init__(self):
        """Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item: BrandItem, spider: Spider) -> BrandItem:
        """Save NL/FF Brands in the database
        This method is called for NL and FF Brand Items
        """
        session = self.Session()

        brand_table, brand = (
            (NLBrand, NLBrand())
            if spider.name == "nl_brands"
            else (FFBrand, FFBrand())
            if spider.name == "ff_brands"
            else (WMBrand, WMBrand())
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
                except:
                    session.rollback()
                    raise

            else:
                logging.log(logging.INFO, f"Duplicate brand item found: {item['name']}")
                session.close()
        else:
            try:
                session.add(brand)
                session.commit()

            except:
                session.rollback()
                raise

            finally:
                session.close()

        return item


class StoreProductsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item: ProductItem, spider: Spider) -> ProductItem:
        """Save products in the database
        This method is called for every Product Item pipeline component
        """

        session = self.Session()

        product_table, product, brand_table = (
            (NLProduct, NLProduct(), NLBrand)
            if spider.name == "nl_products"
            else (FFProduct, FFProduct(), FFBrand)
            if spider.name == "ff_products"
            else (WMProduct, WMProduct(), WMBrand)
        )

        product.code = item["code"]
        product.name = item["product_name"]
        try:
            product.brand_id = (
                session.query(brand_table).filter_by(name=item["brand"]).first().id
            )
        except AttributeError:
            print(f"brand_id: {product.brand_id}")
            # print(
            #     f"brand: {item['brand']}\t prod_table: {product_table}\t prod: {product}\t brand_table: {brand_table}"
            # )
        if product.brand_id is None:
            filtered_brand = item["brand"].translate(
                str.maketrans("", "", string.punctuation)
            )
            print(
                f"brand: {item['brand']}\t prod_table: {product_table}\t prod: {product}\t brand_table: {brand_table}"
            )
            first_letter = item["brand"][0]
            potential_brands = [brand.name for brand in 
                session.query(brand_table)
                .filter(brand_table.name.like(first_letter + "%"))
                .all()
            ]
            filtered_potential_brands = [
                brand.translate(str.maketrans("", "", string.punctuation))
                for brand in potential_brands
            ]
            for idx, brand in enumerate(filtered_potential_brands):
                if filtered_brand == brand:
                    product.brand_id = (
                        session.query(brand_table)
                        .filter_by(name=potential_brands[idx])
                        .first()
                        .id
                    )
                print(f"\nBRAND FOUND: {product.brand_id} \n")

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
            # print(f"Duplicate product item found: {item['product_name']}")
            # logging.log(
            #     logging.INFO,
            #     f"Duplicate product item found: {item['product_name']}",
            # )
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


class StoreRankedProductsPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates tables
        """
        engine = db_connect()
        create_table(engine)
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
            print(
                f"ranked_table: {ranked_product_table}\t ranked_product: {ranked_product}\t prod_table: {product_table}"
            )

        # check whether the product already exists in db
        existing_product = (
            session.query(ranked_product_table)
            .filter_by(product_id=ranked_product.product_id)
            .first()
        )
        if existing_product is not None:  # the current product exists
            logging.log(
                logging.INFO,
                f"Duplicate ranked product item found with code: {item['code']}",
            )
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
