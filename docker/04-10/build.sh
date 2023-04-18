#! /bin/bash

docker pull pvz122/debian:4.0

cd ..
docker build -t pvz122/libccompile:04-10 -f ./04-10/Dockerfile .
