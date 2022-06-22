import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from spider2022.items import MovieItem


class DoubanSpider(scrapy.Spider):
    # name：标识蜘蛛，一个项目只能有一个name，不能为不同的爬取器设置不同的name
    name = 'douban'
    # 合法域名列表
    allowed_domains = ['movie.douban.com']

    # 爬行器将从该请求开始爬行，后续请求将从这些初始请求相继生成
    def start_requests(self):
        for page in range(10):
            # # yield将结果返回给解析器，并且不会停止循环
            # 配置socks代理
            yield Request(url=f'https://movie.douban.com/top250?start={page * 25}&filter=')

    # 将被调用以用来处理每个请求响应的方法（相同的链接会被自动跳过）
    def parse(self, response: HtmlResponse):
        # 通过selector包裹成一个选择器对象
        sel = Selector(response)
        # el.xpath
        # 取得单一元素值呼叫get（）方法/取得多个元素值呼叫getall（）方法/取得文字内容，加上「/ text（）」关键字/取得属性值则加上「@属性名称」关键字
        #  sel.css
        # sel.re
        # list_items = sel.css('#content > div > div.article > ol > li')
        list_items = response.xpath('//div[@id="content"]//div[@class="article"]/ol/li')
        for list_item in list_items:
            movie_item = MovieItem()
            try:
                detail_url = list_item.xpath('.//div[@class="hd"]/a/@href').extract()[0] or ''
                # detail_url = list_item.css("div.info>div.hd>a::attr(href)").extract_first()
                # ::text：获取文本信息，extract：将解析器列表转化为为字符串数组，extract_first()：获取解析器列表的第一条数据
                # movie_item['title'] = list_item.css('span.title::text').extract_first()
                movie_item['title'] = list_item.xpath('.//span[@class="title"]/text()').extract()[0] or ''
                # movie_item['rating'] = list_item.css('span.rating_num::text').extract_first()
                movie_item['rating'] = list_item.xpath('.//span[@class="rating_num"]/text()').extract()[0] or ''
                movie_item['subject'] = list_item.xpath('.//span[@class="inq"]/text()').extract()[0] or ''
                # movie_item['subject'] = list_item.css('span.inq::text').extract_first()
            except Exception as e:
                print("e")
            yield Request(url=detail_url, callback=self.parse_detail,cb_kwargs={'item':movie_item})

        # href_list = sel.css('div.paginator > a::attr(href)')
        href_list = response.xpath('//div[@class="paginator"]/a/@href')
        for href in href_list:
            # urljoin：将相对路径变成绝对路径
            url = response.urljoin(href.extract())
            yield Request(url=url)
            # print(url)
        # pass

    def parse_detail(self, response: HtmlResponse,**kwargs):
        movie_item = kwargs['item']
        movie_item['durating'] = response.xpath('.//span[@property="v:runtime"]/text()').extract()[0] or ''
        movie_item['intro'] = response.xpath('.//span[@property="v:summary"]/text()').extract()[0] or ''
        return print(movie_item)
        yield movie_item
        pass
