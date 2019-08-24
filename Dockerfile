FROM python:3.7.4

WORKDIR /app

COPY sicp_bot sicp_bot

COPY prod-requirements.txt prod-requirements.txt

RUN pip install -r prod-requirements.txt

RUN mkdir data

CMD python sicp_bot

