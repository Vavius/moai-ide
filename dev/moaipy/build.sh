#!/bin/bash

# build python extension
rm -f moaipy.cpp

# export CFLAGS=-sysroot,/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk
# export LDFLAGS=-L/Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/MacOSX10.7.sdk/usr/lib
python setup.py build