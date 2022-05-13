# allows arguments to be passed to the script
set positional-arguments := true

# builds a production-ready podman image. Must pass commit revision.
build ref:
	rev=${1:0:7}; podman build --target=prod -t acbilson/micropub-$rev:alpine .

# restarts the systemd service
restart:
	systemctl --user restart container-micropub.service
