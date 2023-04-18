#!/usr/bin/perl

use POSIX qw(dup2);
use Sys::Hostname;

# script cwd
$default_path = "/glibc";
$hostname = hostname();
$use_current_version = 0;

# if version arg passed by command line
if ($#ARGV == 1){
    $min_version = $ARGV[0];
    $max_version = $ARGV[1];
} else {
    # if version arg not passed by command line
    print("Compile start from version: ");
    $min_version = <STDIN>;
    chomp($min_version);
    print("to version: ");
    $max_version = <STDIN>;
    chomp($max_version);
}

# when $min_version = $max_version = 0, use current version
if ($min_version == '0' && $max_version == '0'){
    $use_current_version = 1;
} else {
    # split version by "." and get the second element
    @min_versio_a = split(/\./, $min_version);
    $min_version = $min_versio_a[1];
    @max_version_a = split(/\./, $max_version);
    $max_version = $max_version_a[1];
}


for ($i = $min_version; $i <= $max_version; $i++){
    if ($use_current_version == 1){
        $version = "current";
    } else {
        $version = "2." . $i;
    }
    print("\n\n[BEG] Compiling glibc " . $version . "...");

    # change to source code directory
    chdir($default_path);
    chdir("./src");

    # checkout the version
    print("\n[1/6] Getting the source code...");
    if ($use_current_version == 0){
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
    print("\n[4/6] Building...");
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
    print("\n[5/6] Installing...");
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

    print("\n[SUC] glibc " . $version . " has been compiled.");
}   

# pack all versions
print("\n\n[BEG] Packing all versions into archive...");
chdir($default_path);
$pid = fork();
if ($pid == 0){
    if ($use_current_version == 1){
        exec("tar cf current.tar current");
    } else {
        exec("tar cf 2.". $min_version ."-2.". $max_version . ".tar 2.*");
    }
} else {
    waitpid($pid, 0);
}
if ($? != 0){
    print("\n[Err] Failed to pack all versions.");
    print("\n\n[DON] Done, but you may have to pack the compiled files yourself.");
} else {
    print("\n[SUC] All versions have been packed.");
    if ($use_current_version == 1){
        print("\n\n[DON] All done, you can run \"docker cp ".$hostname.":/glibc/current.tar .\" to get the compiled files.\n");
    } else {
        print("\n\n[DON] All done, you can run \"docker cp ".$hostname.":/glibc/2.".$min_version."-2.".$max_version.".tar .\" to get the compiled files.\n");
    }
}