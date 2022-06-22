# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals, Request
from scrapy.http import HtmlResponse

from utils import create_chrome_driver
# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


def get_cookies_dict():
    cookies_str = 'douban-fav-remind=1; bid=XF3W6rbUkY8; ll="118282"; __gads=ID=ff66087e1a6652e7-226b6c35c8d30007:T=1654332316:RT=1654332316:S=ALNI_MZlj506o8F7EKWt2bimpHF-88PWIw; __utmz=30149280.1654334205.6.2.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1654334212.2.2.utmcsr=search.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/movie/subject_search; _vwo_uuid_v2=DE82AFF89F9900D2BC15F3E4555D5A24A|604d33fc8e65b267944d4b1a36399c6a; __gpi=UID=00000638241d1a33:T=1654332316:RT=1654993800:S=ALNI_MZd7az6fZIWRoSvPtclZGnXryRAGQ; dbcl2="257953901:qINO3RxS9LI"; push_doumail_num=0; push_noty_num=0; __utmv=30149280.25795; ck=sxVG; ap_v=0,6.0; _pk_ref.100001.4cf6=["","",1655909745,"https://search.douban.com/movie/subject_search?search_text=%E5%AE%8C%E7%BE%8E%E4%B8%96%E7%95%8C&cat=1002"]; _pk_id.100001.4cf6=1d0ff0ebb269b265.1654332281.9.1655909745.1655830919.; _pk_ses.100001.4cf6=*; __utma=30149280.450095316.1606837823.1655829298.1655909745.14; __utmb=30149280.0.10.1655909745; __utmc=30149280; __utma=223695111.1207910581.1654332281.1655829298.1655909745.9; __utmb=223695111.0.10.1655909745; __utmc=223695111'
    cookies_dict = {}
    for item in cookies_str.split(";"):
        key, value = item.split("=", maxsplit=1)
        cookies_dict[key] = value
    return cookies_dict


COOKIES_DICT = get_cookies_dict()


class Spider2022SpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class Spider2022DownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    # def __init__(self):
    #     self.brower = create_chrome_driver()

    # def __del__(self):
    #     self.brower.close()
    def process_request(self, request: Request, spider):
        # Called for each request that goes through the downloader
        # middleware.
        # 添加代理
        # request.meta = {"proxy": ""}

        request.cookies = COOKIES_DICT
        # self.brower.get(request.url)
        # return HtmlResponse(url=request.url, body=self.brower.page_source, request=request, encoding='utf-8')
        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
