#!/bin/bash
pushd tests
export PYTHONPATH=..
python3 test-config.py
python3 test-ftpfile.py
popd

