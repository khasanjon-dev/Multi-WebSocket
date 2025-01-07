FROM python:3.12-slim-bullseye

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

COPY ./requirements /app/requirements/

RUN pip install -r /app/requirements/local.txt

COPY ./compose/ /compose/

RUN mv /compose/local/django/start /start
RUN cat start | sed 's/\r$//' > start
RUN chmod +x /start

RUN mv /compose/local/django/entrypoint /entrypoint
RUN cat entrypoint | sed 's/\r$//' > entrypoint
RUN chmod +x /entrypoint


RUN rm -rf /compose/


COPY . /app


ENTRYPOINT [ "bash", "/entrypoint" ]

