# pull the official docker image
FROM python:3.9.5-slim

# set work directory
WORKDIR /app

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG off
ENV DJANGO_SECRET_KEY '-spx)yp3tr$pcx$=^8xn!=1%#$21&6@vk8=p6uui&5f*s*6!0^'
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD challenge

# install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .
