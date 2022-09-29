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

# builds a production podman image, running integration tests along the way
build:
  set COMMIT_ID (git rev-parse --short HEAD); \
  podman build \
  -t acbilson/micropub:latest \
  -t acbilson/micropub:$COMMIT_ID .

# builds a development podman image.
build-dev:
  podman build \
  --target dev \
  -t acbilson/micropub-dev:latest .

# starts a production podman image.
start: build
  podman run --rm \
  --expose $EXPOSED_PORT -p $EXPOSED_PORT:$EXPOSED_PORT \
  -e "SITE=http://localhost:$EXPOSED_PORT" \
  -e "ADMIN_USER=$ADMIN_USER" \
  -e "ADMIN_PASSWORD=$ADMIN_PASSWORD" \
  -e "CLIENT_ID=$GITHUB_CLIENT_ID" \
  -e "CLIENT_SECRET=$GITHUB_CLIENT_SECRET" \
  -e "FLASK_SECRET_KEY=$FLASK_SECRET_KEY" \
  -e "SESSION_SECRET=$SESSION_SECRET" \
  -e "CONTENT_PATH=/mnt/chaos/content" \
  --name micropub \
  acbilson/micropub:latest

# launches a tmux session with everything I need to interactively develop
develop: init
	tmux new-session -s micropub -n serve -d '. src/venv/bin/activate.fish; find ./src/app -name "*.py" | entr -r python ./src/main.py';
	tmux new-window  -t micropub:1 -n edit   'nvim src/main.py';
	tmux attach
