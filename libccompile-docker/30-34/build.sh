#! /bin/bash

docker pull gcc:9.1

cd ..
docker build -t pvz122/libccompile:30-34 -f ./30-34/Dockerfile .
