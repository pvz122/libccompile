# libccompile

libccompile is a tool for compiling all versions of GUN Libc. It now supports compiling versions from 2.4 to 2.37 for X86_64.

## Why libccompile

Glibc is a tricky beast to compile. It has a lot of dependencies and a lot of options. Especially when you want to compile an older version of Glibc, you will need to spend a lot of effort to meet all the dependencies for gcc and ld.

libccompile is a tool that can help you compile all versions of Glibc. It is based on docker, so you don't need to worry about the dependencies. It will automatically download the glibc source code and compile it for you.

## Usage

1. Make sure you have installed docker, tar and gzip. If you are using Ubuntu, you can install them by running `sudo apt install docker.io tar gzip`. Then download the latest release of libccompile from release page.

2. Run `./libccompile help` to see the usage:
    
    ```bash
    ~/build►./libccompile help                                            

    Usage: libccompile COMMAND [ARGS]

    Commands:
        all     Compile all versions of glibc, from 2.4 to 2.37

        range   Compile a range of versions of glibc
                usage: libccompile range <min version-max version>
                example: libccompile range 2.15-2.37

        current Compile the current version of your glibc source
                usage: libccompile current <path to glibc source>
                example: libccompile current /home/user/glibc

        build   Build the docker image from the Dockerfile instead of pulling it from dockerhub

        clean   Clean all docker images, you may download or build them if you want to compile again

        help    Show this help message
    ```

3. Run `./libccompile all` to compile all versions of Glibc. It will take a long time to compile all versions. You can also run `./libccompile range <min version-max version>` to compile a range of versions. For example, `./libccompile range 2.15-2.37` will compile all versions from 2.15 to 2.37.

4. After the compilation is finished, you can find the compiled binaries in current directory. The binaries are named as `glibc_<min version>-<max version>.tar.gz`.

5. You may want to clean the docker images after the compilation. Run `./libccompile clean` to clean all docker images.

## Advanced

### Compile your own glibc source

If you want to compile your own glibc source (for you may have some patches), you can run `./libccompile current <path to glibc source>`.

### Build the docker image from the Dockerfile

If you want to build the docker image from the Dockerfile, you can run `./libccompile build`. It will take a long time to build the docker image.