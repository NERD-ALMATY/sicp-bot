FROM python:3.7.4

RUN mkdir /srv/app

COPY . /srv/app

WORKDIR /srv/app

RUN pip install -r requirements.txt

CMD python sicp_bot

