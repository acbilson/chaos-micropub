.POSIX:

.PHONY: config-dev
config-dev: copy-env ## configures dev templates from env file
	cp template/build-site.sh uwsgi/build-site.sh; \
	cp template/micropub.ini uwsgi/micropub.ini

.PHONY: config-prod
config-prod: ## configures prod templates from env file
	cp template/build-site.sh uwsgi/build-site.sh; \
	cp template/micropub.ini uwsgi/micropub.ini

.PHONY: build-dev
build-dev: config-dev ## builds a version to be used for development
	docker build -f uwsgi/Dockerfile -t acbilson/micropub:alpine-3.12 .

.PHONY: build-prod
build-prod: config-prod ## builds a version to be used for production
	sudo podman build -f uwsgi/Dockerfile -t acbilson/micropub:alpine-3.12 .

.PHONY: start-dev
start-dev: build-dev ## runs a local development version
	docker run --rm -d -p 5000:80 --env-file .env --name micropub \
		-v ~/source/alexbilson.dev/hugo/config:/etc/hugo \
		-v ~/source/chaos-content:/mnt/chaos/content \
		-v ~/source/chaos-theme:/mnt/chaos/themes/chaos \
		acbilson/micropub:alpine-3.12

.PHONY: start-prod
start-prod: ## run a production version
	echo 'production micropub will be deployed across multiple containers'

.PHONY: test
test: ## tests development docker image
	curl http://localhost:5000/health --verbose; \
  sleep 1 && docker logs -n 5 micropub

.PHONY: clean
clean: ## cleans remnants of the build process
	docker rm micropub;
	rm uwsgi/build-site.sh

.PHONY: copy-env
copy-env: ## copies env for backup
	mkdir -p ~/safe/micropub && cp .env ~/safe/micropub/env.bk

.PHONY: help
help: ## show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | \
	sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
