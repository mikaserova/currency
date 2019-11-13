import selenium_task.scrapper as scrapper
import json
import os
import time
from datetime import datetime, date, timedelta

from couchbase.exceptions import CouchbaseError
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
class Bank(object):
    def __init__(self,name, url, tags,tag_type):
        self.bank_name=name
        self.url=url
        self.tag_set=tags
        self.tag_type=tag_type

       
class CurrencyStatistic(object):
    @staticmethod
    def initialise_banks():
        bank_arr=[]
        tags=["EUR_buy","EUR_sell","USD_buy","USD_sell","RUB_buy","RUB_sell"]
        b=Bank("Privat","https://privatbank.ua/",tags,"id")
        bank_arr.append(b)
        tags=["buy-EUR","sell-EUR","buy-USD","sell-USD","buy-RUB","sell-RUB"]
        b=Bank("Oschad","https://www.oschadbank.ua/ua", tags,"class")
        bank_arr.append(b)
        tags=["rate-numbers-eur","rate-numbers-usd","rate-numbers-rub"]
        b=Bank("Aval","https://www.aval.ua", tags,"select")
        bank_arr.append(b)
        return bank_arr
        
    @staticmethod
    def process(banks):
        res={}
        s=scrapper.WebScrapper()
        for b in banks:
            if b.tag_type=='id':
                r=s.getDataByID(b.url,b.tag_set)
            elif b.tag_type=='class':
                r=s.getDataByClass(b.url,b.tag_set)
            elif b.tag_type=='select':
                r=s.getDataBySelect(b.url,b.tag_set)
                time.sleep(5)
            res[b.bank_name]=r
        s.finalize()
        return res

    @staticmethod
    def writeJSON(name,data):
        now = datetime.now()
        curr_time=now.strftime("%Y/%m/%d")
        res={curr_time:data}
        feeds={}
        if not os.path.isfile(name):
        
            with open(name,'a+')as file:
               json.dump(res,file, indent=4)
        else:
            with open(name)as file:
                feeds=json.load(file)
                feeds[curr_time]=data
            with open(name,'w') as file:
                json.dump(feeds,file, indent=4)

    @staticmethod # TODO test
    def writeDB(data):
        now = datetime.now()
        curr_time=now.strftime("%Y/%m/%d")
        #res={curr_time:data}
        cluster = Cluster('http://cdb:8091')
        authenticator = PasswordAuthenticator('sashasierova', '4esZXdr5')
        cluster.authenticate(authenticator)
        bucket = cluster.open_bucket('currency_rate')
        bucket.upsert(curr_time, data)
    

         
        