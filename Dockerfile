FROM python:3.11

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1

WORKDIR /bot

RUN apt-get update && apt-get install -y ffmpeg

COPY poetry.lock pyproject.toml ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-root

COPY . .
