"""
Copy input files of the same name but with different subdirectories
into temporary directory - with names based on these input subdirectories.

This is done to avoid standard WDL behavior of giving array of files with same name -
some totally made up subdirectories to avoid a name conflict and as such - to
lose original naming information
"""
#!/usr/bin/env python3

import os
from os.path import isdir, basename, dirname, splitext
import shutil
import argparse
from typing import Dict, List

Files = List[str]
FilesMap = Dict[str, str]


def get_mapping(f: Files, targetdir: str) -> FilesMap:
    """
    Get old-names to new-names mapping, tries to detect uniqueness of IDs at some level of directories.
    Assumes that paths to input files have same depths
    """
    N: int = len(f)

    FileMap: FilesMap = {}
    DirMap: FilesMap = {}
    for x in f:
        val = splitext(x)
        if val[1] != ".h5":
            raise ValueError(f"Input file has wrong extension: {x}")
        FileMap[x] = os.path.join(targetdir, basename(x))
        DirMap[x] = os.path.join(targetdir, basename(dirname(x)) + ".h5")

    num_diff_files = len(set(FileMap.values()))
    if num_diff_files == N:
        # All files are unique. WDL will not localize them in made-up subdirectories
        return FileMap
    else:
        num_diff_dirs = len(set(DirMap.values()))
        if num_diff_dirs == N:
            # All first-level dirs are unique.
            return DirMap
    raise ValueError("Both files and first-level directories are not unique, implement deeper recursion")

def copy_files(fm: FilesMap):
    """ Copy (potentially renamed) files into temporary location"""
    for key, value in fm.items():
        shutil.copy(key, value)


def main():
    """ Parse parameters and run renaming code """
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", required=True, help="input location of hd5 files")
    parser.add_argument("-o", "--output", required=True, help="output location of renamed hd5 files")
    args = parser.parse_args()
    for x in [args.input, args.output]:
        if not isdir(x):
            raise ValueError(f"Required directory doesn't exist: {x}")

    input_files : Files = []
    for root, dirs, files in os.walk(args.input):
        for filename in files:
            input_files.append(os.path.join(root, filename))

    map_: FilesMap = get_mapping(input_files, args.output)
    copy_files(map_)
    print("Done!")

if __name__ == "__main__":
    main()
