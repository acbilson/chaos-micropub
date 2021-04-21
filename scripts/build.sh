#!/bin/bash
. .env

ENVIRONMENT=$1

case $ENVIRONMENT in

dev)
  echo "creates files from template..."
  mkdir dist && \
    envsubst < template/build-site.sh > dist/build-site.sh && \
    envsubst < template/micropub.ini > dist/micropub.ini && \
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
    envsubst < template/micropub.ini > dist/dist/micropub.ini && \
    envsubst < template/config-dev.toml > dist/dist/config.toml

  echo "copies files to distribute..."
  cp Dockerfile dist/

  echo "copies source code to distribute..."
  cp -r src dist/src

  echo "distributes dist/ folder..."
  scp -r dist ${UAT_HOST}:/mnt/msata/build/uat

  echo "builds image on UAT"
  ssh -t ${UAT_HOST} \
    sudo podman build \
      -f /mnt/msata/build/uat/Dockerfile \
      --target=uat \
      -t acbilson/micropub-uat:alpine-3.12 \
      /mnt/msata/build/uat
;;

prod)
  echo "creates files from template..."
  mkdir -p dist/dist && \
    envsubst < template/build-site.sh > dist/dist/build-site.sh && \
    envsubst < template/micropub.ini > dist/dist/micropub.ini && \
    envsubst < template/config-prod.toml > dist/dist/config.toml && \
    envsubst < template/container-micropub.service > dist/container-micropub.service

  echo "copies files to distribute..."
  cp Dockerfile dist/

  echo "copies source code to distribute..."
  cp -r src dist/src

  echo "distributes dist/ folder..."
  scp -r dist ${PROD_HOST}:/mnt/msata/build/prod

  echo "builds image on production"
  ssh -t ${PROD_HOST} \
    sudo podman build \
      -f /mnt/msata/build/prod/Dockerfile \
      --target=prod \
      -t acbilson/micropub:alpine-3.12 \
      /mnt/msata/build/prod
;;

*)
  echo "please provide one of the following as the first argument: dev, uat, prod."
  exit 1

esac
