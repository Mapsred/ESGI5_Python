fix-perm:
	sudo chown -R $USER:$USER ./polls

bash:
	docker-compose exec web bash

.PHONY: fix-perm bash
