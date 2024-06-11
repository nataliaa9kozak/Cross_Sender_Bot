FROM python:3.12-alpine

WORKDIR /usr/src/telegram_app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN adduser -S -D -u 1000 docker_user
RUN chown -R 1000:1000 /usr/src/telegram_app
USER docker_user
