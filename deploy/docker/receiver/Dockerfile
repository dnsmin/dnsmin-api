FROM python:3.12-slim

WORKDIR /srv/app

COPY ./src-api/receiver.py /srv/app/server.py

RUN apt update \
    && apt install -y --no-install-recommends curl \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install dnspython aiohttp

ENV ZONES_BIND_HOST=0.0.0.0

EXPOSE 5353 5354 8000

USER 1000:1000

CMD ["python", "server.py"]
