#!/bin/bash

# build python extension
rm -f moaipy.cpp

PYTHON_PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin/python"
export MACOSX_DEPLOYMENT_TARGET=10.8
$PYTHON_PATH setup.py build