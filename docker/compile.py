#! /usr/bin/python3
# requires: glibc source repository at ./src (https://sourceware.org/git/glibc.git)
#           binutils gcc g++ make gawk realpath git python3 bison(for >= 2.21)
# outputs:  glibc binaries at ./<version>/

import os
import sys
import json
import shutil
import subprocess

default_path = "/glibc"
meta = []
hostname = subprocess.check_output(["hostname"]).decode("utf-8").strip()
use_current_version = False


# load build_meta.json to restore the build status
if os.path.exists("build_meta.json"):
    with open("build_meta.json", "r") as f:
        meta = json.load(f)
else:
    # if version arg passed by command line
    if len(sys.argv) == 3:
        min_version = sys.argv[1]
        max_version = sys.argv[2]
    else:
        # if version arg not passed by command line
        min_version = input("Compile start from version: ")
        max_version = input("to version: ")

    # when $min_version = $max_version = 0, use current version
    if min_version == "0" and max_version == "0":
        use_current_version = True
        meta.append({"version": "current", "compiled": False})
    else:
        if len(min_version.split(".")) != 2 or len(max_version.split(".")) != 2:
            print("[ERR] Invalid version number.")
            exit(1)
        if int(min_version.split(".")[0]) != 2 or int(max_version.split(".")[0]) != 2:
            print("[ERR] libccompile only supports glibc 2.x.")
            exit(1)
        for i in range(
            int(min_version.split(".")[1]), int(max_version.split(".")[1]) + 1
        ):
            meta.append({"version": "2.{}".format(i), "compiled": False})

    # write build_meta.json
    with open("build_meta.json", "w") as f:
        json.dump(meta, f, indent=4)

for glibc in meta:
    # skip versions that have been built
    if glibc["compiled"]:
        print("Version {} has been compiled.".format(glibc["version"]))
        continue

    print("\n\n[BEG] Compiling glibc {}...".format(glibc["version"]))
    os.chdir(default_path)

    # get source
    print("[1/6] Getting the source code...")
    if not os.path.exists("src"):
        print("[ERR] Source code directory not exist.")
        exit(1)
    os.chdir(default_path + "/src")
    if not use_current_version:
        retv = subprocess.call(
            ["git", "checkout", "-f", "glibc-{}".format(glibc["version"])]
        )
        if retv != 0:
            print("[ERR] Failed to checkout glibc-{}".format(glibc["version"]))
            continue
    os.chdir(default_path)

    # mkdir build
    print("[2/6] Creating build directory...")
    if os.path.exists("build"):
        shutil.rmtree("build")
    os.mkdir("build")
    os.chdir("build")

    # configure, make, make install
    print("[3/6] Configuring...")
    # write stdout to log file
    with open("../configure-{}.log".format(glibc["version"]), "w") as f:
        retv = subprocess.call(
            ["../src/configure", "--disable-werror", "--prefix="],
            stdout=f,
            stderr=subprocess.STDOUT,
        )
    if retv != 0:
        print(
            "[ERR] Configure failed. Please check {}:/glibc/configure-{}.log for more information.".format(
                hostname, glibc["version"]
            )
        )
        continue
    os.remove("../configure-{}.log".format(glibc["version"]))

    print("[4/6] Building...")
    with open("../make-{}.log".format(glibc["version"]), "w") as f:
        retv = subprocess.call(["make", "-j4"], stdout=f, stderr=subprocess.STDOUT)
    if retv != 0:
        print(
            "[ERR] Make failed. Please check {}:/glibc/make-{}.log for more information.".format(
                hostname, glibc["version"]
            )
        )
        continue
    os.remove("../make-{}.log".format(glibc["version"]))

    print("[5/6] Installing...")
    # mkdir install directory
    if os.path.exists("../{}".format(glibc["version"])):
        shutil.rmtree("../{}".format(glibc["version"]))
    os.mkdir("../{}".format(glibc["version"]))
    install_path = os.path.realpath("../{}".format(glibc["version"]))

    with open("../make-install-{}.log".format(glibc["version"]), "w") as f:
        retv = subprocess.call(
            [
                "make",
                "DESTDIR={}".format(install_path),
                "install_root={}".format(install_path),
                "install",
            ],
            stdout=f,
            stderr=subprocess.STDOUT,
        )
    if retv != 0:
        print(
            "[ERR] Make install failed. Please check {}:/glibc/make-install-{}.log for more information.".format(
                hostname, glibc["version"]
            )
        )
        continue
    os.remove("../make-install-{}.log".format(glibc["version"]))

    # rm build directory
    print("[6/6] Cleaning...")
    os.chdir(default_path)
    shutil.rmtree("build")

    print("[SUC] glibc {} has been compiled.".format(glibc["version"]))
    glibc["compiled"] = True

    # write build_meta.json
    os.chdir(default_path)
    with open("build_meta.json", "w") as f:
        json.dump(meta, f, indent=4)

# pack all versions
print("\n\n[BEG] Packing all versions into archive...")
os.chdir(default_path)
if use_current_version:
    retv = subprocess.call(["tar", "cf", "current.tar", "current"])
else:
    version_to_pack = []
    for glibc in meta:
        if glibc["compiled"]:
            version_to_pack.append(glibc["version"])
    tar_cmd = [
        "tar",
        "cf",
        "{}-{}.tar".format(meta[0]["version"], meta[-1]["version"]),
    ]
    tar_cmd.extend(version_to_pack)
    retv = subprocess.call(tar_cmd)

if retv != 0:
    print("[ERR] Failed to pack all versions.")
    print("\n\n[DON] Done, but you may have to pack the compiled files yourself.")
else:
    print("[SUC] All versions have been packed.")
    if use_current_version:
        print(
            "\n\n[DON] All done, you can run `docker cp {}:/glibc/current.tar .` to get the compiled files.".format(
                hostname
            )
        )
    else:
        print(
            "\n\n[DON] All done, you can run `docker cp {}:/glibc/{}-{}.tar .` to get the compiled files.".format(
                hostname, meta[0]["version"], meta[-1]["version"]
            )
        )
