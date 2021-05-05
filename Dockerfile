FROM python:3.8-alpine

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE 1
ENV DEBUG 0

WORKDIR /code

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    && apk del build-deps

COPY . .
RUN pip install -r requirements.txt
RUN python manage.py migrate
RUN pip install gunicorn
CMD python manage.py runserver 0.0.0.0:$PORT
#CMD gunicorn news.wsgi:application --bind 0.0.0.0:$PORT
