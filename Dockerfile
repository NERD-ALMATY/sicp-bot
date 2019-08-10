FROM python:3.7.4

RUN mkdir /srv/app

COPY . /srv/app

RUN cd /srv/app

RUN pip install -r requirements.txt

ENV TELE_TOKEN=''
ENV GITHUB_TOKEN=''
ENV DIR_PATTERN=''

CMD python main.py

