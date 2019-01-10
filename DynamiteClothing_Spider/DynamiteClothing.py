"""This spider is used to scrape products and their details from
https://www.dynamiteclothing.com/us
"""

from scrapy import FormRequest
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from dynamiteclothing.items import Product
from scrapy.exceptions import DropItem


class DynamiteclothingSpider(CrawlSpider):
    name = 'DynamiteClothing'
    allowed_domains = ['www.dynamiteclothing.com']
    start_urls = [
        'https://www.dynamiteclothing.com/us/profile/login.jsp?h=true']

    ids_seen = set()
    homepage_urls_css = ['.subcategory.subCatLink', '#catPageNext']
    product_urls_css = '[title="View Product Details"]'
    rules = (
        Rule(LinkExtractor(restrict_css=homepage_urls_css)),
        Rule(LinkExtractor(restrict_css=product_urls_css), callback='parse_product')
    )

    def parse_start_url(self, response):
        return FormRequest.from_response(
            response,
            formid='loginForm',
            formdata={
                'loginEmail': 'zain@gmail.com',
                '/atg/userprofiling/ProfileFormHandler.value.password': 'ABc123'},
            callback=self.parse_check_login
        )

    def parse_check_login(self, response):
        if response.css('[href*="profile.jsp"]::attr(href)').extract_first():
            yield response.follow('us?li=true', callback=self.parse)
        else:
            self.logger.error('Login failed')
            return

    def parse_product_name(self, response):
        return response.css('.prodName::text').extract_first().strip()

    def parse_product_id(self, response):
        id = response.css('#productId::attr(value)').extract_first()
        if id in self.ids_seen:
            raise DropItem(f'Duplicate product found: {id}')
        else:
            self.ids_seen.add(id)
            return id

    def parse_product_price(self, response):
        return response.css('.prodPricePDP::text, .salePrice::text').re_first('\S+')

    def parse_product_sale_price(self, response):
        return response.css('.withSale::text').extract_first('N/A').strip()

    def parse_product_colors(self, response):
        return response.css('.swatchColor::text').extract_first().strip()

    def parse_product_sizes(self, response):
        return response.css('#productSizes span::text').extract()

    def parse_product_description(self, response):
        return response.css(
            '#descTab0Content p::text, #descTabDescriptionContent p::text'
        ).extract_first().replace('\u00a0', '')

    def parse_product_details(self, response):
        details_with_problems = response.css(
            '#descTabDetailsContent li::text, #descTab0Content li::text, #descTabDescriptionContent li::text'
        ).extract()
        return [
            each_detail.replace('\u00a0', ' ').strip()
            for each_detail in details_with_problems
        ]

    def parse_product_img_urls(self, response):
        return response.css('a::attr(data-zoom)').extract()

    def parse_product(self, response):
        product = Product()
        product['name'] = self.parse_product_name(response)
        product['id'] = self.parse_product_id(response)
        product['price'] = self.parse_product_price(response)
        product['sale_price'] = self.parse_product_sale_price(response)
        product['colors'] = self.parse_product_colors(response)
        product['sizes'] = self.parse_product_sizes(response)
        product['description'] = self.parse_product_description(response)
        product['details'] = self.parse_product_details(response)
        product['img_urls'] = self.parse_product_img_urls(response)

        return product
