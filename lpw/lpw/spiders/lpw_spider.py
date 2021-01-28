# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders.crawl import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from ..items import LpwItem

class LpwSpider(CrawlSpider):
    name = 'lpw_spider'
    allowed_domains = ['liepin.com']
    start_urls = ['https://www.liepin.com/zhaopin/?key=python']
    #定义URL规则：对页面内职位URL进行爬取，并进行回调，不继续跟进；翻页URL爬取，并进行跟进。
    rules= {
        #页内爬取规则
        Rule(LinkExtractor(allow=r'https://www.liepin.com/job/\d+\.shtml.*',restrict_xpaths = ['//ul[@class="sojob-list"]//a']),callback = 'parse_job',follow = False),
        #翻页爬取规则
        Rule(LinkExtractor(allow=r'/zhaopin/.+curPage=\d+',restrict_xpaths=['//div[@class="pagerbar"]//a']),follow=True)
    }


    # 获取主要爬取信息并传递给items
    def parse_job(self, response):
        title = response.css(".title-info h1::text").get()
        company = response.css(".title-info h3 a::text").get()
        city = response.css(".basic-infor span a::text").get()
        education = response.css(".job-qualifications span:nth-child(1)::text").get()
        experience = response.css(".job-qualifications span:nth-child(2)::text").get()
        des = response.css(".content-word::text").getall()
        descript = "".join(des).strip()
        item = LpwItem(title=title,company=company,city=city,education=education,experience=experience,descript=descript)
        #print(item)
        yield item




