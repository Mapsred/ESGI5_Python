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

Create the superadmin in one line
```bash
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'kamal123')" | ./manage.py shell
```

#### Some ressources
https://docs.djangoproject.com/en/2.1/intro/tutorial01/
https://docs.djangoproject.com/en/2.1/intro/tutorial02/
https://docs.djangoproject.com/en/2.1/intro/tutorial03/
https://docs.djangoproject.com/en/2.1/intro/tutorial04/

https://github.com/Conchylicultor/DeepQA 
https://bootsnipp.com/snippets/featured/message-chat-box
...