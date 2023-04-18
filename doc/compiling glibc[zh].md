# 编译 glibc

[TOC]



## 通用流程

1. 下载源码

    `git clone https://sourceware.org/git/glibc.git src`

    `cd src`

2. 切换到目标版本分支

    `git checkout release/{GLIBC_VERSION}/master`

3. 创建编译临时文件目录

    `mkdir ../build`

    `cd ../build`

4. configure

    `../src/configure --disable-werror --prefix=`

5. make

    `make`

6. 创建二进制文件目录

    `mkdir ../{GLIBC_VERSION}`

7. make install

    `make install DESTDIR={realpath ../{GLIBC_VERSION}}`

8. 清理

    `cd ../src`

    `rm -rf ../build`

9. 跳到第 2 步

编译好后的目录结构：

```
total 32K
drwxrwxr-x  2 pvz122 pvz122 4.0K Mar 26 07:38 bin
drwxrwxr-x  2 pvz122 pvz122 4.0K Mar 26 07:38 etc
drwxrwxr-x 21 pvz122 pvz122 4.0K Mar 26 07:38 include
drwxrwxr-x  4 pvz122 pvz122 4.0K Mar 26 07:38 lib
drwxrwxr-x  3 pvz122 pvz122 4.0K Mar 26 07:38 libexec
drwxrwxr-x  2 pvz122 pvz122 4.0K Mar 26 07:38 sbin
drwxrwxr-x  4 pvz122 pvz122 4.0K Mar 26 07:38 share
drwxrwxr-x  3 pvz122 pvz122 4.0K Mar 26 07:38 var
```

```
lib
├── audit
│   └── sotruss-lib.so
├── crt1.o
├── crti.o
├── crtn.o
├── gconv
│   ├── ANSI_X3.110.so
...
│   └── VISCII.so
├── gcrt1.o
├── ld-2.27.so
├── ld-linux-x86-64.so.2 -> ld-2.27.so
├── libanl-2.27.so
├── libanl.a
├── libanl.so -> libanl.so.1
├── libanl.so.1 -> libanl-2.27.so
├── libBrokenLocale-2.27.so
├── libBrokenLocale.a
├── libBrokenLocale.so -> libBrokenLocale.so.1
├── libBrokenLocale.so.1 -> libBrokenLocale-2.27.so
├── libc-2.27.so
├── libc.a
├── libcidn-2.27.so
├── libcidn.so -> libcidn.so.1
├── libcidn.so.1 -> libcidn-2.27.so
├── libc_nonshared.a
├── libcrypt-2.27.so
├── libcrypt.a
├── libcrypt.so -> libcrypt.so.1
├── libcrypt.so.1 -> libcrypt-2.27.so
├── libc.so
├── libc.so.6 -> libc-2.27.so
├── libdl-2.27.so
├── libdl.a
├── libdl.so -> libdl.so.2
├── libdl.so.2 -> libdl-2.27.so
├── libg.a
├── libm-2.27.a
├── libm-2.27.so
├── libm.a
├── libmcheck.a
├── libmemusage.so
├── libm.so
├── libm.so.6 -> libm-2.27.so
├── libmvec-2.27.so
├── libmvec.a
├── libmvec_nonshared.a
├── libmvec.so -> libmvec.so.1
├── libmvec.so.1 -> libmvec-2.27.so
├── libnsl-2.27.so
├── libnsl.so.1 -> libnsl-2.27.so
├── libnss_compat-2.27.so
├── libnss_compat.so -> libnss_compat.so.2
├── libnss_compat.so.2 -> libnss_compat-2.27.so
├── libnss_db-2.27.so
├── libnss_db.so -> libnss_db.so.2
├── libnss_db.so.2 -> libnss_db-2.27.so
├── libnss_dns-2.27.so
├── libnss_dns.so -> libnss_dns.so.2
├── libnss_dns.so.2 -> libnss_dns-2.27.so
├── libnss_files-2.27.so
├── libnss_files.so -> libnss_files.so.2
├── libnss_files.so.2 -> libnss_files-2.27.so
├── libnss_hesiod-2.27.so
├── libnss_hesiod.so -> libnss_hesiod.so.2
├── libnss_hesiod.so.2 -> libnss_hesiod-2.27.so
├── libpcprofile.so
├── libpthread-2.27.so
├── libpthread.a
├── libpthread_nonshared.a
├── libpthread.so
├── libpthread.so.0 -> libpthread-2.27.so
├── libresolv-2.27.so
├── libresolv.a
├── libresolv.so -> libresolv.so.2
├── libresolv.so.2 -> libresolv-2.27.so
├── librt-2.27.so
├── librt.a
├── librt.so -> librt.so.1
├── librt.so.1 -> librt-2.27.so
├── libSegFault.so
├── libthread_db-1.0.so
├── libthread_db.so -> libthread_db.so.1
├── libthread_db.so.1 -> libthread_db-1.0.so
├── libutil-2.27.so
├── libutil.a
├── libutil.so -> libutil.so.1
├── libutil.so.1 -> libutil-2.27.so
├── Mcrt1.o
└── Scrt1.o

2 directories, 339 files
```

