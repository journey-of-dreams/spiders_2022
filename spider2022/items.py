# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    # define the fields for your item here like:
    # #Field()：携带存储元数据
    # name = scrapy.Field()
    title = scrapy.Field()
    rating = scrapy.Field()
    subject = scrapy.Field()
    durating = scrapy.Field()
    intro = scrapy.Field()
    pass
