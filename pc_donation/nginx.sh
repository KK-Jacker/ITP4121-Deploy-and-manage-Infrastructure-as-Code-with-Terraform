#!/bin/sh
# this script is used to boot a Docker container
source venv/bin/activate

exec nginx -g "daemon off;"
# exec /usr/sbin/nginx -c /etc/nginx/nginx.conf
