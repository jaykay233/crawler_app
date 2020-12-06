import scrapy
from wandoujia.items import WandoujiaItem
from urllib.parse import quote
import string
import logging
from lxml import etree


class WandoujiaSpider(scrapy.Spider):
    name = 'wandoujia_spider'
    allowed_domains = ['wandoujia.com','zhushou.360.cn']
    base_url = 'http://zhushou.360.cn/search/index/?kw='
    base_website='http://zhushou.360.cn'

    def start_requests(self):
        app_file = '/Users/xuzhiyuan/PycharmProjects/crawler/wandoujia/wandoujia/spiders/app'
        with open(app_file, 'r') as f:
            for line in f.readlines():
                line = line.replace('\n', '')
                url_encode = quote(self.base_url + line, safe=string.printable)
                logging.info(url_encode)
                yield scrapy.Request(url=url_encode, callback=self.parse, meta={'app_name': line})

    def parse(self, response, **kwargs):
        app_name = response.meta['app_name']
        # print(app_name)
        # print(response.body)
        r = response.xpath('//h3/a/@href')
        # logging.warning(str(len(r)))
        for element in r:
            links = element.extract()
            links = self.base_website + links
            links_encode = quote(links, safe=string.printable)
            logging.warning(links_encode)
            yield scrapy.Request(url=links_encode, callback=self.parse2, meta={'app_name': app_name})

    def parse2(self, response):
        item = WandoujiaItem()
        app_name = response.meta['app_name']
        item['app_name'] = app_name
        logging.warning(app_name)
        r = response.xpath('//div[@class="app-tags"]/a/text()')
        logging.warning(len(r))
        cate = []
        for element in r:
            cate.append(element.extract())
        category = ','.join(cate)
        if len(category):
            print(app_name + '\t' + category)
            item['category'] = category
            yield item
