from scrapy.item import Item, Field


class Product(Item):

    name = Field()
    code = Field()
    sizes = Field()
    colors = Field()
    price = Field()
    description = Field()
    material = Field()
    care_details = Field()
    image_urls = Field()
