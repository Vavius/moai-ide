# MOAI Editor

### Features
* Host for latest MOAI SDK (currently 1.6)
* Particle editor for MOAI script-based particle system
* Lua code reload localy and remote (experimental)
* Ability to specify target resolution (set as MOAIEnvironment.screenWidth and MOAIEnvironment.screenHeight values)
* Colored console output with timestamps

### Roadmap
What is missing:
* Hmm, the Editor itself is pretty missing. Currently, this is just a Python-Qt MOAI Host

### Setup
Since all used technologies are cross platform in nature this thing should work on Windows, Linux, OS X without problems. 
However, I've only tested this on OS X 10.8-10.10. To build on other platforms you'll need to compile MOAI as python module, read [Technical details](#technical-details) for more info. 

### Dependencies: 
* Qt 4.8.5 and PySide 1.2.1: https://qt-project.org/wiki/PySide_Binaries_MacOSX (sometimes 1.2.1 does not work, then 1.1.1 can be used with Qt 4.8.5)
* PyOpenGL-3.0.2 - included in this repo as archives

### Installation
1. Install Qt, then PySide bindings
2. Unzip and install include/PyOpenGL-3.0.2.zip (python setup.py install)

### Running
    cd editor
    python mainwindow.py

or double-click on run.command

Use file->open or cmd+O to open any moai main.lua file. 

### Particle Editor
Based on MOAI particle system, that is much more flexible than PEX. 

1. In the menu bar select `Particle Editor` -> `New Project`
2. Ensure that particle docks are visible. In the `Window` menu: `Particle Editor` and `Particle Params` should be checked. 
3. Load an image for particles. There is also an option to load TexturePacker exported atlases in MOAI (.lua) format.
4. Add first emitter and state. Click on Emitter1, you'll see it's properties in Particle params dock. Select your State1 as initial state for the emitter.
5. Some particles should appear on the screen now. 

### Technical details
MOAI is compiled as python module with Cython. Lua communication implemented with Lupa. There are some modifications to Lupa in order to make it use existing lua_State from MOAI. 
Python module sources located in dev/moaipy:
* static moai libs - I suppose they need to be recompiled for your current platform
* cmoai.pxd - cython header file for AKU calls
* moaipy.pyx - here we wrap AKU functions to be called from python
* _lupa.pyx - modified lupa
* setup.py - distutils script
* build.sh - run it to build extension


