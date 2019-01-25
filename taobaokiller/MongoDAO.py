# -*- coding: utf-8 -*-
import pymongo

client = pymongo.MongoClient(host='localhost',port=27017)

taobaoDB=client.TaoBaoDB
shalouCol = taobaoDB.ShaLou

shalou ={
    'name':'Timer时光',
    'link':'http://wwww.abc.com',
    'price':'333',
    'sells':'488',
    'shop_name':'HelloShalow'
}

result = shalouCol.insert(shalou)
print(result)
