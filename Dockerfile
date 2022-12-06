FROM python:3-alpine3.12

WORKDIR /app

ENV RUNTIME_DEPS \
        sudo \
        bash \
        chromium \
        chromium-chromedriver \
        tzdata


RUN apk add --update --no-cache $RUNTIME_DEPS \
    && rm -rf /tmp/*

COPY src/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ENV DISPLAY=:99
ENV IS_RUNNING_IN_DOCKER=true


CMD ["python", "/app/src/ms_rewards_farmer.py"]
