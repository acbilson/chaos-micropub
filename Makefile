.POSIX:

.PHONY: serve
serve: ## runs a local dev server
	cd client; npm run serve

.PHONY: build
build: ## builds a version to be used for local testing in Nginx
	cd client; npm run build

.PHONY: help
help: ## show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | \
	sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

