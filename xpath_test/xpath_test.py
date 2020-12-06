#coding:utf8
from lxml import etree

def parse(response):
    yield {'len':len(response.text)}

if __name__ == '__main__':
    tree=etree.parse('wanjoujia_test.html')
    r=tree.xpath('//ul[@class="app-box clearfix"]//li')
    for item in r:
        print(item.xpath('div/@id'))

    import scrapy
    r = scrapy.Request(url='https://www.wandoujia.com/search/14969806060801622287',callback=parse)
    print(r.headers)
