# exit on error
set -e

echo "<<<<<<<<<<<<<<<<<<<<<  RUNNING MIGRATIONS >>>>>>>>>>>>>>>>>>>>>>>>"
python manage.py migrate 


#Create background service for celery worker and beat
# celery -A expense worker -l info -E &
gunicorn exception_management.wsgi --bind 0.0.0.0:8000
#python src/manage.py runserver 0.0.0.0:8000