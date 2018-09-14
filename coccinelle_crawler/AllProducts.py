"""This spider is used to scrape products and their details from
http://www.coccinelle.com/en
"""
import re

import scrapy

from coccinelle_crawler.items import Product
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class AllproductsSpider(CrawlSpider):
    name = 'AllProducts'
    allowed_domains = ['coccinelle.com']
    start_urls = ['http://www.coccinelle.com/en']

    rules = (
        Rule(LinkExtractor(restrict_css=('.b-menu_category-level_2-link'))),
        Rule(LinkExtractor(restrict_css=(
        '.js-producttile_link.b-product_image-wrapper'
        )), callback='parse_product_details'),
    )

    def parse_product_details(self, response):
        product = Product()
        product['name'] = response.css(
        'span.b-product_name::text').extract_first()
        product['code'] = response.css(
        'div.b-product_master_id::text').extract_first()[7:-1]
        product['sizes'] = response.css(
        'ul.js-tab_product_set-cont.tabs_product_set li a::text'
        ).extract() or 'One size'
        product['colors'] = response.css(
        'a.b-swatches_color-link::attr(title)').extract() or 'N/A'
        product['price'] = response.css('h4::text').extract_first()[2:]
        product['description'] = response.css(
        'div.b-product_material::text').extract_first()[1:-1]
        product['material'] = response.css(
        'div.b-product_material::text').extract_first()[1:-1]
        product['care_details'] = response.css(
        'div.b-care_details-content.js-care_details-content::text'
        ).extract()[1:]
        product['image_URLs'] = response.css(
        'img.js-producttile_image::attr(data-src)').extract()

        return product
