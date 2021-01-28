# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LpwItem(scrapy.Item):
    title = scrapy.Field()
    company = scrapy.Field()
    city = scrapy.Field()
    education = scrapy.Field()
    experience = scrapy.Field()
    descript = scrapy.Field()

