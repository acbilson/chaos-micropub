# builds a production-ready podman image
build:
	podman build --target=prod -t acbilson/micropub:alpine .

# restarts the systemd service
restart:
	systemd restart container-micropub.service

# builds a production-ready podman image
redeploy: build restart

