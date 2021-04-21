#!/bin/sh
. .env

docker run --rm \
  --expose ${EXPOSED_PORT} -p ${EXPOSED_PORT}:80 \
  -e "SITE=${DEV_SITE}" \
  -e "CLIENT_ID=${UAT_CLIENT_ID}" \
  -e "CLIENT_SECRET=${UAT_CLIENT_SECRET}" \
  -e "FLASK_SECRET_KEY=${FLASK_SECRET_KEY}" \
  -e "SESSION_SECRET=${SESSION_SECRET}" \
  -v ${CONTENT_PATH}/chaos-content:/mnt/chaos/content \
  -v ${THEME_PATH}/chaos-theme:/mnt/chaos/themes/chaos \
  -v ${SITE_PATH}/site:/var/www/site \
  --name micropub \
  acbilson/micropub-dev:alpine-3.12
