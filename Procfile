release: python app/manage.py migrate
web: gunicorn --chdir app core.wsgi:application --log-file -
