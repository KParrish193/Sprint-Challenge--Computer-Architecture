#!/usr/bin/env python3

"""Main."""

import sys
from os import listdir
from cpu import *


# grab filename from command line and pass to load as parameter
# check if filename is in list of allowed filename in examples folder
# 1. create a dictionary of allowed filenames
# 2. check if provided filename is in dictionary
# check if a file is provided in commandline
cpu = CPU()

files = {file: None for file in listdir("examples")}

if len(sys.argv) > 1:
    filename = sys.argv[1]

    if filename in files:
        cpu.load(filename)

    else:
        print(f"Invalid Filename")

else:
    cpu.load("print8.ls8")

cpu.run()