FROM python:3.9.6-alpine

WORKDIR /home/pc_donation

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

RUN apk add --no-cache --update build-base gcc python3-dev jpeg-dev zlib-dev musl-dev libffi-dev openssl-dev nginx bash

COPY requirements.txt requirements.txt
RUN python3.9 -m venv venv
RUN venv/bin/pip3 install --upgrade pip
RUN venv/bin/pip3 install -r requirements.txt
RUN venv/bin/pip3 install gunicorn
COPY app app
COPY migrations migrations
COPY pc_donation.py config.py run.py boot.sh nginx.sh web.sh ./
RUN chmod +x boot.sh nginx.sh web.sh

COPY nginx.conf /etc/nginx/
COPY dev/project.conf /etc/nginx/conf.d/
RUN mkdir -p /run/nginx
RUN mkdir -p /home/pc_donation/logs
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
ENV FLASK_APP run.py
ENV FLASK_DEBUG=0

EXPOSE 80 443 5000
ENTRYPOINT ["./web.sh"]
