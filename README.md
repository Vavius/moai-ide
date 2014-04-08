# MOAI Editor

This editor is a Python-Qt based host for MOAI SDK. 
The main idea behind all this is pretty easy: 
* I wanted to add editor features to MOAI SDK with live game preview - like most of 3d AAA engines have
* Editors tend to have pretty complicated GUI - coding all this in Lua with MOAI classes is a pain, also some performance issues could arise, so better to look at existing frameworks and run MOAI as GL View
* Qt is one of the most complete frameworks for crossplatform GUI applications
* GUI stuff is easier to code and tune with dynamic language such as Python (may consider QtScript as well)

### Features
* Host for latest MOAI SDK (currently 1.5)
* Lua code reload localy and remote (experimental)
* Ability to specify target resolution (set as MOAIEnvironment.screenWidth and MOAIEnvironment.screenHeight values)
* Color console output with timestamps
* Limited modules support - no sound, box2d, http-task. I'll be adding those soon


### Setup
Since all used technologies are cross platform in nature this thing should work on Windows, Linux, OS X without problems. 
However, I've only tested this on OS X 10.8 and 10.9. To build on other platforms you'll need to compile MOAI as python module, read [Technical details](#technical-details) for more info. 

### There are tons of dependencies: 
* Qt 4.8.5 and PySide 1.2.1: https://qt-project.org/wiki/PySide_Binaries_MacOSX (sometimes 1.2.1 does not work, then 1.1.1 can be used with Qt 4.8.5)
* hanappe/flower based lua framework from here: https://github.com/Vavius/moai-framework
* PyOpenGL-3.0.2 and Cython-0.19.2 - included in this repo as archives

### Installation
1. Install Qt, then PySide bindings
2. Unzip and install include/PyOpenGL-3.0.2.zip (python setup.py install)
3. Clone Lua framework https://github.com/Vavius/moai-framework, then link or copy src/ folder from it to editor/lua/moai-framework/src/

### Running
    cd editor
    python mainwindow.py

or double-click on run.command

Use file->open or cmd+O to open any moai main.lua file. 

### Live Reload
There is a watchdog module that looks for changed files in current directory (the one that contains opened main.lua). 
Probably you'll find 3 checkboxes in the host window: 
* Local - whether to auto-reload local host on file change 
* Device - whether to send changes to selected device (should be found and specified in drop-down menu) 
* Full reload - buggy one. When checked the whole MOAI context is created from scratch. Does not work for Device. Should be always checked for Local. 

### Device reload
WARNING: this feature was working in my tests some time ago, but currently I'm not using it in any of my projects, so it can be broken. Also, live-update (i.e. not full reload) needs a rethink. 

Device reload implemented by sending files with luasocket and saving them to DocumentDirectory under livereload/ path. Lua package.path is altered to look in documents/livereload first. Also, resource lookup paths are updated to handle images, fonts and other resources hot-swap. 

Devices can be found in local network. Device should run the app you currently developing. To enable remote reload add this to main.lua:

    if MOAIAppIOS or MOAIAppAndroid then
        LIVE_RELOAD_CLIENT = require "util.LiveReloadClient"

        -- table here specifies custom lua search paths, that was added by your app to package.path
        -- in order to properly add directory overrides
        LIVE_RELOAD_CLIENT:init({'src/?.lua', 'src/framework/?.lua'})
    end

Only live-update aka "not full reload" is working for device. It relauches current ingame scene when something is reloaded. 

### Technical details
MOAI is compiled as python module with Cython. Lua communication implemented with Lupa. There are some modifications to Lupa in order to make it use existing lua_State from MOAI. 
Python module sources located in dev/moaipy:
* static moai libs - I suppose they need to be recompiled for your current platform
* cmoai.pxd - cython header file for AKU calls
* moaipy.pyx - here we wrap AKU functions to be called from python
* _lupa.pyx - modified lupa
* setup.py - distutils script
* build.sh - run it to build extension


