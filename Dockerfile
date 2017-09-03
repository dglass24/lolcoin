FROM ubuntu:16.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN mkdir var

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000
EXPOSE 5001
