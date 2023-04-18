#! /bin/bash

# if glibc-src.tar.gz is not present, download it
if [ ! -f glibc-src.tar.gz ]; then
    git clone https://sourceware.org/git/glibc.git glibc-src
    tar czf glibc-src.tar.gz glibc-src/
    rm -rf glibc-src
fi

# build the image
cd 04-10
./build.sh
cd ..

cd 11-15
./build.sh
cd ..

cd 16-22
./build.sh
cd ..

cd 23-29
./build.sh
cd ..

cd 30-34
./build.sh
cd ..

cd 35-39
./build.sh
cd ..

echo "Done."
