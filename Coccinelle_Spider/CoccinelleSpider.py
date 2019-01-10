"""This spider is used to scrape products and their details from
http://www.coccinelle.com/en
"""

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from coccinelle_crawler.items import Product


class CoccinelleSpider(CrawlSpider):
    name = 'CoccinelleSpider'
    allowed_domains = ['coccinelle.com']
    start_urls = ['http://www.coccinelle.com/en']

    ids_seen = set()

    homepage_urls_css = ['.b-menu_category-level_2-link', '[rel="next"]']
    homepage_tags_css = ('link', 'a')
    product_urls_css = '.js-producttile_link.b-product_image-wrapper'

    rules = (
        Rule(LinkExtractor(restrict_css=homepage_urls_css, tags=homepage_tags_css)),
        Rule(LinkExtractor(restrict_css=product_urls_css),callback='parse_product_details'),
    )

    def parse_product_name(self, response):
        return response.css('span.b-product_name::text').extract_first()

    def parse_product_code(self, response):
        code = response.css('div.b-product_master_id::text').extract_first().replace('Code:', '').strip()
        if code in self.ids_seen:
            raise DropItem(f'Duplicate product found: {code}')
        else:
            self.ids_seen.add(code)
            return code

    def parse_product_sizes(self, response):
        return response.css('ul.js-tab_product_set-cont.tabs_product_set li a::text').extract() or ['One size']

    def parse_product_colors(self, response):
        return response.css('a.b-swatches_color-link::attr(title)').extract() or ['N/A']

    def parse_product_price(self, response):
        return response.css('h4::text').extract_first().replace('€', '').strip()

    def parse_product_description(self, response):
        return response.css('div.b-product_long_description::text').extract_first().strip()

    def parse_product_material(self, response):
        return response.css('div.b-product_material::text').extract_first().strip()

    def parse_product_care_details(self, response):
        return response.css('div.b-care_details-content.js-care_details-content::text').extract()[1:]

    def parse_product_image_urls(self, response):
        return response.css('img.js-producttile_image::attr(data-src)').extract()

    def parse_product_details(self, response):
        product = Product()
        product['name'] = self.parse_product_name(response)
        product['code'] = self.parse_product_code(response)
        product['sizes'] = self.parse_product_sizes(response)
        product['colors'] = self.parse_product_colors(response)
        product['price'] = self.parse_product_price(response)
        product['description'] = self.parse_product_description(response)
        product['material'] = self.parse_product_material(response)
        product['care_details'] = self.parse_product_care_details(response)
        product['image_urls'] = self.parse_product_image_urls(response)

        return product
