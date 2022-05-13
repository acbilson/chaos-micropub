#!/bin/bash
rev=${1:0:7}; podman build --target=prod -t acbilson/micropub-$rev:alpine .
