.POSIX:

##################
# Additional Tasks
##################

.PHONY: help
help: ## show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | \
	sort | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

######################
# Development Workflow
######################

.PHONY: clean
clean: ## cleans remnants of the build process
	. ./scripts/clean.sh dev

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

.PHONY: clean-uat
clean-uat: clean ## cleans remnants of the build process on the UAT machine
	. ./scripts/clean.sh uat

.PHONY: build-uat
build-uat: clean-uat ## builds a remote UAT Docker image
	. ./scripts/build.sh uat

.PHONY: deploy-uat
deploy-uat: ## deploys a remote UAT environment
	. ./scripts/deploy.sh uat

.PHONY: stop-uat
stop-uat: ## stops a remote UAT environment
	. ./scripts/stop.sh uat

.PHONY: smoketest
smoketest: ## runs smoke tests against the remote UAT environment
	. ./scripts/test.sh smoke

#####################
# Deployment Workflow
#####################

.PHONY: clean-prod
clean-prod: clean ## cleans remnants of the build process on the production machine
	. ./scripts/clean.sh prod

.PHONY: build-prod
build-prod: clean-prod ## builds a remote production Docker image
	. ./scripts/build.sh prod

.PHONY: deploy
deploy: ## deploys the remote production Docker image
	. ./scripts/deploy.sh prod

.PHONY: stop
stop: ## stops the remote prod service
	. ./scripts/stop.sh prod
