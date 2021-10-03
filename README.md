# README

## Serve backend in Linux distro and WSL

1. install nginx, redis
2. clone frontend and backend repo to /var/www
3. copy `api` file to `/etc/nginx/sites-avaliable`
4. `ln -s /etc/nginx/sites-avaliable/api /etc/nginx/sites-enabled/api`
5. `rm /etc/nginx/sites-enabled/default`
6. `service nginx start` (or restart)
7. cd repo dir & run setup.sh in repo, which will create apienv first and install needed package 
(please add to package list if some package missing)
8. `source apienv/bin/activate`
9. `gunicorn --workers 3 --bind unix:/tmp/api.sock -m 007 wsgi:app`
10. for sake of privilige, `chmod 777 /tmp/api.sock` (DO NOT EXECUTE IN PRODUCTION ENVIRONMENT)
11. start celery server with `celery -A pool worker -c 12`
12. browse page at localhost
