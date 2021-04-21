.POSIX:

##################
# Additional Tasks
##################

.PHONY: init
init: ## initializes the project configuration
	. ./scripts/init.sh

.PHONY: clean
clean: ## cleans remnants of the build process
	. ./scripts/clean.sh

.PHONY: help
help: ## show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | \
	sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

######################
# Development Workflow
######################

.PHONY: build
build: clean ## builds a local development Docker image
	. ./scripts/build.sh dev

.PHONY: start
start: ## starts a local development Docker container
	. ./scripts/start.sh

.PHONY: unittest
unittest: ## runs unit tests in a local development Docker container
	. ./scripts/test.sh unit

##############
# UAT Workflow
##############

.PHONY: build-uat
build-uat: clean ## builds a remote UAT Docker image
	. ./scripts/build.sh uat

.PHONY: deploy-uat
deploy-uat: ## deploys a remote UAT environment
	. ./scripts/deploy.sh uat

.PHONY: smoketest
smoketest: ## runs smoke tests against the remote UAT environment
	. ./scripts/test.sh smoke
	curl http://localhost:5000/health --verbose; \
  sleep 1 && docker logs -n 5 micropub

#####################
# Deployment Workflow
#####################

.PHONY: build-prod
build-prod: clean ## builds a remote production Docker image
	. ./scripts/build.sh prod

.PHONY: deploy
deploy: ## deploys the remote production Docker image
	. ./scripts/deploy.sh prod
