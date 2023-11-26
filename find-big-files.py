#! python3
# -*- coding: utf-8 -*-

"""
Usage:  python big-files.py [options] directory

find-big-files.py - Looks for big files (default bigger than 1GB) in given directory and prints their path

Options:
    -s - file size
    -h - help
"""


import os
import sys
from pathlib import Path


def printhelp():
    print(
        """Usage:  python big-files.py [options] directory

find-big-files.py - Looks for big files (default bigger than 1GB) in given directory and prints their path

Options:
    -s - file size
    -h - help
          """
    )


def unit_convertor(num, unit_in, unit_out):
    """Unit convertor"""
    units = {
        "B": 1,
        "KB": 1000,  # B
        "MB": 1000000,
        "GB": 1000000000,
        "TB": 1000000000000,
    }

    if unit_in not in units:
        print(f"Can't convert {num}{unit_in} to {unit_out}")
        sys.exit(1)

    return num * units[unit_in] / units[unit_out]


def check_if_big(file_size, path, min_size, file_type="File: "):
    if file_size >= min_size:  # 1GB
        print(
            file_type
            + os.path.abspath(path)
            + "\n"
            + str(round(file_size / 1000000000, 2))
            + " GB"
        )


def search_for_files(path):
    if path.exists():
        for folder_name, subfolders, filenames in os.walk(path):
            folder_size = 0
            for filename in filenames:
                try:
                    filename_path = str(Path(folder_name, filename))
                    filename_size = os.path.getsize(filename_path)
                except FileNotFoundError:
                    #  Doesn't work only on some system files
                    print(f"Couldn't get size of {filename_path}")
                    continue
                else:
                    folder_size += filename_size
                check_if_big(filename_size, filename_path, min_size)
            check_if_big(folder_size, folder_name, min_size, file_type="Directory: ")
    else:
        print("Path " + str(os.path.abspath(path)) + " doesn't exist")


if sys.argv[1] == "-h":
    printhelp()
    sys.exit(1)
else:
    min_size = 1000000000  # 1GB
    path = Path.cwd()
    i = 1
    while i < len(sys.argv):
        if sys.argv[i] == "-s":
            try:
                min_size_val = int(sys.argv[i + 1][:-2])  # Zrobić konwersję
                min_size_unit = sys.argv[i + 1][-2:].upper()
                min_size = unit_convertor(min_size_val, min_size_unit, "B")
            except IndexError:
                print("No file size specified")
                sys.exit(1)
            except ValueError:
                print(f"{sys.argv[i + 1]} isn't valid size")
                sys.exit(1)
            i += 2
        else:
            path = Path(sys.argv[i])
            search_for_files(path)
            i += 1
    if path == Path.cwd():
        search_for_files(path)
