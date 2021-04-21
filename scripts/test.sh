#!/bin/bash
. .env

TEST_TYPE=$1

case $TEST_TYPE in

unit)
  echo "under construction"
;;

smoke)
  echo "under construction"
	curl http://localhost:5000/health --verbose; \
  sleep 1 && docker logs -n 5 micropub
;;

*)
  echo "please provide one of the following as the first argument: unit, smoke."
  exit 1

esac
