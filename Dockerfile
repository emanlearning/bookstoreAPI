FROM ubuntu:latest
LABEL authors="Asus"

ENTRYPOINT ["top", "-b"]



FROM tiangolo/uvicorn-gunicorn-fastapi:python3.14

COPY requirements.txt /
RUN python -m pip install - r/requirements.txt

COPY . /app
WORKDIR /app

