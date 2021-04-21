#!/bin/bash
. .env

ENVIRONMENT=$1

case $ENVIRONMENT in

dev)
  echo "creates files from template..."
  mkdir dist && \
    envsubst < template/build-site.sh > dist/build-site.sh && \
    envsubst < template/config-dev.toml > dist/config.toml

  echo "builds development image..."
  docker build -f Dockerfile \
    --target=dev \
    --build-arg EXPOSED_PORT=${EXPOSED_PORT} \
    -t acbilson/micropub-dev:alpine-3.12 .
;;

uat)
  echo "creates files from template..."
  mkdir -p dist/dist && \
    envsubst < template/build-site.sh > dist/dist/build-site.sh && \
    envsubst < template/config-uat.toml > dist/dist/config.toml

  echo "copies files to distribute..."
  cp Dockerfile dist/

  echo "copies source code to distribute..."
  cp -r src dist/src

  echo "distributes dist/ folder..."
  scp -r dist web:/mnt/msata/build/uat

  echo "builds image on UAT"
  ssh -t web \
    sudo podman build \
      -f /mnt/msata/build/uat/Dockerfile \
      --target uat \
      -t acbilson/micropub-uat:alpine-3.12 \
      /mnt/msata/build/uat
;;

prod)
  mkdir dist
  echo "under construction";
;;

*)
  echo "please provide one of the following as the first argument: dev, uat, prod."
  exit 1

esac
