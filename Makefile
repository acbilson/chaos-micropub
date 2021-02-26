.POSIX:

.PHONY: serve
serve: build ## runs a local dev server
	docker run --rm -p 8091:8080 acbilson/chaos-micropub-server

.PHONY: build
build: ## builds a version to be used for local testing in Nginx
	docker build -t acbilson/chaos-micropub-server .

.PHONY: help
help: ## show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | \
	sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'
