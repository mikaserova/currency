set -m

    /entrypoint.sh couchbase-server &

 
# Couchbase DB Server Ports
# sudo iptables -A INPUT -p tcp -m state –state NEW -m tcp –dport 4369 -j ACCEPT
# sudo iptables -A INPUT -p tcp -m state –state NEW -m tcp –dport 8091 -j ACCEPT
# sudo iptables -A INPUT -p tcp -m state –state NEW -m tcp –dport 80 -j ACCEPT
   
    ST=$( curl  -o /dev/null -s -w "%{http_code}\n"  http://cdb:8091/ui/index.html )
    echo "$ST"
    count=1
while [ $ST -ne 200 ]
do
  ST=$( curl  -o /dev/null -s -w "%{http_code}\n"  http://cdb:8091/ui/index.html )
        echo "$ST"
        echo "waiting ... "
        sleep 10
done

  
    # Setup initial cluster/ Initialize Node
    couchbase-cli cluster-init -c  http://cdb --cluster-name  "currency_stor" --cluster-username "sashasierova" \
    --cluster-password "4esZXdr5" --services data,index,query --cluster-ramsize 768 --cluster-index-ramsize 256 \
    --index-storage-setting default 

    # Setup Administrator username and password
    #curl -4 -v http://scrapper_v2_couch_db_1/settings/web -d port=8091 -d username="sashasierova" -d password="4esZXdr5"


    sleep 15

    # Setup Bucket
     couchbase-cli bucket-create -c http://cdb:8091 --username "sashasierova" \
    --password "4esZXdr5" --bucket "currency_rate" --bucket-type couchbase \
    --bucket-ramsize 256

     sleep 15

      couchbase-cli bucket-create -c http://cdb:8091 --username "sashasierova" \
    --password "4esZXdr5" --bucket "currency_weekly" --bucket-type couchbase \
    --bucket-ramsize 256

     sleep 15

     couchbase-cli bucket-create -c http://cdb:8091 --username "sashasierova" \
    --password "4esZXdr5" --bucket "currency_monthly" --bucket-type couchbase \
    --bucket-ramsize 256

     sleep 15

    # couchbase-cli setting-index -c http://scrapper_v2_couch_db_1:8091 --username "sashasierova" \
    # --password "4esZXdr5" 

   #curl -X POST -v -u "sashasierova":"4esZXdr5" http://scrapper_v2_couch_db_1:8091/query/service -d statement='CREATE PRIMARY INDEX ON `currency_rate`'
   



    fg 1