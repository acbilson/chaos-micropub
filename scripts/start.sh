#!/bin/sh
. .env

docker run --rm \
  --expose $EXPOSED_PORT -p $EXPOSED_PORT:80 \
  --env-file .env --name micropub \
  -v ~/source/alexbilson.dev/hugo/config:/etc/hugo \
  -v ~/source/chaos-content:/mnt/chaos/content \
  -v ~/source/chaos-theme:/mnt/chaos/themes/chaos \
  acbilson/micropub:alpine-3.12

