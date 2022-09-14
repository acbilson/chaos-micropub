set dotenv-load
set shell := ["/opt/homebrew/bin/fish", "-c"]

# instantiates a local python virtualenv
init:
	if not test -d src/venv; python -m venv src/venv; end;
	if not test -d src/venv/lib/python3.10/site-packages/werkzeug; echo 'install packages to continue'; end

# tests that we're using a virtualenv
venv:
	if test (which python) = "/usr/local/bin/python"; echo 'not a virtualenv, please activate' && return 1; else; return 0; end

# runs a local development instance
run: init venv
	python src/main.py

# builds a development docker image.
build:
  set COMMIT_ID (git rev-parse --short HEAD); \
  docker build \
  --target dev \
  -t acbilson/micropub:latest \
  -t acbilson/micropub:$COMMIT_ID .

# starts a development docker image.
start:
  docker run --rm \
  --expose $EXPOSED_PORT -p $EXPOSED_PORT:80 \
  -e "SITE=http://localhost:$EXPOSED_PORT" \
  -e "CLIENT_ID=$GITHUB_CLIENT_ID" \
  -e "CLIENT_SECRET=$GITHUB_CLIENT_SECRET" \
  -e "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" \
  -e "SESSION_SECRET=$SESSION_SECRET" \
  -e "CONTENT_PATH=/mnt/chaos/content" \
  -v $SOURCE_PATH/src:/mnt/src \
  -v $CONTENT_PATH:/mnt/chaos/content \
  --name micropub \
  acbilson/micropub:latest
