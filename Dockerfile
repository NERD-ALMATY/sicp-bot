FROM python:3.7-slim-buster

WORKDIR /app

COPY sicp_bot sicp_bot
COPY bin bin
COPY setup.py setup.py

RUN mkdir data

RUN pip install -e .

CMD sicp-bot

