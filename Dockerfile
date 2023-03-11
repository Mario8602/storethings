FROM python:3.10-alpine3.16

COPY requirements.txt /temp/requirement.txt
COPY store /store
WORKDIR /store
EXPOSE 8000

RUN pip install -r /temp/requirement.txt

RUN adduser --disabled-password store-user

USER store-user