更改可执行文件 libc 版本：

`patchelf --set-interpreter {PATH_TO_GLIBCS}/{GLIBC_VERSION}/lib/ld-linux-x86-64.so.2 --set-rpath {PATH_TO_GLIBCS}/{GLIBC_VERSION}/lib {PATH_TO_EXECUTABLE}`



## 编译器及依赖

gawk 是所有版本的依赖

| glibc版本 | 年份 | gcc最低版本 | gcc推荐版本 | ld最低版本 | ld推荐版本 | bison | python3 |
| --------- | ---- | ----------- | ----------- | ---------- | ---------- | ----- | ------- |
| 2.3       | 2002 | 3.2         | 3.2         | 2.10.1     | 2.10.1     | no    | no      |
| 2.4       | 2006 | 3.4         | 4.1         | 2.15       | 2.15       | no    | no      |
| 2.5       | 2006 | 3.4         | 4.1         | 2.15       | 2.15       | no    | no      |
| 2.6       | 2007 | 3.4         | 4.1         | 2.15       | 2.15       | no    | no      |
| 2.7       | 2007 | 3.4         | 4.1         | 2.15       | 2.15       | no    | no      |
| 2.8       | 2008 | 3.4         | 4.1         | 2.15       | 2.15       | no    | no      |
| 2.9       | 2008 | 3.4         | 4.1         | 2.15       | 2.15       | no    | no      |
| 2.10      | 2009 | 3.4         | 4.1         | 2.15       | 2.15       | no    | no      |
| 2.11      | 2009 | 3.4         | 4.1         | 2.15       | 2.15       | no    | no      |
| 2.12      | 2010 | 3.4         | 4.1         | 2.15       | 2.15       | no    | no      |
| 2.13      | 2011 | 3.4         | 4.1         | ?          | ?          | no    | no      |
| 2.14      | 2011 | 3.4         | 4.1         | ?          | ?          | no    | no      |
| 2.15      | 2012 | 3.4         | 4.1         | ?          | ?          | no    | no      |
| 2.16      | 2012 | 4.3         | 4.6         | 2.20       | 2.20       | no    | no      |
| 2.17      | 2012 | 4.3         | 4.6         | 2.20       | 2.20       | no    | no      |
| 2.18      | 2013 | 4.4         | 4.6         | 2.20       | 2.20       | no    | no      |
| 2.19      | 2014 | 4.4         | 4.6         | 2.20       | 2.20       | no    | no      |
| 2.20      | 2012 | 4.4         | 4.6         | 2.20       | 2.20       | no    | no      |
| 2.21      | 2015 | 4.6         | 4.9.2       | 2.22       | 2.25       | yes   | no      |
| 2.22      | 2015 | 4.6         | 4.9.2       | 2.22       | 2.25       | yes   | no      |
| 2.23      | 2016 | 4.7         | 5.3         | 2.22       | 2.25       | yes   | no      |
| 2.24      | 2016 | 4.7         | 5.3         | 2.22       | 2.25       | yes   | no      |
| 2.25      | 2017 | 4.7         | 6.3         | 2.22       | 2.25       | yes   | no      |
| 2.26      | 2017 | 4.9         | 7.1         | 2.25       | 2.27       | yes   | no      |
| 2.27      | 2018 | 4.9         | 7.3         | 2.25       | 2.29.1     | yes   | no      |
| 2.28      | 2018 | 4.9         | 8.1.1       | 2.25       | 2.31.1     | yes   | no      |
| 2.29      | 2019 | 5           | 8.2.1       | 2.25       | 2.31.1     | yes   | yes     |
| 2.30      | 2019 | 6.2         | 9.1.1       | 2.25       | 2.31.1     | yes   | yes     |
| 2.31      | 2020 | 6.2         | 9.2.1       | 2.25       | 2.32       | yes   | yes     |
| 2.32      | 2020 | 6.2         | 9.2.1       | 2.25       | 2.32       | yes   | yes     |
| 2.33      | 2021 | 6.2         | 10.2        | 2.25       | 2.35.1     | yes   | yes     |
| 2.34      | 2021 | 6.2         | 11.2        | 2.25       | 2.35.1     | yes   | yes     |
| 2.35      | 2022 | 6.2         | 12.0        | 2.25       | 2.37       | yes   | yes     |
| 2.36      | 2022 | 6.2         | 12.1        | 2.25       | 2.38       | yes   | yes     |
| 2.37      | 2023 | 6.2         | 13.0        | 2.25       | 2.39       | yes   | yes     |



