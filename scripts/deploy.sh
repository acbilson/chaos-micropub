#!/bin/bash
. .env

ENVIRONMENT=$1

case $ENVIRONMENT in

uat)
  echo "runs container in uat..."
  ssh -t ${UAT_HOST} \
    sudo podman run --rm -d \
      --expose ${UAT_EXPOSED_PORT} -p ${UAT_EXPOSED_PORT}:80 \
      -e "SITE=${UAT_SITE}" \
      -e "CLIENT_ID=${UAT_CLIENT_ID}" \
      -e "CLIENT_SECRET=${UAT_CLIENT_SECRET}" \
      -e "FLASK_SECRET_KEY=${FLASK_SECRET_KEY}" \
      -e "SESSION_SECRET=${SESSION_SECRET}" \
      -v ${PRD_CONTENT_PATH}/chaos-content:/mnt/chaos/content \
      --name micropub-uat \
      acbilson/micropub-uat:alpine-3.12
;;

prod)
  echo "enabling micropub service..."
  ssh -t ${PROD_HOST} sudo systemctl daemon-reload
  ssh -t ${PROD_HOST} sudo systemctl enable --now container-micropub.service
;;

*)
  echo "please provide one of the following as the first argument: uat, prod."
  exit 1

esac
