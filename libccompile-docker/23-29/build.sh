#! /bin/bash

docker pull gcc:5.3

cd ..
docker build -t pvz122/libccompile:23-29 -f ./23-29/Dockerfile .