## 编译

### ~~2.4 - 2.15~~ 2.4 - 2.10

*尽管官方 INSTALL 文件声称 2.11-2.15 也推荐使用 gcc 4.1 版本和 ld 2.15 版本，但这个版本下 configure 会出现 assembler too old 报错。*

glibc 2.4 - 2.15 都推荐采用 gcc 4.1，这个版本的 gcc 太过古早 (2006年左右发布)，采用虚拟机运行 Debian 4.0 Etch (2007年发行) 编译。

Debian Etch 下载地址：http://cdimage.debian.org/mirror/cdimage/archive/4.0_r0/amd64/iso-cd/

安装好后，更新 apt 源：

`echo 'deb http://archive.debian.org/debian-archive/debian/ etch main' > /etc/apt/sources.list`

`apt-get update`

安装依赖：

`apt-get install binutils gcc g++ make gawk realpath`

Debian Etch 默认安装的是 gcc 4.1.2

编译：

```shell
# ./build for working directory, ./src for source code, and ./$VERSION for output binary
../src/configure --disable-werror --prefix=""
make -j4
make install_root=`realpath ../$VERSION` DESTDIR=`realpath ../$VERSION` install
```

#### Perl 脚本批量编译

Debian Etch 的 git 版本太低了，无法识别 glibc 的仓库。从源码编译安装 git 1.8：https://mirrors.edge.kernel.org/pub/software/scm/git/

安装好一些依赖后：

```shell
make configure
./configure --prefix=/usr
make
sudo make install
```

Etch 发布于2007年，python3 发布于2008年，所以写了个 perl 脚本编译：

