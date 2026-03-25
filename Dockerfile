# Dockerfile
FROM python:3.14.0

RUN mkdir /src
WORKDIR /src
COPY . /src
RUN apt-get update && apt-get install -y sqlite3
RUN pip install -r requirements.txt
