FROM alpine:latest AS base

WORKDIR /app

ENV RUNTIME_DEPS \
        sudo \
        bash \
        python3 \
        py3-pip \
        chromium-chromedriver \
        tzdata


RUN apk add --update --no-cache $RUNTIME_DEPS \
    && rm -rf /tmp/*

COPY src/requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "/app/src/ms_rewards_farmer.py"]