```perl
#!/usr/bin/perl

use POSIX qw(dup2);
# script cwd
$default_path = $ENV{'PWD'};

print("Compile start from version: 2.");
$min_version = <STDIN>;
chomp($min_version);
print("to version: 2.");
$max_version = <STDIN>;
chomp($max_version);

for ($i = $min_version; $i <= $max_version; $i++){
    $version = "2." . $i;
    print("\n\nCompiling " . $version . "...");

    # change to source code directory
    chdir($default_path);
    chdir("./src");

    # checkout the version
    print("\n[1/6] Checkout glibc " . $version . "...");
    $pid = fork();
    if ($pid == 0){
        exec("git checkout -f glibc-" . $version);
    } else {
        waitpid($pid, 0);
    }
    if ( $? != 0 ){
        print("\n[Err] Git checkout failed!");
        next;
    }
    chdir($default_path);

    # mkdir build
    print("\n[2/6] Create build directory...");
    if(-d "./build"){
        system("rm -rf ./build");
    }
    mkdir("./build");

    # configure
    print("\n[3/6] Configure...");
    chdir("./build");
    # open file configure-version.log
    open(CONFLOG, ">../configure-" . $version . ".log");
    $pid = fork();
    if ($pid == 0){
        dup2(fileno(CONFLOG), fileno(STDOUT));
        dup2(fileno(CONFLOG), fileno(STDERR));
        exec("../src/configure --disable-werror --prefix=");
    } else {
        waitpid($pid, 0);
    }
    close(CONFLOG);
    if ($? != 0){
        print("\n[Err] Configure failed!");
        next;
    }
    system("rm -f ../configure-" . $version . ".log");

    # make
    print("\n[4/6] Make...");
    # open file make-version.log
    open(MAKELOG, ">../make-" . $version . ".log");
    $pid = fork();
    if ($pid == 0){
        dup2(fileno(MAKELOG), fileno(STDOUT));
        dup2(fileno(MAKELOG), fileno(STDERR));
        exec("make -j4");
    } else {
        waitpid($pid, 0);
    }
    close(MAKELOG);
    if ($? != 0){
        print("\n[Err] Make failed!");
        next;
    }
    system("rm -f ../make-" . $version . ".log");

    # make install
    print("\n[5/6] Make install...");
    # mkdir ../version
    if(-d "../" . $version){
        system("rm -rf ../" . $version);
    }
    mkdir("../" . $version);
    $install_path = `realpath ../$version`;
    chomp($install_path);
    # open file make-install-version.log
    open(MAKEINSTALLLOG, ">../make-install-" . $version . ".log");
    $pid = fork();
    if ($pid == 0){
        dup2(fileno(MAKEINSTALLLOG), fileno(STDOUT));
        dup2(fileno(MAKEINSTALLLOG), fileno(STDERR));
        exec("make DESTDIR=". $install_path ." install_root=". $install_path ." install");
    } else {
        waitpid($pid, 0);
    }
    close(MAKEINSTALLLOG);
    if ($? != 0){
        print("\n[Err] Make install failed!");
        next;
    }
    system("rm -f ../make-install-" . $version . ".log");

    # rm build directory
    print("\n[6/6] Cleaning...");
    chdir($default_path);
    system("rm -rf ./build");

    print("\n[SUC] Compile " . $version . " finished!");
}   

print("\n\n[SUC] All versions compiled!");
```

### 2.11 - 2.15

使用 Debian 6.0 Squeeze (2014年发行) 编译 (我也不知道为什么这个版本能编译成功，但是高一个或低一个都不行)。下载地址：http://cdimage.debian.org/mirror/cdimage/archive/6.0.10/amd64/iso-cd/

更新 apt 源：``echo 'deb http://archive.debian.org/debian-archive/debian/ squeeze main' > /etc/apt/sources.list``

安装依赖：`apt-get install binutils gcc g++ make gawk realpath git-core zip unzip`

使用 python3 脚本。

### 2.16 - 2.22

glibc 2.16 - 2.22 使用 Debian 7.0 Wheezy (2013年发行) 编译。

Debian Wheezy 下载地址：http://cdimage.debian.org/mirror/cdimage/archive/7.0.0-live/amd64/iso-hybrid/

安装好后，更新 apt 源：

`echo 'deb http://archive.debian.org/debian-archive/debian/ wheezy main' > /etc/apt/sources.list`

`apt-get update`

安装依赖：

`apt-get install binutils gcc g++ make gawk realpath bison`

