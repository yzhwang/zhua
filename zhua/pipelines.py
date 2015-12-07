# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from scrapy.exporters import JsonLinesItemExporter

class ZhuaPipeline(object):

    def __init__(self):
        self.files = {}

	@classmethod
	def from_crawler(cls, crawler):
		pipeline = cls()
		crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
		crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
		return pipeline

    def open_spider(self, spider):
		name = '%s_products.json' % spider.name
		self.file  = open(name, 'w+b')
		self.exporter = JsonLinesItemExporter(self.file)
		self.exporter.start_exporting()

    def close_spider(self, spider):
		self.exporter.finish_exporting()
		self.file.close()

    def process_item(self, item, spider):
		self.exporter.export_item(item)
		return item
