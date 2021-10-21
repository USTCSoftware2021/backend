#!/usr/bin/bash

echo "1. Create virtual environment."

python3 -m venv apienv
if ! [ -e apienv/bin/activate ]; then
	echo "Venv create failed."
	exit 1
fi

source apienv/bin/activate

pip install -U pip
pip install -U setuptools
pip install setuptools_scm
pip install wheel
pip install -r requirements.txt

echo "2. Move required nginx and systemd config files, assuming that systemd is used as init process"
echo "> Note: the config differs from our deployment for https config is exclusive to specific site"

cp ./server_config/cat /etc/nginx/sites-avaliable
ln -s /etc/nginx/sites-avaliable/cat /etc/nginx/sites-enabled/cat
rm /etc/nginx/sites-enabled/default

cp ./server_config/*.service /etc/systemd/system
systemctl daemon-reload
systemctl start nginx.service
systemctl start gunicorn.service
systemctl start celery.service
systemctl start redis.service