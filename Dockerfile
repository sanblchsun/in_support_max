FROM python:3.10.4

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN apt-get update && apt-get install -y sqlite3
RUN apt-get -y install ntp
RUN cp /usr/share/zoneinfo/Europe/Moscow /etc/localtime
RUN pip install -r requirements.txt
