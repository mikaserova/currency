import selenium_task.currency_scrapper as cs 
from selenium_task.optimization import CurrencyOpt as co
from flask import  request
from flask import Flask
import logging
import sys 
#import requests
from datetime import datetime
import time
#import argparse
from apscheduler.scheduler import Scheduler
from crontab import CronTab
app = Flask(__name__)
logging.basicConfig(filename='scrapper_app.log', filemode='w', format='%(message)s')
def process():
    arr=cs.CurrencyStatistic.initialise_banks()
    res=cs.CurrencyStatistic.process(arr)
    cs.CurrencyStatistic.writeDB(res)
    return res
def monthly_update():
    co.calculateTotal(weeks=0, months=1,buck="currency_monthly")
@app.route('/', methods=["POST","GET"])
def index():
   
    ##parser = argparse.ArgumentParser(description='Get currency rate from bank sites')
    #parser.add_argument('-f',dest='file_name', default='flask_task/stat.json', help="Set the name of a file, where statistic data will be saved")
##parser.add_argument('-t', dest='time',default='0 10 * * *',help='set time when to start execution in cron format')
    #parser.add_argument('-del', dest='del',default='0 10 * * *',help='set time when to start execution in cron format')
    #cron=CronTab(user=True)
   ## result=parser.parse_args()
    print("SCRAPPER STARTED")
    result = request.get_json(force=True)
    #result=result['data']
    print("RESULT:", result)
    # # j1=cron.find_command('/scrapper_v2/cr.py')
    # # if j1==None:
    # #     j=cron.new(command=' /usr/local/bin/f2py3.6  /scrapper_v2/cr.py  ', comment="job for currency scrapper")
    # #     j.setall(result.time)
    # # else:
    # #     for item in j1:
    # #         item.setall(result.time)
    # # cron.write()
    # # res = process()
    
    scheduler = Scheduler()
    scheduler.start()
    logging.debug('Scheduler started : ', scheduler.running)
    scheduler.add_cron_job(co.calculateTotal, minute="*", hour="*", day="*",month="*", day_of_week="2"),  
    sys.stdout.write('Scheduler started : ', scheduler.running)
    scheduler.add_cron_job(monthly_update, day="last", hour=23,minute=55) 
    sys.stdout.write(" CRON JOBS: ", scheduler.get_jobs())
    if result:
        times=result['time'].split()
        scheduler.add_cron_job(process, minute=times[0], hour=times[1], day=times[2],month=times[3], day_of_week=times[4] )
    
    # try:
    #     # This is here to simulate application activity (which keeps the main thread alive).
    #     while True:
    #         time.sleep(t-1)
    # except (KeyboardInterrupt, SystemExit):
    #     # Not strictly necessary if daemonic mode is enabled but should be done if possible
    #     scheduler.shutdown() 
    return result