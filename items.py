from scrapy.item import Item, Field


class Product(Item):
    name = Field()
    id = Field()
    price = Field()
    sale_price = Field()
    colors = Field()
    sizes = Field()
    description = Field()
    details = Field()
    img_urls = Field()
