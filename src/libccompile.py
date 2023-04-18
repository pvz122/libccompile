#! /usr/bin/python3

import os
import sys
import subprocess
import random
import shutil

# --------- constants ---------

help_str = """
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
"""
random_str = str(
    random.randint(100000, 999999)
)  # random string to avoid conflicts with other docker containers


# --------- utility functions ---------


# check if requirements are met
def met_requirements() -> bool:
    # python >= 3.8
    if sys.version_info < (3, 8):
        print("Error: libccompile requires python >= 3.8")
        return False
    # docker usable
    try:
        subprocess.check_output(["docker", "ps"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Error: docker is not installed or not usable")
        return False
    # tar installed
    try:
        subprocess.check_output(["tar", "--version"], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print("Error: tar is not installed")
        return False
    return True


# check if version str is valid
def check_version(version: str) -> bool:
    if len(version.split(".")) != 2:
        print("Error: invalid version")
        return False
    try:
        int(version.split(".")[0])
        int(version.split(".")[1])
    except ValueError:
        print("Error: invalid version")
        return False

    if int(version.split(".")[0]) != 2:
        print("Error: libccompile only supports glibc 2.x")
        return False

    return True


# select the version range to compile
# input: version pair of current min and max version
# output: version range dict for this run
def version_range_selector(version_pair: list) -> dict:
    min_version_num = int(version_pair[0].split(".")[1])
    max_version_num = int(version_pair[1].split(".")[1])
    if min_version_num > max_version_num:
        return None

    if min_version_num <= 10:
        if min_version_num < 4:
            print(
                "Warning: glibc versions below 2.4 are not supported, libccompile will try to compile them using 2.4 config"
            )
        version_pair[0] = "2.11"
        return {
            "min": "2.{}".format(min_version_num),
            "max": "2.{}".format(min(10, max_version_num)),
            "range": "04-10",
        }
    elif min_version_num <= 15:
        version_pair[0] = "2.16"
        return {
            "min": "2.{}".format(min_version_num),
            "max": "2.{}".format(min(15, max_version_num)),
            "range": "11-15",
        }
    elif min_version_num <= 22:
        version_pair[0] = "2.23"
        return {
            "min": "2.{}".format(min_version_num),
            "max": "2.{}".format(min(22, max_version_num)),
            "range": "16-22",
        }
    elif min_version_num <= 29:
        version_pair[0] = "2.30"
        return {
            "min": "2.{}".format(min_version_num),
            "max": "2.{}".format(min(29, max_version_num)),
            "range": "23-29",
        }
    elif min_version_num <= 34:
        version_pair[0] = "2.35"
        return {
            "min": "2.{}".format(min_version_num),
            "max": "2.{}".format(min(34, max_version_num)),
            "range": "30-34",
        }
    else:  # min_version_num >= 35, last run
        if max_version_num > 37:
            print(
                "Warning: glibc versions above 2.37 are not supported, libccompile will try to compile them using 2.37 config"
            )
        version_pair[0] = "2.{}".format(max_version_num + 1)
        return {
            "min": "2.{}".format(min_version_num),
            "max": "2.{}".format(max_version_num),
            "range": "35-37",
        }


# indicate the version of glibc source by version.h
# it contains macro like such: #define VERSION "2.37.9000"
def indicate_version(path: str) -> str:
    if not os.path.exists(os.path.join(path, "version.h")):
        return None
    with open(os.path.join(path, "version.h"), "r") as f:
        for line in f:
            if "VERSION" in line:
                version_num = line.split(".")[1]
                return "2.{}".format(version_num)


# get the specified docker image
def get_docker_image(version_range: str) -> bool:
    # check if docker image exists
    try:
        subprocess.check_output(
            [
                "docker",
                "image",
                "inspect",
                "pvz122/libccompile:{}".format(version_range["range"]),
            ],
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError:
        # pull from dockerhub
        print(
            "Warning: docker image pvz122/libccompile:{} not found, pulling from dockerhub".format(
                version_range["range"]
            )
        )
        ret_code = subprocess.call(
            [
                "docker",
                "pull",
                "pvz122/libccompile:{}".format(version_range["range"]),
            ]
        )
        if ret_code != 0:
            print(
                "Error: docker pull failed when compiling glibc version {} to {}, you may need to build the docker image yourself, try 'libccompile build'".format(
                    version_range["min"], version_range["max"]
                )
            )
            return False

    return True


# --------- main functions ---------


# compile a range of glibc versions
def compile_range(min_version: str, max_version: str):
    # compile glibc versions from min_version to max_version
    version_pair = [min_version, max_version]
    tar_files = []
    while (version_range := version_range_selector(version_pair)) is not None:
        print(
            "Compiling glibc versions {} to {}".format(
                version_range["min"], version_range["max"]
            )
        )

        # get docker image
        if not get_docker_image(version_range):
            continue

        # run docker container
        ret_code = subprocess.call(
            [
                "docker",
                "run",
                "-it",
                "--name",
                "{}-{}_{}".format(
                    version_range["min"], version_range["max"], random_str
                ),
                "pvz122/libccompile:{}".format(version_range["range"]),
                version_range["min"],
                version_range["max"],
            ]
        )
        if ret_code != 0:
            print(
                "Error: docker run failed when compiling glibc version {} to {}".format(
                    version_range["min"], version_range["max"]
                )
            )
            continue

        # copy tar file from container
        ret_code = subprocess.call(
            [
                "docker",
                "cp",
                "{}-{}_{}:/glibc/{}-{}.tar".format(
                    version_range["min"],
                    version_range["max"],
                    random_str,
                    version_range["min"],
                    version_range["max"],
                ),
                "./",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if ret_code != 0:
            print(
                "Error: docker cp failed when compiling glibc version {} to {}".format(
                    version_range["min"], version_range["max"]
                )
            )
            continue
        tar_files.append("{}-{}.tar".format(version_range["min"], version_range["max"]))

        # remove container
        ret_code = subprocess.call(
            [
                "docker",
                "rm",
                "{}-{}_{}".format(
                    version_range["min"], version_range["max"], random_str
                ),
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        if ret_code != 0:
            print(
                "Error: docker rm failed when compiling glibc version {} to {}".format(
                    version_range["min"], version_range["max"]
                )
            )
            continue
        print(
            "Successfully compiled glibc versions {} to {}".format(
                version_range["min"], version_range["max"]
            )
        )

    # pack all tar files into a tar.gz
    if len(tar_files) > 0:
        # GUN tar supports concatenating multiple tar files into one
        if sys.platform == "linux":
            if len(tar_files) > 1:
                # concatenate tar files into first.tar
                # tar --concatenate --file=first.tar second.tar …
                concat_cmd = ["tar", "--concatenate", "--file={}".format(tar_files[0])]
                concat_cmd.extend(tar_files[1:])
                ret_code = subprocess.call(concat_cmd)
                if ret_code != 0:
                    print("Error: tar concatenate failed")
                    return

                # rm second.tar …
                try:
                    for tar_file in tar_files[1:]:
                        os.remove(tar_file)
                except OSError as e:
                    print("Error: rm failed")
                    return

            # compress first.tar into glibc_min-max.tar.gz
            # tar -zcf glibc_min-max.tar.gz first.tar
            ret_code = subprocess.call(
                [
                    "tar",
                    "-zcf",
                    "glibc_{0}-{1}.tar.gz".format(min_version, max_version),
                    tar_files[0],
                ]
            )
            if ret_code != 0:
                print("Error: tar compress failed")
                return

            # rm first.tar
            try:
                os.remove(tar_files[0])
            except OSError as e:
                print("Error: rm failed")
                return

            print(
                "Glibc versions {} to {} are successfully compiled and packed into glibc_{0}-{1}.tar.gz".format(
                    min_version, max_version
                )
            )
        # BSD tar does not support concatenating multiple tar files into one, simply extract all tar files and pack them into one tar.gz
        else:
            os.mkdir("glibc_{0}-{1}".format(min_version, max_version))
            for tar_file in tar_files:
                # extract tar file into glibc_min-max
                ret_code = subprocess.call(
                    [
                        "tar",
                        "-xf",
                        tar_file,
                        "--directory=glibc_{0}-{1}".format(min_version, max_version),
                    ]
                )
                if ret_code != 0:
                    print("Error: tar extract failed")
                    return
                # rm tar file
                try:
                    os.remove(tar_file)
                except:
                    print("Error: rm failed")
                    return

            # pack glibc_min-max into tar.gz
            ret_code = subprocess.call(
                [
                    "tar",
                    "-zcf",
                    "glibc_{0}-{1}.tar.gz".format(min_version, max_version),
                    "glibc_{0}-{1}".format(min_version, max_version),
                ]
            )
            if ret_code != 0:
                print("Error: tar compress failed")
                return
            # rm glibc_min-max
            try:
                shutil.rmtree("glibc_{0}-{1}".format(min_version, max_version))
            except:
                print("Error: rm failed")
                return

            print(
                "Glibc versions {} to {} are successfully compiled and packed into glibc_{0}-{1}.tar.gz".format(
                    min_version, max_version
                )
            )


# compile a custom version of glibc
def compile_current(src_path: str):
    if (version := indicate_version(src_path)) == None:
        print("libccompile can not indicate the version of your glibc source")
        version = input("Please enter the version manually: ")
        if check_version(version) == False:
            print("Error: invalid version")
            return

    # select range
    version_pair = [version, version]
    version_range = version_range_selector(version_pair)

    # get docker image
    if not get_docker_image():
        return

    # compile
    # docker run -it --name=CONTAINER_NAME -v GLIBC_SOURCE_PATH:/glibc/src pvz122/libccompile:35-37
    ret_code = subprocess.call(
        [
            "docker",
            "run",
            "-it",
            "--name=current_{}".format(random_str),
            "-v",
            "{}:/glibc/src".format(src_path),
            "pvz122/libccompile:{}".format(version_range),
            "0",
            "0",
        ]
    )
    if ret_code != 0:
        print("Error: docker run failed")
        return

    # cp compiled glibc to current directory
    ret_code = subprocess.call(
        [
            "docker",
            "cp",
            "current_{}:/glibc/current.tar".format(random_str),
            "./glibc_current.tar",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if ret_code != 0:
        print("Error: docker cp failed")
        return

    # rm docker container
    ret_code = subprocess.call(
        ["docker", "rm", "current_{}".format(random_str)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if ret_code != 0:
        print("Error: docker rm failed")
        return

    # compress glibc_current.tar into glibc_current.tar.gz
    ret_code = subprocess.call(
        ["tar", "-zcf", "glibc_current.tar.gz", "glibc_current.tar"]
    )
    if ret_code != 0:
        print("Error: tar compress failed")
        return

    # rm glibc_current.tar
    try:
        os.remove("glibc_current.tar")
    except OSError as e:
        print("Error: rm failed")
        return

    print(
        "Current glibc source is successfully compiled and packed into glibc_current.tar.gz"
    )


# build docker image
def build_docker():
    if not os.path.exists("docker"):
        print(
            "Error: docker directory not found, you need to get the full source code of libccompile"
        )
        return

    # build docker image
    os.chdir("docker")
    ret_code = subprocess.call("./build.sh")
    if ret_code != 0:
        print("Error: docker build failed")
        return


# clean docker image
def clean_docker():
    # remove docker image
    for version_range in ["04-10", "11-15", "16-22", "23-29", "30-34", "35-37"]:
        try:
            subprocess.call(
                ["docker", "rmi", "pvz122/libccompile:{}".format(version_range)],
            )
        except:
            pass


# deal with arguments, do some sanity check
def main():
    # check if requirements are met
    if not met_requirements():
        exit(1)

    if len(sys.argv) == 1:
        # no command
        print("Error: missing command, try 'libccompile help' for more information")
        exit(1)
    if sys.argv[1] == "all":
        # compile all versions
        compile_range("2.4", "2.37")
    elif sys.argv[1] == "range":
        # compile a range of versions
        if len(sys.argv) < 3:
            # missing arguments
            print(
                "Error: missing arguments, try 'libccompile help' for more information"
            )
            exit(1)
        if len(sys.argv[2].split("-")) != 2:
            # not a valid version range
            print(
                "Error: invalid argument {}, try 'libccompile help' for more information".format(
                    sys.argv[2]
                )
            )
            exit(1)

        min_version, max_version = sys.argv[2].split("-")
        # check if versions are valid
        if check_version(min_version) == False or check_version(max_version) == False:
            exit(1)

        # check if min_version <= max_version
        min_version_num = int(min_version.split(".")[1])
        max_version_num = int(max_version.split(".")[1])
        if min_version_num > max_version_num:
            print(
                "Error: invalid version range {}, min version must be <= max version".format(
                    sys.argv[2]
                )
            )

        # compile the range
        compile_range(min_version, max_version)
    elif sys.argv[1] == "current":
        # compile current version
        if len(sys.argv) < 3:
            # missing path
            print(
                "Error: missing arguments, try 'libccompile help' for more information"
            )
            exit(1)
        # check if path is valid
        if not os.path.isdir(sys.argv[2]):
            print(
                "Error: invalid path {}, try 'libccompile help' for more information".format(
                    sys.argv[2]
                )
            )
            exit(1)

        # compile it
        compile_current(sys.argv[2])
    elif sys.argv[1] == "build":
        # build docker image
        build_docker()
    elif sys.argv[1] == "clean":
        # clean docker image
        clean_docker()
    elif sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        # help
        print(help_str)
    else:
        # not a valid command
        print(
            "Invalid command {}, try 'libccompile help' for more information".format(
                sys.argv[1]
            )
        )
        exit(1)


if __name__ == "__main__":
    main()
