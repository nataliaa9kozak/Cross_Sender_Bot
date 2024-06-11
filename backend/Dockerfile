FROM python:3.9.6-alpine

WORKDIR /usr/src/backend

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir logs

COPY . .

# Do some commands
RUN echo "Collect static files"
RUN python manage.py collectstatic --noinput

RUN adduser -S -D -u 1000 docker_user
RUN chown -R 1000:1000 /usr/src/backend
USER docker_user
