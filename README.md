# Librarian

This repository contains:
* Librarian, a tool designed to identify native libraries and their versions as found in Android apps based on our novel similarity metric bin2sim.
* The input data needed for running this tool.
* An extended version of the evaluation results.

The DOI for this repository is DOI: XXX

## Overview: ##
The figure below shows the overall workflow of LibRARIAN. LibRARIAN identifies unknown third-party native libraries and their versions (Unknown Lib Versions) by:
(1) extracting features that distinguish major, minor, and patch versions of libraries that are stable across platforms regardless of underlying architecture or compilation environments 
(2) comparing those features against features from a ground-truth dataset (Known Lib Versions) using a novel similarity metric, bin2sim 
(3) matching against strings that identify version information of libraries extracted from the ground-truth dataset, which we refer to as Version Identification Strings

![Figure 1](/images/approach_cropped.png) 

### Feature Vector Extraction: ###
Our binary similarity detection is based on the extraction of features from binaries combining both metadata found in ELF files as well as identifying features in different binary sections of the library. All shared libraries included in Android apps are compiled into Executable and Linkable Format (ELF) binaries. Like other object files, ELF binaries contain a symbol table with externally visible identifiers such as function names, global symbols, local symbols, and imported symbols.
This symbol table is, on one hand, used during loading and linking and, on the other hand, used by binary analysis tools (e.g., *objdump*, *readelf*, *nm*, *pwntools*, or *angr*) to infer information about the binary.

### Similarity Computation: ###
bin2sim is used to determine the similarity between feature vectors. Given two binaries b_1 and b_2 with respective feature vectors FV_1 and FV_2, the bin2sim is the size of the intersection of FV_1 and FV_2 (i.e., the number of common features) over the size of the union of FV_1 and FV_2 (i.e., the number of unique features). The similarity score is a floating-point value between 0 and 1, with a score of 1 indicating identical features, and a score of 0 indicating no shared features between the two libraries.

## Librarian 101: ## 
Librarian's structure in a nutshell:
```
|-- sample_apps
|-- UnknownLibs_bins
|-- UnknownLibs_FVs
|-- knownLibs_FVs
|-- evaluation-results
|-- output_examples
|-- scripts
|   |-- cluster_libs.py
|   |-- Bin2Bin_Score_Calculator
|   |   |-- run_bin_sim.sh
|   |   |-- binsimScore.py
|   |   |-- extracted_bin_FVS.txt
|   |   `-- source_bin_FVS.txt
|   `-- Feature_Extractor
|       |-- run_extract_fv.sh
|       |-- extract_feature_vector.py
|       `-- extracted_bins.txt
```

* **sample_apps**: Our repository contains the top 200 apps collected from GooglePlay along with their previous releases, obtained from [AndroZoo](https://androzoo.uni.lu/). Due to the large size of this set (209 GB), we provide only 20 unique android packages, as a sample, with a total of 32 app versions. e.g. com.instagram.android has 7 different versions, where the version name is the sha256 of the app version. Naming app versions after their sha256 will enable us to 1) distinguish between different versions of the same app, 2) easily match every app version with [version details](https://androzoo.uni.lu/lists) found in AndroZoo such as: vercode, markets, apk_size etc. 
* **UnknownLibs_bins**: This folder contains binaries extracted from apps in `sample_apps` arranged into folders based on the binary's sha256. (Run: `python3 cluster_libs.py` to obtain them). For example, cluster/folder (ca8a18f07d0d16e3ce1f4cb35d6d326fd0bbb2a4e82488a937f6feffbfa44b3b) contains 5 identical binaries (i.e. they share the same sha256), which were extracted from 5 different apps or app versions. 
* **UnknownLibs_FVs**: Feature vectors extracted from `UnknownLibs_bins` and stored in JSON files.
* **KnownLibs_FVs**: Features vectors extracted from our groundTruth (KnownLibs) and stored in JSON files.
* **scripts**:
  * cluster_libs.py: Extracts biniares from the sample_apps folder and clusters them based on their sha256 (to remove duplicates and reduce run time).
  * Feature_Extractor: Scripts needed to extract feature vectors.
  * Bin2Bin_Score_Calculator: Scripts needed for computing the similarity score between `knownLibs_FVs` and `UnknownLibs_FVs`.  

## Evaluation Results: ##
`Librarian-ICSE2021-RQs.xlsx` under `evaluation-results`
 contains an extended version of the evaluation results presented in the paper (Section 3). Each table’s result is represented in a separate sheet:
* **inferred_libs**: Contains the results of using Librarian to infer the versions of 7251 binaries extracted from android apps. Each binary is represented in one row, with:
  * The name of the cluster/folder which the binary resides in (column A).
  * The name of the binary, represented as *binaryName_* then the *sha256 of the app* which the binary was extracted from (column B).
  * The number of other similar binaries (i.e. binaries that share the same sha256) that reside in the same cluster (column C).
  * The binary's architecture (column D and E).
  * The binary version inferred by Librarian (column F).
  * Whether a binary is vulnerable or not (column G).
* **vul_libs_only**: This table is similar to the previous sheet, but contains vulnerable binaries only 
* **vul_libs_till-now**: Contains the binaries that were vulnerable up until the submission of the paper. Each row contains a vulnerable binary version (column C), along with the name of the distinct app affected by the vulnerable binary (column A), the number of app versions containing a vulnerable binary (column B), and since when was the binary vulnerable (column D). The dates were obtained from [AndroZoo](https://androzoo.uni.lu/lists).
* The remaining sheets are an extended version of the results reported in the paper (table 4 - table 8). Please refer to the paper for more details. 
