FROM python:3.8

RUN apt-get update
RUN apt-get install -y graphviz graphviz-dev
RUN mkdir /myapp/
COPY requirements.txt /myapp/
WORKDIR /myapp/

RUN pip install -r requirements.txt

COPY . /myapp/