Debian Etch 默认安装的是 gcc 4.7.2

编译：

```shell
# ./build for working directory, ./src for source code, and ./$VERSION for output binary
../src/configure --disable-werror --prefix=""
make -j4
make install_root=`realpath ../$VERSION` DESTDIR=`realpath ../$VERSION` install
```

#### Python 脚本批量编译

python3 脚本：

```python
#! /usr/bin/python3
# requires: glibc source repository at ./src (https://sourceware.org/git/glibc.git)
#           binutils gcc g++ make gawk realpath git python3 bison(for >= 2.21)
# outputs:  glibc binaries at ./<version>/

import os
import json
import shutil
import subprocess

default_path = os.path.realpath('.')
meta = []


# load meta_glibc.json to restore the build status
if (os.path.exists("meta_glibc.json")):
    with open("meta_glibc.json", "r") as f:
        meta = json.load(f)
else:
    min_version = input('Compile start from version: ')
    max_version = input('to version: ')

    for i in range(int(min_version.split('.')[1]), int(max_version.split('.')[1]) + 1):
        meta.append({'version': '2.{}'.format(i), 'compiled': False})

    # write meta_glibc.json
    with open("meta_glibc.json", "w") as f:
        json.dump(meta, f, indent=4)

for glibc in meta:
    # skip versions that have been built
    if glibc['compiled']:
        print('Version {} has been compiled.'.format(glibc['version']))
        continue

    print("\n\nCompiling glibc {}...".format(glibc['version']))
    os.chdir(default_path)

    # git source
    print("[1/6] Getting the source code...")
    if (not os.path.exists("src")):
        print('[ERR] Source code directory not exist.')
        continue
    os.chdir(default_path + "/src")
    retv = subprocess.call(
        ["git", "checkout", "-f", "glibc-{}".format(glibc['version'])])
    if (retv != 0):
        print("[ERR] Failed to checkout glibc-{}".format(glibc['version']))
        continue
    os.chdir(default_path)

    # mkdir build
    print("[2/6] Creating build directory...")
    if (os.path.exists("build")):
        shutil.rmtree("build")
    os.mkdir("build")
    os.chdir("build")

    # configure, make, make install
    print("[3/6] Configuring...")
    # write stdout to log file
    with open("../configure-{}.log".format(glibc['version']), "w") as f:
        retv = subprocess.call(
            ["../src/configure", "--disable-werror", "--prefix="], stdout=f, stderr=subprocess.STDOUT)
    if (retv != 0):
        print(
            "[ERR] Configure failed. Please check configure-{}.log for more information.".format(glibc['version']))
        continue
    os.remove("../configure-{}.log".format(glibc['version']))

    print("[4/6] Building...")
    with open("../make-{}.log".format(glibc['version']), "w") as f:
        retv = subprocess.call(["make", "-j4"], stdout=f,
                               stderr=subprocess.STDOUT)
    if (retv != 0):
        print(
            "[ERR] Make failed. Please check make-{}.log for more information.".format(glibc['version']))
        continue
    os.remove("../make-{}.log".format(glibc['version']))

    print("[5/6] Installing...")
    # mkdir install directory
    if (os.path.exists("../{}".format(glibc['version']))):
        shutil.rmtree("../{}".format(glibc['version']))
    os.mkdir("../{}".format(glibc['version']))
    install_path = os.path.realpath("../{}".format(glibc['version']))

    with open("../make-install-{}.log".format(glibc['version']), "w") as f:
        retv = subprocess.call(
            ["make", "DESTDIR={}".format(install_path), "install_root={}".format(install_path), "install"], stdout=f, stderr=subprocess.STDOUT)
    if (retv != 0):
        print(
            "[ERR] Make install failed. Please check make-install-{}.log for more information.".format(glibc['version']))
        continue
    os.remove("../make-install-{}.log".format(glibc['version']))

    # rm build directory
    print("[6/6] Cleaning...")
    os.chdir("..")
    shutil.rmtree("build")

    print("[SUC] glibc {} has been compiled.".format(glibc['version']))
    glibc['compiled'] = True

    # write meta_glibc.json
    os.chdir(default_path)
    with open("meta_glibc.json", "w") as f:
        json.dump(meta, f, indent=4)

print("\n\n[DON] All versions have been compiled.")
```



