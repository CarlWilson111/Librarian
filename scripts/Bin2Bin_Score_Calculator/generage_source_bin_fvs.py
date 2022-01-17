

import os

KnownLibs_FVs = "../../KnownLibs_FVs"
lines = []

for folder, _, libfvs in os.walk(KnownLibs_FVs):
    for libfv in libfvs:
        if libfv.endswith(".json"):
            lines.append(libfv + "\n")
            #fp.write(os.path.basename(folder) +"/" + lib)

with open("source_bin_FVS.txt", "w") as fp:
    fp.writelines(lines)