# pull base image
FROM python:3.9.0

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


# install dependencies
COPY ./prod.requirements.txt .
COPY ./dev.requirements.txt .

RUN pip install --upgrade pip -r prod.requirements.txt
RUN pip install --upgrade pip -r dev.requirements.txt

# run a postgres healthcheck
COPY ./scripts/postgres-healthcheck.py /usr/local/bin/postgres-healthcheck
RUN chmod u+x /usr/local/bin/postgres-healthcheck

# copy project
COPY ./app .

CMD python manage.py makemigrations; python manage.py migrate; python manage.py runscript; python manage.py runserver 0.0.0.0:8000