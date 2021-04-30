#!/bin/bash
. .env

docker run --rm \
  --expose ${EXPOSED_PORT} -p ${EXPOSED_PORT}:80 \
  -e "SITE=${DEV_SITE}" \
  -e "CLIENT_ID=${UAT_CLIENT_ID}" \
  -e "CLIENT_SECRET=${UAT_CLIENT_SECRET}" \
  -e "FLASK_SECRET_KEY=${FLASK_SECRET_KEY}" \
  -e "SESSION_SECRET=${SESSION_SECRET}" \
  -v ${SITE_PATH}/site:/var/www/site \
  -v ${SOURCE_PATH}/src:/mnt/src \
  --name micropub \
  acbilson/micropub-dev:alpine-3.12
