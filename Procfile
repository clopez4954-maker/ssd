web: cd backend && python manage.py migrate && python manage.py collectstatic --no-input && gunicorn config.wsgi --bind 0.0.0.0:$PORT
