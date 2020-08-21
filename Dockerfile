FROM python:3.7-slim

LABEL version="v1"
LABEL description="Stock Bot - check stock prices and warn when a threshold is reached"
LABEL maintainer="Dennis Bakhuis"
LABEL linkedin="https://www.linkedin.com/in/dennisbakhuis/"

RUN useradd -ms /bin/bash stockbot
WORKDIR /home/stockbot

COPY ./requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./app app

RUN chown -R stockbot:stockbot ./
USER stockbot

CMD ["python",\
     "app/StockAlarmServer.py"\
]
