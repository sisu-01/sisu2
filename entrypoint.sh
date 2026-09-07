python3 manage.py migrate
gunicorn config.wsgi -b unix:/tmp/gunicorn_sisu2.sock -D
nginx
