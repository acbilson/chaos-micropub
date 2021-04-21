#!/bin/bash
. .env

TEST_TYPE=$1

case $TEST_TYPE in

unit)
  echo "under construction"
;;

smoke)
  echo "under construction"
;;

*)
  echo "please provide one of the following as the first argument: unit, smoke."
  exit 1

esac
