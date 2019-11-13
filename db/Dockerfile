FROM couchbase/server

COPY configure-server.sh /opt/couchbase
USER root
RUN chmod +x /opt/couchbase/configure-server.sh

# RUN  apt-get update
# RUN  apt-get -y upgrade 
# RUN apt-get install -y 


# RUN  apt-get install iptables sudo -y

# # RUN ufw status verbose
# RUN ufw  allow 80 
# RUN apt-get update && apt-get install sudo
# #RUN sudo netstat -tnlp tcp | grep :80
# RUN  sudo apt-get install -y iptables
CMD ["/opt/couchbase/configure-server.sh"]
#RUN curl -u "sashasierova":"4esZXdr5" -d "CREATE PRIMARY INDEX ON \`currency_rate\`" http://scrapper_v2_couch_db_1:8095/analytics/service
#RUN   cbq --script="CREATE PRIMARY INDEX ON \`currency_rate\`"