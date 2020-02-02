FROM python:3

ADD . /api

WORKDIR /api

RUN apt-get update
RUN pip install --no-cache-dir -r requirements.txt

expose 8080
CMD python run.py 