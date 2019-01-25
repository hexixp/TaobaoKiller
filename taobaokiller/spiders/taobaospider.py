# -*- coding: utf-8 -*-
import scrapy
from taobaokiller.items import TaobaokillerItem
from selenium import webdriver
from bs4 import BeautifulSoup as bs4
import time
import re
from taobaokiller.settings import *

import pymongo

class TaobaospiderSpider(scrapy.Spider):
    name = 'taobaospider'
    allowed_domains = ['www.taobao.com']
    start_url = 'https://s.taobao.com/search?q='+ KEY_WORDS
    client = pymongo.MongoClient(host='localhost', port=27017)
    taobaoDB = client.TaoBaoDB
    shalouCol = taobaoDB.ShaLou

    def start_requests(self):
        url_list = []
        for i in range(PAGES_NUM):
            url = self.start_url+'&s='+str(i*44)
            url_list.append(url)
        for url in url_list:
            print("--->",url)
            yield scrapy.Request(url=url,callback=self.parse)

    def url_decode(self,temp):
        while '\\' in temp:
            index = temp.find('\\')
            st = temp[index:index+7]
            temp = temp.replace(st,'')

        index = temp.find('id')
        temp = temp[:index+2]+'='+temp[index+2:]
        index =temp.find('ns')
        temp = temp[:index]+'&'+'ns='+temp[index+2:]
        index =temp.find('abbucket')
        temp ='https:'+temp[:index]+'&'+'abbucket='+temp[index+8:]
        return temp

    def pic_url_decode(self,temp):
        return 'https:'+temp

    def parse(self, response):
        taobao_item = TaobaokillerItem()
        item = response.xpath('//script/text()').extract()
        pat = '"raw_title":"(.*?)","pic_url":"(.*?)","detail_url":"(.*?)","view_price":"(.*?)","view_fee":".*?","item_loc":".*?","view_sales":"(.*?)","comment_count":".*?","nick":"(.*?)"'
        urls = re.findall(pat,str(item))
        if len(urls) ==0:
            print("Not found result")
            return

        urls.pop(0)

        row={}.fromkeys(['name','link','price','pic_url','sells','shop_name','item_type','create_date'])

        for url in urls:
            weburl = self.url_decode(temp=url[2])
            taobao_item['name']=url[0]
            taobao_item['link']=weburl
            taobao_item['price']=url[3]
            taobao_item['pic_url']=self.pic_url_decode(url[1])
            taobao_item['sells']=url[4][:-3]
            taobao_item['shop_name']=url[5]

            row['name'] = taobao_item['name']
            row['link'] = taobao_item['link']
            row['price'] = float(taobao_item['price'])
            row['pic_url'] = taobao_item['pic_url']
            row['sells'] = int(taobao_item['sells'])
            row['shop_name'] = taobao_item['shop_name']
            row['item_type'] = KEY_WORDS
            row['create_date'] =time.strftime('%Y%m%d%H%M%S')

            self.shalouCol.insert(row)
            row = {}.fromkeys(['name', 'link', 'price', 'pic_url', 'sells', 'shop_name','item_type','create_date'])
        print(taobao_item)




