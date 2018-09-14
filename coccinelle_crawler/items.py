import scrapy


class Product(scrapy.Item):

    name = scrapy.Field()
    code = scrapy.Field()
    sizes = scrapy.Field()
    colors = scrapy.Field()
    price = scrapy.Field()
    description = scrapy.Field()
    material = scrapy.Field()
    care_details = scrapy.Field()
    image_URLs = scrapy.Field()
