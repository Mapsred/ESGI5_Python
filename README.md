PyStone
=======

How to ...
----------

### Initiate the project

```bash
docker-compose up -d
docker-compose exec web bash

python manage.py migrate
python manage.py create_cards
python manage.py createsuperuser
```

If you want to make migrations :

```bash
python manage.py makemigrations
```

#### Some ressources
https://docs.djangoproject.com/en/2.1/intro/tutorial01/
https://docs.djangoproject.com/en/2.1/intro/tutorial02/
https://docs.djangoproject.com/en/2.1/intro/tutorial03/
https://docs.djangoproject.com/en/2.1/intro/tutorial04/

...