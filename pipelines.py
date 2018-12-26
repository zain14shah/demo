from scrapy.exceptions import DropItem


class RemoveDuplicatesPipeline(object):
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        if item['prod_id'] in self.ids_seen:
            raise DropItem(f'Duplicate product found: {prod_id}')
        else:
            self.ids_seen.add(item['prod_id'])
            return item
