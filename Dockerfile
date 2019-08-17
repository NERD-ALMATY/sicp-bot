FROM python:3.7.4

RUN mkdir /srv/app

COPY . /srv/app

WORKDIR /srv/app

RUN pip install -r requirements.txt

EXPOSE 5000

CMD python sicp_bot

