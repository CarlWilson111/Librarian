

import os

UnknownLibs_bins = "../../UnknownLibs_bins"
lines = []

for folder, _, libs in os.walk(UnknownLibs_bins):
    for lib in libs:
        if lib.endswith(".so"):
            lines.append(os.path.basename(folder) + "/" + lib + "\n")
            #fp.write(os.path.basename(folder) +"/" + lib)

with open("extracted_bins.txt", "w") as fp:
    fp.writelines(lines)