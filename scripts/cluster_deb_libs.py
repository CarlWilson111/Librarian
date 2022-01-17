#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Xu Meiqiu"
__license__ = "GPL"
__version__ = "2.0"

#Extracts biniares from apps and clusters them based on their sha256
import os
import subprocess
import json
import hashlib
import shutil
import time

apps_dir="../sample_debs"
dest_folder = "../UnknownLibs_bins"
start_time=time.time()

def do_temp(temp_dir, deb_name):
    for folder, _, libs in os.walk(temp_dir):
        for lib in libs:
            if lib.endswith(".so"):
                lib_path = os.path.join(folder, lib)
                if not os.path.exists(lib_path): # In case of the link target does not exist
                    print("Lib file {} was a link file and the target doesn't exist!".format(lib_path))
                    continue
                with open(lib_path, "rb") as f:
                    # For each binary under /lib, generate its corresponding hash code
                    bytes = f.read()
                    cluster_name = hashlib.sha256(bytes).hexdigest()

                    # Create a new directory with binary hash_code (if such folder does not exist), and copy binary to that folder
                    renamed_native = lib[:-3] + "_" + deb_name + ".so"
                    cluster_name = os.path.join(dest_folder, cluster_name)
                    if (not (os.path.exists(cluster_name))):
                        os.mkdir(cluster_name)
                    else:
                        if (not (os.path.exists(os.path.join(cluster_name, renamed_native)))):
                            print("Cluster folder existed!")
                    print("Moving binary {} to cluster {}".format(lib_path, os.path.basename(cluster_name)))
                    shutil.move(lib_path, os.path.join(cluster_name, renamed_native))

print("--- Start Clustering Deb Binaries based on their sha256 ---")
for folder,_,debs in os.walk(apps_dir):
    for deb in debs:
        if deb.endswith(".deb"):
            subprocess.call(["rm", "-r", "temp"])

            # Iterates and unzips each .apk per app
            print("Extracting binaries from {}...".format(os.path.basename(deb)))
            subprocess.call(["dpkg -X %s %s" % (os.path.join(folder,deb),"temp")],
                        shell = True,
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.STDOUT)
            do_temp("temp", os.path.basename(deb))
            # for binary in os.listdir("temp"):
            #     if binary.endswith(".so"):
            #         with open(os.path.join("temp",binary),"rb") as f:
            #             # For each binary under /lib, generate its corresponding hash code
            #             bytes = f.read()
            #             cluster_name = hashlib.sha256(bytes).hexdigest()
            #
            #             # Create a new directory with binary hash_code (if such folder does not exist), and copy binary to that folder
            #             renamed_native=binary[:-3]+".so"
            #             cluster_name=os.path.join(dest_folder,cluster_name)
            #             if(not(os.path.exists(cluster_name))):
            #                 os.mkdir(cluster_name)
            #             print("Moving binary {} to cluster {}".format(binary[:-3],os.path.basename(cluster_name)))
            #             shutil.move(os.path.join("temp",binary),os.path.join(cluster_name,renamed_native))

        print("-"*65)

end_time=time.time()

print("--- Total execution time:{:.2f} sec ---".format(end_time-start_time))
