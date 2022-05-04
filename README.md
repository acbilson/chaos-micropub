An ~IndieWeb~ original micropub server, written in Python Flask.

chaos-micropub began as an IndieWeb micropub server and retains the name, but to get started it's locked into a specific Hugo workflow. To me the capacity to publish personal comments to my site is more important than interoperability. It does not presently do anything particularly IndieWeb-like, except perhaps by abiding by the rule to eat one's own dogfood.

# Images

This is the interface for creating a note. There are more fields as you scroll down, but I like ample whitespace.

![Create Note](https://github.com/acbilson/chaos-micropub/blob/master/images/2021-10-27-note-form.png)

This is the interface for editing a log.

![Edit Log](https://github.com/acbilson/chaos-micropub/blob/master/images/2021-10-27-log-edit-form.png)

# Configuration

The entire workflow can be accomplished via Make, however, you'll need to configure the scripts on which Make depends by creating a .env file. `env-example` supplies the required variables.

# Developer Process

This code flows through three steps:

Develop -> Verify -> Deploy

In develop, the goal is to provide quick feedback for code changes and test this service as a single system.

In verify (or <acronym title="User Acceptance Testing">UAT</acronym>), the goal is to confirm that this service is operable with its other services. It mimics the production environment.

In deploy, the goal is to deliver this service to my production server.

The processor architecture and container tooling I use in production differs from what I use locally. To avoid issues porting this service to the production server, I use the same server to conduct my UAT and production builds and tests.

# Develop

### Artifacts

Docker image: acbilson/micropub-dev:alpine
Hugo config: config-dev.toml
Hugo build script: build-site.sh
Hugo theme: [acbilson/chaos-theme](https://github.com/acbilson/chaos-theme.git)
Markdown content: [acbilson/chaos-content](https://github.com/acbilson/chaos-content.git)

### Dependencies

- Docker
- Make
- bash
- envsubst
- entr (optional)

## Build

To build a local Docker developer image, run:

`make build`

The developer image runs the Flask application directly without UWSGI to take advantage of file change refresh. Also, authentication is disabled in the developer image so I don't need a fresh OAuth token for local development.

## Run

To start the developer container, run:

`make start`

## Test

Unit tests are run on the developer image with the following command:

`make test`

When I'm making changes, I like to get immediate feedback from my unit tests on save. This can be accomplished with the invaluable `entr` command. It will watch for file changes and run whatever command you'd like after any change happens. Here's how I use it:

`find ./src | entr make test`

# Verify

### Artifacts

Docker image: acbilson/micropub-uat:alpine
Hugo config: config.toml
Hugo build script: build-site.sh
UWSGI config: micropub.ini
Hugo theme: [acbilson/chaos-theme](https://github.com/acbilson/chaos-theme.git)
Markdown content: [acbilson/chaos-content](https://github.com/acbilson/chaos-content.git)

### Dependencies

A production-like uat server with:

- Podman
- OpenSSH
- bash

## Build

To build a Docker verify image on the UAT server, run:

`make build-uat`

## Deploy

To deploy the image on the UAT server, run:

`make deploy-uat`

The UAT image runs the Flask application behind UWSGI to mimic the production instance.

# Deploy

### Artifacts

Docker image: acbilson/micropub:alpine
Hugo config: config-uat.toml
Hugo build script: build-site.sh
UWSGI config: micropub.ini
Systemd service file: container-micropub.service
Hugo theme: [acbilson/chaos-theme](https://github.com/acbilson/chaos-theme.git)
Markdown content: [acbilson/chaos-content](https://github.com/acbilson/chaos-content.git)

### Dependencies

A production server with:

- Podman
- OpenSSH
- bash
- systemd
- A web proxy like Nginx to broadcast this service to the public Web

## Build

To build a Docker production image on the prod server, run:

`make build-prod`

## Run

To start the production service, run:

`make deploy`

The production image runs the Flask application behind UWSGI, which allows for multi-threading and interfaces with my web proxy. The container is managed by systemd.

## Redeploy

Since my app is not production-critical I will sometimes publish hotfixes to production before testing in uat. The deployment process is greatly simplified with redeploy, which disables, rebuilds, and enables my service.

`make redeploy`
