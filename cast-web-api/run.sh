#!/bin/ash

docker build -t cast-web-api:latest .

docker run \
--name castwebapi \
--net=host
-p 3001:3001 \
cast-web-api:latest