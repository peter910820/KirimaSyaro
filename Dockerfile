# syntax=docker/dockerfile:1.4
FROM --platform=$BUILDPLATFORM python:3.10-alpine

WORKDIR /app
ADD . /app

# set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# install the requirements
RUN pip3 install --requirement /app/requirements.txt
RUN pip3 install -U pytube

EXPOSE 5000/tcp

CMD ["python", "./main.py"]