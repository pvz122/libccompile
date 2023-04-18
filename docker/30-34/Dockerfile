FROM gcc:9.1

# Install dependencies
RUN \ 
    apt-get update && \ 
    DEBIAN_FRONTEND=noninteractive apt-get install -y gawk bison && \ 
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
