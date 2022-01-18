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

# copy project
COPY ./app .

CMD python manage.py makemigrations; python manage.py migrate; python manage.py runserver 0.0.0.0:8000