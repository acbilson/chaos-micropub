#!/bin/sh
. .env

echo "backing up sensitive .env file"
mkdir -p ~/safe/micropub && cp .env ~/safe/micropub/env.bk

echo "removing /dist"
rm -rf dist/

#docker rm micropub
#rm uwsgi/build-site.sh
