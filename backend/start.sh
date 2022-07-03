python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --no-input
python manage.py graph_models -a -o erd.png
python manage.py runserver 0.0.0.0:8000
