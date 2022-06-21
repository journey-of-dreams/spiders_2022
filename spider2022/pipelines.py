# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import pymysql

class DbPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', db='zdsc', charset='utf8')
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
        self.data.append((title,rating,subject))
        if len(self.data) == 100:
            self._write_to_db()
            self.data.clear()
        return item

    def _write_to_db(self):
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
        self.sheet.append(("标题", "评分", "主题"))

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
        print(title, rating, subject)
        self.sheet.append((title, rating, subject))
        # 返回item给其他需要的函数用
        return item
