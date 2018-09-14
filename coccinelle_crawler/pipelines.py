from scrapy.exceptions import DropItem


class RemoveDuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['code'] in self.ids_seen:
            raise DropItem(f'Duplicate product found: {code}')
        else:
            self.ids_seen.add(item['code'])
            return item
