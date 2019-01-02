"""This spider extracts the prayer timings from the given URL with reference to
the prayer names and city names.
"""
import scrapy


class PrayersTimingsSpider(scrapy.Spider):
    name = 'prayers_timings'

    start_urls = [
        'https://www.dawn.com/prayers-timings'
    ]

    def parse(self, response):
        prayer_names = response.xpath(
            '//table[@class ="table  table-bordered table-striped"]//th/text()'
        ).extract()[1:]

        for prayer_data in response.xpath('//tr[@class ="text-center"]'):
            city_name = prayer_data.xpath(
                './/td/strong/text()'
            ).extract_first()
            all_prayer_timings = prayer_data.xpath('.//td/text()').extract()

            prayer_timings = {}
            for index, name in enumerate(prayer_names):
                prayer_timings[name] = all_prayer_timings[index]
            yield {city_name: prayer_timings}
