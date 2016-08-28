# web: waitress-serve --port=$PORT andreffs.wsgi:application
web: python manage.py collectstatic --noinput; gunicorn core.wsgi --log-file -
