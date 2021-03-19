.POSIX:

.PHONY: build
build: ## builds a version to be used for local development
	docker build --target develop -t acbilson/chaos-micropub-dev .

.PHONY: dev
dev: build ## runs a local dev server
	docker run --rm -p 5000:5000 acbilson/chaos-micropub-dev

.PHONY: build-deploy
build-deploy: ## builds a version to be used for deployment
	docker build -f dockerfile.prod -t acbilson/chaos-micropub-nginx .

.PHONY: build-prod
build-prod: ## builds a production version of my containers
	sudo podman build -f uwsgi/Dockerfile -t acbilson/chaos-micropub-uwsgi .; \
	sudo podman build -f nginx/Dockerfile -t acbilson/chaos-micropub-nginx .

.PHONY: build-uwsgi
build-uwsgi: ## builds a uwsgi production-ready container
	docker build -f uwsgi/Dockerfile -t acbilson/chaos-micropub-uwsgi .

.PHONY: build-nginx
build-nginx: ## builds a nginx container to serve my app
	docker build -f nginx/Dockerfile -t acbilson/chaos-micropub-nginx .

.PHONY: run-uwsgi
run-uwsgi: build-uwsgi ## runs a local uwsgi container
	docker run --rm -p 5000:5000 acbilson/chaos-micropub-uwsgi

.PHONY: start
start: build-prod ## runs a local production pod
	sudo podman pod create -p 3000:3000 -n pod1; \
  sudo podman run -dt --pod pod1 localhost/acbilson/chaos-micropub-uwsgi; \
  sudo podman run -dt --pod pod1 localhost/acbilson/chaos-micropub-nginx

.PHONY: stop
stop: ## stops a local production pod
	sudo podman pod stop pod1 && sudo podman pod rm pod1

.PHONY: deploy
deploy: build-deploy ## runs a local production server
	docker run --rm -p 5002:80 acbilson/chaos-micropub-nginx

.PHONY: clean
clean: ## cleans the docker images
	docker rmi acbilson/chaos-micropub-dev && \
  docker rmi acbilson/chaos-micropub-nginx

.PHONY: copy-env
copy-env: ## copies ignored file for storage
	cp src/.env ~/safe/micropub/.env

.PHONY: help
help: ## show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | \
	sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
