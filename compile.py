#!/usr/bin/env python3
import py_compile
import os, fnmatch

def find(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

files = find("*.py", ".")
for file in files:
    if "/compile.py" not in file:
        print("Compiling: {}".format(file))
        py_compile.compile(file, doraise=False)
