FROM python:3.10-alpine3.16

COPY requirements.txt /temp/requirement.txt
COPY store /store
WORKDIR /store
EXPOSE 8000

RUN apk update && apk add postgresql-client build-base postgresql-dev
#RUN apk update && apk add postgresql-client build-base postgresql-dev gcc python3-dev musl-dev

#RUN apk add postgresql-client build-base postgresql-dev

RUN pip install -r /temp/requirement.txt

RUN adduser --disabled-password store-user

USER store-user