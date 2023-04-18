FROM gcc:5.3

# Install dependencies
RUN \ 
    echo 'deb http://archive.debian.org/debian-archive/debian/ jessie main' >/etc/apt/sources.list && \ 
    apt-get update && \ 
    DEBIAN_FRONTEND=noninteractive apt-get install -y --force-yes gawk bison python3 && \ 
    apt-get clean

# copy script and src
WORKDIR /glibc
COPY glibc-src.tar.gz /glibc
COPY compile.py /glibc
RUN \ 
    cd /glibc && \ 
    tar --no-same-owner --no-same-permissions -xf glibc-src.tar.gz && \ 
    mv glibc-src src && \ 
    rm -rf glibc-src.tar.gz && \ 
    chmod +x compile.py

# entrypoint
ENTRYPOINT ["/glibc/compile.py"]
