from scrapy import Item, Field

# from dataclasses import dataclass
# from decimal import Decimal


# TODO: Convert to dataclass and use data validators
# @dataclass
class ProductItem(Item):
    code = Field()
    brand = Field()
    product_name = Field()
    variant = Field()
    retail_price = Field()
    on_sale = Field()
    current_price = Field()
    in_stock = Field()
    product_url = Field()
    # __slots__ = [
    #     "id",
    #     "brand",
    #     "product_name",
    #     "variant",
    #     "retail_price",
    #     "on_sale",
    #     "current_price",
    #     "in_stock",
    #     "product_url",
    # ]
    # id: str
    # brand: str
    # product_name: str
    # variant: str
    # retail_price: Decimal
    # on_sale: bool
    # current_price: Decimal
    # in_stock: bool
    # product_url: str


class RankedProductItem(Item):
    code = Field()
    category = Field()
    ranking = Field()
    rating = Field()
    review_count = Field()
    filter = Field()
    name = Field()


class BrandItem(Item):
    name = Field()
    url = Field()


# class ProductPriceItem(Item):
#     product_id = Field()
#     time_stamp = Field()
#     retail_price = Field()
#     on_sale = Field()
#     current_price = Field()
#     in_stock = Field()
