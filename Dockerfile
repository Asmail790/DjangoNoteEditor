FROM python:3.10-alpine



#ENV PYTHONPATH="${PYTHONPATH}:/home/App"
RUN apk update
RUN apk add bash

COPY requirements.txt /home/
RUN pip install -r /home/requirements.txt