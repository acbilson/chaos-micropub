#!/bin/bash
. .env

ENVIRONMENT=$1

case $ENVIRONMENT in

uat)
  echo "stops container in uat..."
  ssh -t ${UAT_HOST} sudo podman stop micropub-uat
;;

prod)
  echo "stops container in production..."
  ssh -t ${PROD_HOST} sudo systemctl disable micropub
  ssh -t ${PROD_HOST} sudo podman stop micropub
;;

*)
  echo "please provide one of the following as the first argument: uat, prod."
  exit 1

esac
