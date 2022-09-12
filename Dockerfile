# Execution environment specification
#
# This file defines application's operating-system-level virtualization
# See https://docs.docker.com/engine/reference/builder/.


FROM python:3.10

WORKDIR app

COPY Makefile .env .env.example requirements.txt ./
RUN make init

COPY . .
RUN make setup

EXPOSE 8000

HEALTHCHECK CMD curl http://localhost:8000 || exit 1

CMD make run
