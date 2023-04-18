#! /usr/bin/python3

import os
import sys

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

    clean   Clean all docker images and containers

    help    Show this help message
"""

def compile_range(min_version: str, max_version: str):
    pass

def compile_current(src_path: str):
    pass

def build_docker():
    pass

def clean_docker():
    pass

def main():
    if len(sys.argv) == 1:
        print("Missing command, try 'libccompile help' for more information")
        exit(1)
    if sys.argv[1] == "all":
        compile_range("2.4", "2.37")
    elif sys.argv[1] == "range":
        if len(sys.argv) < 3:
            print("Missing arguments, try 'libccompile help' for more information")
            exit(1)
        if(len(sys.argv[2].split("-")) != 2):
            print("Invalid argument {}, try 'libccompile help' for more information".format(sys.argv[2]))
            exit(1)
        min_version, max_version = sys.argv[2].split("-")
        if len(min_version.split(".")) != 2 or len(max_version.split(".")) != 2:
            print("Invalid version range {}, try 'libccompile help' for more information".format(sys.argv[2]))
            exit(1)
        if min_version.split(".")[0] != "2" or max_version.split(".")[0] != "2":
            print("Invalid version range {}, libccompile only supports glibc 2.x".format(sys.argv[2]))
            exit(1)

        compile_range(min_version, max_version)
    elif sys.argv[1] == "current":
        if len(sys.argv) < 3:
            print("Missing arguments, try 'libccompile help' for more information")
            exit(1)
        if not os.path.isdir(sys.argv[2]):
            print("Invalid path {}, try 'libccompile help' for more information".format(sys.argv[2]))
            exit(1)
        compile_current(sys.argv[2])
    elif sys.argv[1] == "build":
        build_docker()
    elif sys.argv[1] == "clean":
        clean_docker()
    elif sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        print(help_str)
    else:
        print("Invalid command {}, try 'libccompile help' for more information".format(sys.argv[1]))
        exit(1)


if __name__ == "__main__":
    main()