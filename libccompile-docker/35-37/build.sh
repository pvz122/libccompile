#! /bin/bash

docker pull gcc:12

cd ..
docker build -t pvz122/libccompile:35-37 -f ./35-37/Dockerfile .
