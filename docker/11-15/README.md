# libccompile 11-15

This image compiles glibc `2.11 - 2.15`. It is based on Debian 6.0.8 Squeeze and uses gcc version `4.4.5` and ld version `2.20.1`.

## Usage

1. Run container using:

   ```shell
   docker run -it --name=CONTAINER_NAME pvz122/libccompile:11-15
   ```

   `CONTAINER_NAME` can be casual.

2. Input the version range you want to compile:

   ```
   Compile start from version: MIN_VERSION
   to version: MAX_VERSION
   ```

   e.g:

   ```
   Compile start from version: 2.11
   to version: 2.15
   ```

3. After compiling, get the binary archive using:

   ```shell
   docker cp CONTAINER_NAME:/glibc/MIN_VERSION-MAX_VERSION.tar .
   ```

4. Finally, clean it by:

   ```shell
   docker rm CONTAINER_NAME
   docker rmi pvz122/libccompile:11-15
   docker rmi debian:6.0.8
   ```

## Advanced Usage

You can compile your own glibc source using:

```shell
docker run -it --name=CONTAINER_NAME -v GLIBC_SOURCE_PATH:/glibc/src pvz122/libccompile:11-15
```

In which `GLIBC_SOURCE_PATH` is your own glibc source path.

Then, input `0` for both min version and max version. It looks like:

```
Compile start from version: 0
to version: 0
```

After compiling, get the binary archive using:

```shell
docker cp CONTAINER_NAME:/glibc/current.tar .
```

This may fail if your glibc source is not based on version  `2.11 - 2.15`.
