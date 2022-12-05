FROM python:3.10-alpine as dev
RUN apk update
RUN apk add bash

COPY requirements.txt /home/
RUN pip install -r /home/requirements.txt
WORKDIR /home/App
COPY App .
RUN python manage.py test 


FROM python:3.10-alpine as production



#ENV PYTHONPATH="${PYTHONPATH}:/home/App"
RUN apk update
RUN apk add bash

COPY requirements.txt /home/
RUN pip install -r /home/requirements.txt
