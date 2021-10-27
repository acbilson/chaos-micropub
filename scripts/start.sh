#!/bin/bash
. .env

ENVIRONMENT=$1

case $ENVIRONMENT in

dev)
docker run --rm \
  --expose ${EXPOSED_PORT} -p ${EXPOSED_PORT}:80 \
  -e "SITE=${DEV_SITE}" \
  -e "CLIENT_ID=${UAT_CLIENT_ID}" \
  -e "CLIENT_SECRET=${UAT_CLIENT_SECRET}" \
  -e "FLASK_SECRET_KEY=${FLASK_SECRET_KEY}" \
  -e "SESSION_SECRET=${SESSION_SECRET}" \
  -e "CONTENT_PATH=${DEV_CONTENT_PATH}" \
  -v ${SITE_PATH}/site:/var/www/site \
  -v ${SOURCE_PATH}/src:/mnt/src \
  -v ${SOURCE_PATH}/content:/mnt/chaos/content \
  --name micropub \
  acbilson/micropub-dev:alpine-3.12
;;

test)
# entrypoint args must come after image name (weird)
docker run --rm \
  -v ${SOURCE_PATH}/src:/mnt/src \
  -v ${SOURCE_PATH}/content:/mnt/chaos/content \
  --name micropub-test \
  --entrypoint "python" \
  acbilson/micropub-dev:alpine-3.12 \
  -m unittest discover tests
;;

*)
  echo "please provide one of the following as the first argument: dev, test."
  exit 1

esac
