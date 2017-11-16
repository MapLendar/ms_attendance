FROM python:3

ENV PYTHONUNBUFFERED 1

RUN mkdir /ms_attendance
WORKDIR /ms_attendance

RUN pip install Django
RUN pip install django-tastypie
RUN pip install mysqlclient

ADD . /ms_attendance
