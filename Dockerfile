FROM python:3.6

MAINTAINER Stefan Kuznetsov (skuznetsov@posteo.net)

ADD . /bolas

WORKDIR /bolas

RUN pip install -r requirements.txt

CMD ["python", "./run.py"]