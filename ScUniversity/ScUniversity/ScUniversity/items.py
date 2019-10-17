# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
#字段实体
import scrapy


# class ScuniversityItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

class ScUniversityItem(scrapy.Item):
    univername = scrapy.Field()               #高校名称(如:北京大学)
    univerlocadd = scrapy.Field()             #高校所在地(如:北京)
    univertype = scrapy.Field()               #高校类型(如:综合)
    univerproper = scrapy.Field()             #高校性质(如:本科)
    univerdist = scrapy.Field()               #高校特色(如:985、211)
    univerfrom = scrapy.Field()               #高校隶属(如:教育部)
    univerurl = scrapy.Field()                #学校网址(如:www.pku.edu.cn)