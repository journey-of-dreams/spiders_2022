# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql
from scrapy.crawler import Crawler


class DbPipeline:
    def from_crawler(cls, crawler: Crawler):
        host = crawler.settings['DB_HOST']
        port = crawler.settings['DB_PORT']
        username = crawler.settings['DB_USER']
        password = crawler.settings['DB_PASS']
        database = crawler.settings['DB_NAME']
        return cls(host, port, username, password, database)

    def __init__(self, host, port, username, password, database):
        self.conn = pymysql.connect(host=host, port=port, user=username, passwd=password, db=database,
                                    charset='utf8mb4', autocommit=True)
        self.cursor = self.conn.cursor()
        self.data = []
        pass

    def close_spider(self, spider):
        if len(self.data) > 0:
            self.conn.commit()
        self.conn.close()
        pass

    def process_item(self, item, spider):
        # 字典通过get()拿值可以指定默认值，不至于拿不到时直接报错
        title = item.get("title", "")
        rating = item.get("rating", "")
        subject = item.get("subject", "")
        # 改成批量处理
        self.data.append((title, rating, subject))
        if len(self.data) == 100:
            self._write_to_db()
            self.data.clear()
        return item

    def _write_to_db(self):
        # decimal(3,1)
        self.cursor.executemany(
            f'insert into douban250(link,img_src,title,rating,judge_num,inq) values({self.data})'
        )
        self.conn.commit()


class ExcelPipeline:

    def __init__(self):
        self.wb = openpyxl.Workbook()
        # 拿到默认的工作表
        # self.sheet = self.wb.active
        # 创建新工作表
        self.sheet = self.wb.create_sheet("Top250")
        self.sheet.append(("标题", "评分", "主题", "时长", "简介"))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.wb.save("电影数据.xlsx")

    # 处理数据的方法(声明周期函数，自动调用)
    def process_item(self, item, spider):
        # 字典通过get()拿值可以指定默认值，不至于拿不到时直接报错
        title = item.get("title", "")
        rating = item.get("rating", "")
        subject = item.get("subject", "")
        durating = item.get("durating", "")
        intro = item.get("intro", "")
        print(title, rating, subject)
        self.sheet.append((title, rating, subject, durating, intro))
        # 返回item给其他需要的函数用
        return item
