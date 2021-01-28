# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from twisted.enterprise import adbapi        #导入adbapi

class LpwPipeline(object):
    def __init__(self,mysql_config):
        self.dbpool = adbapi.ConnectionPool(
        #创建一个数据库连接池对象，其中包括多个连接对象，每个连接对象在独立的线程中工作
        mysql_config['DRIVER'],
        host=mysql_config['HOST'],
        port=mysql_config['PORT'],
        user=mysql_config['USER'],
        password=mysql_config['PASSWORD'],
        db=mysql_config['DATABASE'],
        charset='utf8'
)
    @classmethod
    #从settings中读取数据库配置
    def from_crawler(cls, crawler):
        mysql_config = crawler.settings['MYSQL_CONFIG']
        return cls(mysql_config)

    def process_item(self,item, spider):
    #以异步的方式调用insert_item函数，dbpool会选择连接池中的一个连接对象在独立线程中调用insert_item，其中参数item会被传给insert_item的第二个参数，传给insert_item的第一个参数是一个Transaction对象，其接口与Cursor对象类似，可以调用execute方法执行SQL语句，insert_item执行后，连接对象会自动调用commit方法
        result = self.dbpool.runInteraction(self.insert_item, item)
        return item

    # 定义一个输入sql语句，并执行sql语句的函数（由于在配置文件中加入了引擎标签，多以不需要再导入pymysql库）

    def insert_item(self,cursor,item):
        sql = "insert into spider_lpw(id,title,company,city,education,experience,descript) values(null,%s,%s,%s,%s,%s,%s)"
        args = (item['title'],
        item['company'], item['city'], item['education'], item['experience'], item['descript'])
        cursor.execute(sql,args)