from dateutil.relativedelta import relativedelta
from datetime import datetime, date, timedelta
from couchbase.exceptions import CouchbaseError
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator
from couchbase.n1ql import N1QLQuery
import re
import statistics
class CurrencyOpt(object):
    @staticmethod
    def dbConnect(link='http://cdb:8091', buck='currency_rate'):#link changed must be cdb
        cluster = Cluster(link)
        print("CLUSTER:",cluster)
        authenticator = PasswordAuthenticator('sashasierova', '4esZXdr5')
        cluster.authenticate(authenticator)
        bucket = cluster.open_bucket(buck)
        return bucket 

    @staticmethod # TODO 
    def calculateTotal(buck="currency_weekly",weeks=1,months=0):
        td=date.today()
        st=td-relativedelta(weeks=weeks, months=months)
        st=re.sub('-','/',str(st))
        td=re.sub('-','/',str(td))

        from_bucket = CurrencyOpt.dbConnect()
        to_bucket = CurrencyOpt.dbConnect(buck=buck)
        print("ST",st)
        query = N1QLQuery("SELECT META().id, * FROM `currency_rate` WHERE META().id >$1", st)
        count = 0
        f=[]
        total=[]
        res=[]
        for i in range(18):
            total.append([])
        for row in from_bucket.n1ql_query(query):
                f.append(row['currency_rate'])
        print("F",f)
        for daily in f:
            i = 0
            for data in daily.items():
                for d in data[1].items():
                    
                    total[i].append(float(d[1]))
                    i+=1
        for i in range(len(total)):
            res.append(round(statistics.mean(total[i]),2))
        d=CurrencyOpt.make_dict(res)
        print("!!!!!!!!!")
        print (d)
        
        to_bucket.upsert(td,d)
        


        
    @staticmethod
    def make_dict(arr):
        curr_names=['EUR','USD','RUB']
        bank_names=['Privat', 'Oschad', 'Aval']
        temp = {}
        val=""
        for i in range(len(arr)):
            
            if i%6==0:
                temp[bank_names[i//6]]={}
            
            # val=curr_names[i//3]
            if i%2==0:
                val=curr_names[(i%6)//2]
                cur = val+"_buy"
            else:
                cur = val+"_sell"
            temp[bank_names[i//6]][cur]=arr[i]
        return temp

   
if __name__ == '__main__':
     CurrencyOpt.calculateTotal()
     CurrencyOpt.calculateTotal(weeks=0, months=1,buck="currency_monthly")
    