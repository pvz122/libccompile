FROM debian:7.3

# install dependencies
RUN \ 
echo 'deb http://archive.debian.org/debian-archive/debian/ wheezy main' >/etc/apt/sources.list && \ 
apt-get update && \ 
apt-get install -y --force-yes binutils gcc g++ make gawk bison realpath git-core python3 && \ 
apt-get clean

# copy script and src
WORKDIR /glibc
COPY glibc-src.tar.gz /glibc
COPY compile.py /glibc
RUN \ 
cd /glibc && \ 
tar xf glibc-src.tar.gz && \ 
mv glibc-src src && \ 
rm -rf glibc-src.tar.gz && \ 
chmod +x compile.py

# entrypoint
ENTRYPOINT ["/glibc/compile.py"]
