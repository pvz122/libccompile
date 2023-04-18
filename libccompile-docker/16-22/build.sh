#! /bin/bash

docker pull debian:7.3

cd ..
docker build -t pvz122/libccompile:16-22 -f ./16-22/Dockerfile .