### 2.23 - 2.29

自 gcc 4.9 往上，GNU 就提供了官方 Docker 镜像。在此基础上写个 Dockerfile 就可以很方便地编译了。2.23 - 2.29 使用 gcc 5.3 版本编译，Dockerfile 如下：

```dockerfile
FROM gcc:5.3

# Install dependencies
RUN echo 'deb http://archive.debian.org/debian-archive/debian/ jessie main' > /etc/apt/sources.list\
    && apt-get update\
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --force-yes gawk bison python3 zip unzip

WORKDIR /glibc
COPY src.zip /glibc
COPY GlibcCompile.py /glibc
RUN unzip src.zip
ENTRYPOINT ["/glibc/GlibcCompile.py"]
```

#### Docker 版脚本

```python
#! /usr/bin/python3
# requires: glibc source repository at ./src (https://sourceware.org/git/glibc.git)
#           binutils gcc g++ make gawk realpath git python3 bison(for >= 2.21)
# outputs:  glibc binaries at ./<version>/

import os
import json
import shutil
import subprocess

default_path = '/glibc'
meta = []
hostname = subprocess.check_output(['hostname']).decode('utf-8').strip()


# load meta_glibc.json to restore the build status
if (os.path.exists("meta_glibc.json")):
    with open("meta_glibc.json", "r") as f:
        meta = json.load(f)
else:
    min_version = input('Compile start from version: ')
    max_version = input('to version: ')

    for i in range(int(min_version.split('.')[1]), int(max_version.split('.')[1]) + 1):
        meta.append({'version': '2.{}'.format(i), 'compiled': False})

    # write meta_glibc.json
    with open("meta_glibc.json", "w") as f:
        json.dump(meta, f, indent=4)

for glibc in meta:
    # skip versions that have been built
    if glibc['compiled']:
        print('Version {} has been compiled.'.format(glibc['version']))
        continue

    print("\n\n[BEG] Compiling glibc {}...".format(glibc['version']))
    os.chdir(default_path)

    # get source
    print("[1/6] Getting the source code...")
    if (not os.path.exists("src")):
        print('[ERR] Source code directory not exist.')
        continue
    os.chdir(default_path + "/src")
    retv = subprocess.call(
        ["git", "checkout", "-f", "glibc-{}".format(glibc['version'])])
    if (retv != 0):
        print("[ERR] Failed to checkout glibc-{}".format(glibc['version']))
        continue
    os.chdir(default_path)

    # mkdir build
    print("[2/6] Creating build directory...")
    if (os.path.exists("build")):
        shutil.rmtree("build")
    os.mkdir("build")
    os.chdir("build")

    # configure, make, make install
    print("[3/6] Configuring...")
    # write stdout to log file
    with open("../configure-{}.log".format(glibc['version']), "w") as f:
        retv = subprocess.call(
            ["../src/configure", "--disable-werror", "--prefix="], stdout=f, stderr=subprocess.STDOUT)
    if (retv != 0):
        print(
            "[ERR] Configure failed. Please check {}:/glibc/configure-{}.log for more information.".format(hostname, glibc['version']))
        continue
    os.remove("../configure-{}.log".format(glibc['version']))

    print("[4/6] Building...")
    with open("../make-{}.log".format(glibc['version']), "w") as f:
        retv = subprocess.call(["make", "-j4"], stdout=f,
                               stderr=subprocess.STDOUT)
    if (retv != 0):
        print(
            "[ERR] Make failed. Please check {}:/glibc/make-{}.log for more information.".format(hostname, glibc['version']))
        continue
    os.remove("../make-{}.log".format(glibc['version']))

    print("[5/6] Installing...")
    # mkdir install directory
    if (os.path.exists("../{}".format(glibc['version']))):
        shutil.rmtree("../{}".format(glibc['version']))
    os.mkdir("../{}".format(glibc['version']))
    install_path = os.path.realpath("../{}".format(glibc['version']))

    with open("../make-install-{}.log".format(glibc['version']), "w") as f:
        retv = subprocess.call(
            ["make", "DESTDIR={}".format(install_path), "install_root={}".format(install_path), "install"], stdout=f, stderr=subprocess.STDOUT)
    if (retv != 0):
        print(
            "[ERR] Make install failed. Please check {}:/glibc/make-install-{}.log for more information.".format(hostname, glibc['version']))
        continue
    os.remove("../make-install-{}.log".format(glibc['version']))

    # rm build directory
    print("[6/6] Cleaning...")
    os.chdir(default_path)
    shutil.rmtree("build")

    print("[SUC] glibc {} has been compiled.".format(glibc['version']))
    glibc['compiled'] = True

    # write meta_glibc.json
    os.chdir(default_path)
    with open("meta_glibc.json", "w") as f:
        json.dump(meta, f, indent=4)

# pack all versions
print("\n\n[BEG] Packing all versions into archive...")
os.mkdir("{}-{}".format(meta[0]['version'], meta[-1]['version']))
for glibc in meta:
    if (not glibc['compiled']):
        continue
    shutil.move(glibc['version'], "{}-{}".format(
        meta[0]['version'], meta[-1]['version']))
retv = subprocess.call(['zip', '-r', '{}-{}.zip'.format(meta[0]['version'], meta[-1]['version']),
                       '{}-{}'.format(meta[0]['version'], meta[-1]['version'])], stdout=subprocess.DEVNULL)
if (retv != 0):
    print("[ERR] Failed to pack all versions.")
    print('\n\n[DON] Done, but you may have to pack the compiled files yourself.')
else:
    print("[SUC] All versions have been packed.")
    print("\n\n[DON] All done, you can run `docker cp {}:/glibc/{}-{}.zip .` to get the compiled files.".format(
        hostname, meta[0]['version'], meta[-1]['version']))

```

