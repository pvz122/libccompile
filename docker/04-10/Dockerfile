FROM pvz122/debian:4.0

# install dependencies
RUN \ 
echo 'deb http://archive.debian.org/debian-archive/debian/ etch main' >/etc/apt/sources.list && \ 
apt-get update && \ 
apt-get install -y binutils gcc g++ make gawk realpath && \ 
apt-get install -y autoconf zlib1g-dev gettext python && \ 
apt-get clean

# compile and install git
COPY 04-10/git-1.8.2.3.tar /tmp
RUN \ 
cd /tmp && \ 
tar xvf git-1.8.2.3.tar && \ 
cd git-1.8.2.3 && \ 
make configure && \ 
./configure --prefix=/usr && \ 
make && \ 
make install && \ 
cd / && \ 
rm -rf /tmp/git-1.8.2.3 && \ 
rm -rf /tmp/git-1.8.2.3.tar

# copy script and src
WORKDIR /glibc
COPY glibc-src.tar.gz /glibc
COPY compile.pl /glibc
RUN \ 
cd /glibc && \ 
tar xf glibc-src.tar.gz && \ 
mv glibc-src src && \ 
rm -rf glibc-src.tar.gz && \ 
chmod +x compile.pl

# entrypoint
ENTRYPOINT ["/glibc/compile.pl"]
