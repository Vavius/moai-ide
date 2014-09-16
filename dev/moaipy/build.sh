#!/bin/bash

# build python extension
rm -f moaipy.cpp

PYTHON_PATH="/usr/local/Cellar/python/2.7.3/bin/python"
export MACOSX_DEPLOYMENT_TARGET=10.8
$PYTHON_PATH setup.py build