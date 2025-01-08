install:
	pip install -r requirements/local.txt


# DJANGO
make:
	docker exec -it multi-websocket-django-1 python manage.py makemigrations
mig:
	docker exec -it multi-websocket-django-1 python manage.py migrate
super:
	docker exec -it multi-websocket-django-1 python manage.py createsuperuser