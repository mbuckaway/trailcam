#!/bin/bash
pushd tests
export MICROPYPATH="~/.micropython/lib:.."
micropython test-config.py
popd

