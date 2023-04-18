FROM gcc:12

# Install dependencies
RUN \ 
    # echo "deb http://mirrors.cloud.tencent.com/debian bullseye main" >/etc/apt/sources.list && \
    apt-get update && \ 
    DEBIAN_FRONTEND=noninteractive apt-get install -y bison gawk && \ 
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
