#!/bin/bash
. .env

ENVIRONMENT=$1

case $ENVIRONMENT in

dev)
  docker build -f Dockerfile \
    --target=dev \
    --build-arg EXPOSED_PORT=${EXPOSED_PORT} \
    -t acbilson/micropub-dev:alpine-3.12 .
;;

uat)
  mkdir dist
  ssh -t web sudo podman build -f /mnt/msata/source/chaos-micropub/uwsgi/Dockerfile -t acbilson/micropub-uat:alpine-3.12 /mnt/msata/source/chaos-micropub
;;

prod)
  mkdir dist
  echo "under construction";
;;

*)
  echo "please provide one of the following as the first argument: dev, uat, prod."
  exit 1

esac
