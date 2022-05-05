# builds a production-ready podman image
build:
	sudo podman build --target=prod -t acbilson/micropub:alpine .

# restarts the systemd service
restart:
	sudo systemd restart container-micropub.service

# builds a production-ready podman image
redeploy: build restart

