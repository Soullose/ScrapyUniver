# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import uuid
import pymysql
from twisted.enterprise import adbapi
class ScuniversityPipeline(object):
    def process_item(self, item, spider):
        return item


class JsonEncoding(object):

    def __init__(self):
        self.File = codecs.open('univer.json','w',encoding='utf-8')


    def process(self,item,spider):
        univerItem = {}
        univerItem['ID'] = str(uuid.uuid5(uuid.NAMESPACE_DNS,item['univername']))
        univerItem['univerName'] = item['univername']
        univerItem['univerLocadd'] = item['univerlocadd']
        univerItem['univerType'] = item['univertype']
        univerItem['univerProper'] = item['univerproper']
        univerItem['univerDist'] = item['univerdist']
        univerItem['univerFrom'] = item['univerfrom']
        univerItem['univerUrl'] = item['univerurl']

        lines = json.dumps(dict(univerItem),ensure_ascii=False)+"\n"
        self.File.write(lines)

        return item

    def spider_close(self,spider):
        self.File.close()


class MysqlPipeline(object):
    """
    同步操作
    """

    def __init__(self):
        # 建立连接
        self.conn = pymysql.connect('localhost', 'root', '123456', 'scrapydata_qunar', charset='utf8')  # 有中文要存入数据库的话要加charset='utf8'
        # 创建游标
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # sql语句
        insert_sql = """
        insert into univer_info(id,univername,univerlocadd,univertype,univerproper,univerdist,univerfrom,univerurl) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
        """
        # 执行插入数据到数据库操作
        self.cursor.execute(insert_sql, (str(uuid.uuid5(uuid.NAMESPACE_DNS, item['univername'])), item['univername'], item['univerlocadd'],item['univertype'],item['univerproper'],item['univerdist'],item['univerfrom'],item['univerurl']))
        # 提交，不进行提交无法保存到数据库
        self.conn.commit()

    def close_spider(self, spider):
        # 关闭游标和连接
        self.cursor.close()
        self.conn.close()

class MysqlPipelineTwo(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):  # 函数名固定，会被scrapy调用，直接可用settings的值
        """
        数据库建立连接
        :param settings: 配置参数
        :return: 实例化参数
        """
        adbparams = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            password=settings['MYSQL_PASSWORD'],
            cursorclass=pymysql.cursors.DictCursor,  # 指定cursor类型
            charset='utf8'
        )
        # 连接数据池ConnectionPool，使用pymysql或者Mysqldb连接
        dbpool = adbapi.ConnectionPool('pymysql', **adbparams)
        # 返回实例化参数
        return cls(dbpool)

    def process_item(self, item, spider):
        """
        使用twisted将MySQL插入变成异步执行。通过连接池执行具体的sql操作，返回一个对象
        """
        query = self.dbpool.runInteraction(self.do_insert, item)  # 指定操作方法和操作数据
        # 添加异常处理
        query.addCallback(self.handle_error)  # 处理异常

    def do_insert(self, cursor, item):
        int(0)
        # 对数据库进行插入操作，并不需要commit，twisted会自动commit
        insert_sql = """
        insert into univer_info(id,univername,univerlocadd,univertype,univerproper,univerdist,univerfrom,univerurl) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
                    """
        cursor.execute(insert_sql, (str(uuid.uuid5(uuid.NAMESPACE_DNS, item['univername']))+item['univername'], item['univername'], item['univerlocadd'],item['univertype'],item['univerproper'],item['univerdist'],item['univerfrom'],item['univerurl']))

    def handle_error(self, failure):
        if failure:
            # 打印错误信息
            print(failure)