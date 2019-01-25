# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaokillerItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pic_url = scrapy.Field()
    link = scrapy.Field()
    price = scrapy.Field()
    sells = scrapy.Field()
    shop_name = scrapy.Field()
    item_type = scrapy.Field()


