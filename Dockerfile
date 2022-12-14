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

RUN pip3 install --no-cache-dir -r requirements.txt

ENV DISPLAY=:99
ENV IS_RUNNING_IN_DOCKER=true


CMD ["python", "-u", "/app/src/ms_rewards_farmer.py"]
