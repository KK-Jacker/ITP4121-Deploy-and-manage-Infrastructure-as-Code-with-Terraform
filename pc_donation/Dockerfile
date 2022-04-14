FROM python:3.9.6-alpine

WORKDIR /home/pc_donation

# set arugements
ARG VAULT_URL
ARG AZURE_CLIENT_ID
ARG AZURE_TENANT_ID
ARG AZURE_CLIENT_SECRET
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
ENV FLASK_ENV=development
ENV DATABASE_HOST=mysql
ENV MAIL_SERVER=smtp4dev
ENV NGINX_PORT=8080
ENV VAULT_URL=${VAULT_URL}
ENV AZURE_CLIENT_ID=${AZURE_CLIENT_ID}
ENV AZURE_TENANT_ID=${AZURE_TENANT_ID}
ENV AZURE_CLIENT_SECRET=${AZURE_CLIENT_SECRET}

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
ENV FLASK_DEBUG=1

EXPOSE 80 443 5000
ENTRYPOINT ["./web.sh"]
