#!/bin/bash
. .env

ENVIRONMENT=$1

case $ENVIRONMENT in

dev)
  echo "backing up sensitive .env file"
  mkdir -p ~/safe/micropub && cp .env ~/safe/micropub/env.bk

  echo "removing dist/"
  rm -rf dist/

  echo "removing site/"
  rm -rf site/
;;

uat)
  ssh -t ${UAT_HOST} \
    rm -rf /mnt/msata/build/uat
;;

prod)
  ssh -t ${PROD_HOST} \
    rm -rf /mnt/msata/build/prod
;;

*)
  echo "please provide one of the following as the first argument: dev, uat, prod."
  exit 1

esac
