from selenium import webdriver
import re
class WebScrapper(object):
    tags=["EUR_buy","EUR_sell","USD_buy","USD_sell","RUB_buy","RUB_sell"]
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        self.driver=webdriver.Chrome(chrome_options=chrome_options)

    def getDataByID(self,loc, ids):
        self.driver.get(loc)
        result={}
        j=0
        for i in ids:
            elem=self.driver.find_element_by_id(i)
            result[WebScrapper.tags[j]]=elem.text
            j+=1
        return result

  
    def getDataByClass(self,loc, classes):
        self.driver.get(loc)
        result={}
        i=0
        for c in classes:
            elem=self.driver.find_element_by_class_name(c)
            result[WebScrapper.tags[i]]=elem.text
            i+=1
        return result
        
    def getDataBySelect(self,loc, classes):
        self.driver.get(loc)
        result={}
        i=0
        for c in classes:
            elem=self.driver.find_element_by_class_name(c)
            t=self.driver.execute_script("return arguments[0].textContent",elem)
            t=re.sub('\n','',t).strip()
         
            d=re.findall('\d+\.\d+',t)
            result[WebScrapper.tags[i]]=d[0]
            i+=1
            result[WebScrapper.tags[i]]=d[1]
            i+=1
        return result       
    def finalize(self):
        self.driver.close()