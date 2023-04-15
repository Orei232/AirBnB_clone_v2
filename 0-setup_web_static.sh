#!/usr/bin/env bash
# this is a script used is set up web servers for web static

apt-get update
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/
mkdir -p /data/

echo "Holberton school" > /data/web_static/releases/test/index.html
In -sf /data/web_static/releases/test/ /data/web_static/current
chown -R ubuntu /data/
chgrp -R ubuntu /data/
service nginx restart
