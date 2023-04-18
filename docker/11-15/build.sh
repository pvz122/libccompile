#! /bin/bash

docker pull debian:6.0.8

cd ..
docker build -t pvz122/libccompile:11-15 -f ./11-15/Dockerfile .
