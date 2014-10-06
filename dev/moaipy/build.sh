#!/bin/bash

# build python extension
rm -f moaipy.cpp

PYTHON_PATH="/Library/Frameworks/Python.framework/Versions/2.7/bin/python"
export MACOSX_DEPLOYMENT_TARGET=10.8
$PYTHON_PATH setup.py build

echo "=== LIBRARY BUILT ==="

cd 'build/lib.macosx-10.6-intel-2.7/'
echo "overriding loader path for libfmod.dylib ..."
install_name_tool -change "@rpath/libfmod.dylib" "@loader_path/libfmod.dylib" moaipy.so
echo "moving moaipy.so to edtior/moaipy/moaipy.so ..."
cp moaipy.so '../../../../editor/moaipy/moaipy.so'
echo "=== COMPLETE ==="