以下都使用同一个脚本

#### 使用方法

```markdown
# GLibc Compile for version 2.23 - 2.29

1. Build this image using:

   ```shell
   docker build -t glibc_compile:2.23-2.29 .
```

2. Run container using：

   ```shell
   docker run -it --name=CONTAINER_NAME glibc_compile:2.23-2.29
   ```

3. After compiling，get the result zip archive using：

   ```shell
   docker cp CONTAINER_NAME:/glibc/2.23-2.29.zip .
   ```

4. Finally，clean it by：

   ```c
   docker rm CONTAINER_NAME
   docker rmi glibc_compile:2.23-2.29
   ```


以下都类似



### ~~2.30 - 2.37~~ 2.30 - 2.34

*2.35 - 2.37 无法编译*

使用 gcc 9.1，Dockerfile：

```dockerfile
FROM gcc:9.1

# Install dependencies
RUN apt-get update\
    && DEBIAN_FRONTEND=noninteractive apt-get install -y gawk bison zip unzip

WORKDIR /glibc
COPY src.zip /glibc
COPY GlibcCompile.py /glibc
RUN unzip src.zip
ENTRYPOINT ["/glibc/GlibcCompile.py"]
```



### 2.35 - 2.37

使用 gcc 12.0，Dockerfile：

```dockerfile
FROM gcc:12

# Install dependencies
RUN echo "deb http://mirrors.cloud.tencent.com/debian bullseye main" > /etc/apt/sources.list \
    && apt-get update\
    && DEBIAN_FRONTEND=noninteractive apt-get install -y bison gawk zip

WORKDIR /glibc
COPY src.zip /glibc
COPY GlibcCompile.py /glibc
RUN unzip src.zip
ENTRYPOINT ["/glibc/GlibcCompile.py"]
```

