fix-perm:
	sudo chown -R $USER:$USER ./polls

bash:
	docker-compose exec web bash

migrate:
	python manage.py migrate

shell:
	python manage.py shell

.PHONY: fix-perm bash migrate shell
