import scrapy
from scrapy import Selector,Request
from scrapy.http import HtmlResponse

from spider2022.items import MovieItem


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        for page in range(10):
            yield Request(url=f'https://movie.douban.com/top250?start={page*25}&filter=')

    def parse(self, response: HtmlResponse):
        # 通过selector包裹成一个选择器对象
        sel = Selector(response)
        # el.xpath
        # 取得单一元素值呼叫get（）方法/取得多个元素值呼叫getall（）方法/取得文字内容，加上「/ text（）」关键字/取得属性值则加上「@属性名称」关键字
        #  sel.css
        # sel.re
        list_items = sel.css('#content > div > div.article > ol > li')
        for list_item in list_items:
            movie_item = MovieItem()
            # ::text：获取文本信息，extract：将解析器列表转化为为字符串数组，extract_first()：获取解析器列表的第一条数据
            movie_item['title'] = list_item.css('span.title::text').extract_first()
            movie_item['rating'] = list_item.css('span.rating_num::text').extract_first()
            movie_item['subject'] = list_item.css('span.inq::text').extract_first()
            yield movie_item
        # href_list = sel.css('div.paginator > a::attr(href)')
        # for href in href_list:
        #     url = response.urljoin(href.extract())
        #     yield Request(url=url)
        #     print(url)
        # pass
