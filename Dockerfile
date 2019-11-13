FROM selenium/standalone-chrome 

COPY . /v2
WORKDIR /v2
RUN sudo wget -O - http://packages.couchbase.com/ubuntu/couchbase.key | sudo apt-key add -
# Adding Ubuntu 18.04 repo to apt/sources.list of 18.10 or 19.04
RUN echo "deb http://packages.couchbase.com/ubuntu bionic bionic/main" | sudo tee /etc/apt/sources.list.d/couchbase.list
RUN sudo apt-get update

RUN sudo apt-get install -y libcouchbase2-libevent libcouchbase-dev build-essential
RUN sudo apt-get install -y python3.7-dev

#
#RUN python3 -m pip install --upgrade pip
RUN sudo apt-get install --fix-missing   -y python3-setuptools
RUN sudo apt-get install -y python3-pip
#RUN  sudo -H python3 -m pip uninstall pip && sudo apt --reinstall  install python3-pip 
RUN sudo apt-get install -y cron
#RUN sudo apt-get install -y git-core
#RUN pip3 install git+git://github.com/couchbase/couchbase-python-client
#RUN pip3 install couchbase
RUN sudo pip3 install -r requirements.txt
RUN sudo pip3 install python-crontab

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
RUN sudo  sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN sudo apt-get -y update
RUN sudo apt-get install -y google-chrome-stable

# install chromedriver
RUN sudo apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN sudo unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# set display port to avoid crash
ENV DISPLAY=:99
USER root
# install selenium
#RUN pip3 install selenium==3.8.0
EXPOSE 4444:5000
CMD python3 ./run.py 