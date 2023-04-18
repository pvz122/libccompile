# libccompile 23-29

This image compiles glibc `2.23 - 2.29`. It is based on Debian 8.0 Jessie and uses gcc version `5.3.0` and ld version  `2.25`.

## Usage

1. Run container using:

   ```shell
   docker run -it --name=CONTAINER_NAME pvz122/libccompile:23-29
   ```

   `CONTAINER_NAME` can be casual.

2. Input the version range you want to compile:

   ```
   Compile start from version: MIN_VERSION
   to version: MAX_VERSION
   ```

   e.g:

   ```
   Compile start from version: 2.23
   to version: 2.29
   ```

3. After compiling, get the binary archive using:

   ```shell
   docker cp CONTAINER_NAME:/glibc/MIN_VERSION-MAX_VERSION.tar .
   ```

4. Finally, clean it by:

   ```shell
   docker rm CONTAINER_NAME
   docker rmi pvz122/libccompile:23-29
   docker rmi gcc:5.3
   ```

## Advanced Usage

You can compile your own glibc source using:

```shell
docker run -it --name=CONTAINER_NAME -v GLIBC_SOURCE_PATH:/glibc/src pvz122/libccompile:23-29
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

This may fail if your glibc source is not based on version  `2.23 - 2.29`.
