# baie
集成flask_Sqlalchemy flask_login, 开箱即用


gunicorn -w 4 -b 0.0.0.0:5000 --timeout 500 -k tornado app:tornado_app

celery worker -A 'celerywork' --loglevel=INFO --logfile=/var/log/deploy/celery.log