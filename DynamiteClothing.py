import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from dynamiteclothing.items import Product


class DynamiteclothingSpider(CrawlSpider):
    name = 'DynamiteClothing'
    allowed_domains = ['www.dynamiteclothing.com']

    rules = (
        Rule(LinkExtractor(restrict_css=[
            '.subcategory.subCatLink', '#catPageNext'])),
        Rule(LinkExtractor(
            restrict_css='[title="View Product Details"]'),
            callback='parse_product')
    )

    def start_requests(self):
        yield scrapy.Request(
            'https://www.dynamiteclothing.com/us/profile/login.jsp?h=true',
            callback=self.generate_login_request)

    def generate_login_request(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formid='loginForm',
            formdata={
                'loginEmail': 'zain@gmail.com',
                '/atg/userprofiling/ProfileFormHandler.value.password': 'ABc123'},
            callback=self.after_login
        )

    def after_login(self, response):
        if response.css('[href*="profile.jsp"]::attr(href)').extract_first():
            yield scrapy.Request('https://www.dynamiteclothing.com/us?li=true',
                                 callback=self.parse)
        else:
            self.logger.error('Login failed')
            return

    def parse_product(self, response):
        product = Product()
        product['name'] = response.css(
            '.prodName::text').extract_first().strip()
        product['prod_id'] = response.css(
            '#productId::attr(value)').extract_first()
        product['price'] = response.css(
            '.prodPricePDP::text, .salePrice::text').re_first('\S+')
        product['sale_price'] = response.css(
            '.withSale::text').extract_first('N/A').strip()
        product['colors'] = response.css(
            '.swatchColor::text').extract_first().strip()
        product['sizes'] = response.css('#productSizes span::text').extract()
        product['description'] = response.css(
            '#descTab0Content p::text, #descTabDescriptionContent p::text'
        ).extract_first().replace('\u00a0', '')
        details_with_problems = response.css(
            '#descTabDetailsContent li::text, #descTab0Content li::text, #descTabDescriptionContent li::text'
        ).extract()
        details = []
        for each_detail in details_with_problems:
            details.append(each_detail.replace('\u00a0', ' ').strip())
        product['details'] = details
        product['img_URLs'] = response.css('a::attr(data-zoom)').extract()

        return product
