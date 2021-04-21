# chaos-micropub

An ~IndieWeb~ original micropub server, written in Python Flask.

chaos-micropub began as an IndieWeb micropub server and retains the name, but to get started it's locked into a specific Hugo workflow. To me, the capacity to publish personal comments to my site is more important than interoperability.

# Configuration

The entire workflow can be accomplished via Make, however, there is an initial configuration step necessary to get started.

For an interactive configuration, run:

`make init`


# Developer Process

This code flows through three steps:

Develop -> Verify -> Deploy

In develop, the goal is to provide quick feedback for code changes and test this service as a single system.

In verify (or <acronym title="User Acceptance Testing">UAT</acronym>), the goal is to confirm that this service is operable with its other services. It mimics the production environment.

In deploy, the goal is to deliver this service to my production server.

The processor architecture and container tooling I use in production differs from what I use locally. To avoid issues porting this service to the production server, I use the same server to conduct my UAT and production builds and tests.


# Develop

### Artifacts

Docker image: acbilson/micropub-dev:alpine-3.12
Hugo config: config-dev.toml
Hugo theme: [acbilson/chaos-theme](https://github.com/acbilson/chaos-theme.git)
Markdown content: [acbilson/chaos-content](https://github.com/acbilson/chaos-content.git)

### Dependencies

- Docker
- Make
- OpenSSH

## Build

To build a local Docker developer image, run:

`make build`

The developer image runs the Flask application directly without UWSGI to take advantage of file change refresh.


## Run

To start the developer container, run:

`make start-dev`

## Test - TODO

Unit tests are run on the developer image with the following command:

`make unittest`


# Verify

### Artifacts

Docker image: acbilson/micropub-uat:alpine-3.12
Hugo config: config.toml
Hugo theme: [acbilson/chaos-theme](https://github.com/acbilson/chaos-theme.git)
Markdown content: [acbilson/chaos-content](https://github.com/acbilson/chaos-content.git)

### Dependencies

A production-like uat server with:

- A container program that can build Dockerfiles and run containers
- OpenSSH

## Build - TODO

To build a Docker verify image on the uat server, run:

`make build-uat`

## Run - TODO

To deploy the UAT environment, run:

`make deploy-uat`

The UAT image runs the Flask application behind UWSGI to mimic the production instance.

## Test - TODO

Smoke tests are run on the production image with:

`make smoketest`

Smoke tests depend on the presence of two Docker images to mimic the production environment:

- nginx:alpine-stable
- acbilson/webhook-uat:alpine-3.12


# Deploy

### Artifacts

Docker image: acbilson/micropub:alpine-3.12
Hugo config: config-uat.toml
Hugo theme: [acbilson/chaos-theme](https://github.com/acbilson/chaos-theme.git)
Markdown content: [acbilson/chaos-content](https://github.com/acbilson/chaos-content.git)

### Dependencies

A production server with:

- A container program that can build Dockerfiles and run containers
- OpenSSH
- A web proxy to broadcast this service to the public Web

## Build

To build a Docker production image on the prod server, run:

`make build-prod`

## Run

To start the production service, run:

`make deploy`

The production image runs the Flask application behind UWSGI, which allows for multi-threading and interfaces with my web proxy.
