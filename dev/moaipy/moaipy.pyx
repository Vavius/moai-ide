# cython: embedsignature=True

################################################
##                                            ##
##                                            ##
##    8888ba.88ba   .88888.   .d888888  dP    ##
##    88  `8b  `8b d8'   `8b d8'    88  88    ##
##    88   88   88 88     88 88aaaaa88a 88    ##
##    88   88   88 88     88 88     88  88    ##
##    88   88   88 Y8.   .8P 88     88  88    ##
##    dP   dP   dP  `8888P'  88     88  dP    ##
##                                            ##
##                                            ##
################################################

include '_lupa.pyx'

cimport cmoai

# callback management
# here we use global python functions as callbacks

# ctypedef void ( *AKUEnterFullscreenModeFunc )    ()
# ctypedef void ( *AKUExitFullscreenModeFunc )     ()
# ctypedef void ( *AKUOpenWindowFunc )             ( char* title, int width, int height )
# ctypedef void ( *AKUSetSimStepFunc )             ( double step )

cdef void cAKUSetFunc_OpenWindow ( cmoai.AKUOpenWindowFunc func ):
    cmoai.AKUSetFunc_OpenWindow (func)

cdef void cAKUSetFunc_SetSimStep ( cmoai.AKUSetSimStepFunc func ):
    cmoai.AKUSetFunc_SetSimStep (func)

cdef void cAKUSetFunc_EnterFullscreenMode ( cmoai.AKUEnterFullscreenModeFunc func ):
    cmoai.AKUSetFunc_EnterFullscreenMode (func)

cdef void cAKUSetFunc_ExitFullscreenMode ( cmoai.AKUExitFullscreenModeFunc func ):
    cmoai.AKUSetFunc_ExitFullscreenMode (func)


cdef void callAKUSetFunc_OpenWindow ( const char* title, int width, int height ):
    global callback_OpenWindow
    if callback_OpenWindow:
        callback_OpenWindow(title, width, height)

cdef void callAKUSetFunc_SetSimStep ( double step ):
    global callback_SetSimStep
    if callback_SetSimStep:
        callback_SetSimStep(step)

cdef void callAKUSetFunc_EnterFullscreenMode ():
    global callback_EnterFullscreenMode
    if callback_EnterFullscreenMode:
        callback_EnterFullscreenMode()

cdef void callAKUSetFunc_ExitFullscreenMode ():
    global callback_ExitFullscreenMode
    if callback_ExitFullscreenMode:
        callback_ExitFullscreenMode()

def AKULoadLuaHeaders():
    cmoai.AKURunData ( cmoai.moai_lua, cmoai.moai_lua_SIZE, cmoai.AKU_DATA_STRING, cmoai.AKU_DATA_ZIPPED )

def AKUInitializeCallbacks():
    cAKUSetFunc_OpenWindow ( callAKUSetFunc_OpenWindow )
    cAKUSetFunc_SetSimStep ( callAKUSetFunc_SetSimStep )
    cAKUSetFunc_EnterFullscreenMode ( callAKUSetFunc_EnterFullscreenMode )
    cAKUSetFunc_ExitFullscreenMode ( callAKUSetFunc_ExitFullscreenMode )

def AKUSetFunc_OpenWindow(callbackFunc):
    global callback_OpenWindow
    callback_OpenWindow = callbackFunc

def AKUSetFunc_SetSimStep(callbackFunc):
    global callback_SetSimStep
    callback_SetSimStep = callbackFunc

def AKUSetFunc_EnterFullscreenMode(callbackFunc):
    global callback_EnterFullscreenMode
    callback_EnterFullscreenMode = callbackFunc

def AKUSetFunc_ExitFullscreenMode(callbackFunc):
    global callback_ExitFullscreenMode
    callback_ExitFullscreenMode = callbackFunc


def AKUCreateContext():
    return cmoai.AKUCreateContext()

def AKUDeleteContext(context):
    cmoai.AKUDeleteContext(context)

def AKUGetContext():
    return cmoai.AKUGetContext()

def AKUCreateContext():
    cmoai.AKUCreateContext()

def AKUFinalize():
    cmoai.AKUFinalize()

def AKUSetContext(context):
    cmoai.AKUSetContext(context)

# def AKUGetLuaState():
#     cdef long pointer = <long> cmoai.AKUGetLuaState()
#     return pointer

# char*           AKUGetMoaiVersion               ( char* buffer, size_t length )
# char*           AKUGetWorkingDirectory          ( char* buffer, size_t length )
# int             AKUMountVirtualDirectory        ( char* virtualPath, char* archive )

def AKURunScript(filename):
    cmoai.AKURunScript(filename)

def AKURunString(script):
    cmoai.AKURunString(script)

# def AKUSetArgv(argv):
    # cmoai.AKUSetArgv(argv)

# void            AKURunData                      ( void* data, size_t size, int dataType, int compressed )
def AKUSetWorkingDirectory(path):
    cmoai.AKUSetWorkingDirectory(path)

# void            AKUSetArgv                      ( char **argv )



# setup
def AKUFinalizeSim():
    cmoai.AKUFinalizeSim()

def AKUInitializeSim():
    cmoai.AKUInitializeSim()

# management api
def AKUDetectGfxContext():
    cmoai.AKUDetectGfxContext()

def AKUGetSimStep():
    return cmoai.AKUGetSimStep()

def AKUPause(pause):
    cmoai.AKUPause(pause)
    
def AKUReleaseGfxContext():
    cmoai.AKUReleaseGfxContext()

def AKURender():
    cmoai.AKURender()

def AKUSetOrientation(orientation):
    cmoai.AKUSetOrientation(orientation)

def AKUSetScreenDpi(dpi):
    cmoai.AKUSetScreenDpi(dpi)

def AKUSetScreenSize(width, height):
    cmoai.AKUSetScreenSize(width, height)

def AKUSetViewSize(width, height):
    cmoai.AKUSetViewSize(width, height)

def AKUSoftReleaseGfxResources(age):
    cmoai.AKUSoftReleaseGfxResources(age)

def AKUUpdate():
    cmoai.AKUUpdate()

# callback management
#void            AKUSetFunc_EnterFullscreenMode  ( AKUEnterFullscreenModeFunc func );
#void            AKUSetFunc_ExitFullscreenMode   ( AKUExitFullscreenModeFunc func );
#void            AKUSetFunc_OpenWindow           ( AKUOpenWindowFunc func );
#void            AKUSetFunc_SetSimStep           ( AKUSetSimStepFunc func );

# # input device api
def AKUReserveInputDevices(total):
    cmoai.AKUReserveInputDevices(total)

def AKUReserveInputDeviceSensors(deviceID, total):
    cmoai.AKUReserveInputDeviceSensors(deviceID, total)

def AKUSetInputConfigurationName(name):
    cmoai.AKUSetInputConfigurationName(name)

def AKUSetInputDevice(deviceID, name):
    cmoai.AKUSetInputDevice(deviceID, name)

def AKUSetInputDeviceActive(deviceID, active):
    cmoai.AKUSetInputDeviceActive(deviceID, active)

def AKUSetInputDeviceButton(deviceID, sensorID, name):
    cmoai.AKUSetInputDeviceButton(deviceID, sensorID, name)

def AKUSetInputDeviceCompass(deviceID, sensorID, name):
    cmoai.AKUSetInputDeviceCompass(deviceID, sensorID, name)

def AKUSetInputDeviceKeyboard(deviceID, sensorID, name):
    cmoai.AKUSetInputDeviceKeyboard(deviceID, sensorID, name)

def AKUSetInputDeviceLevel(deviceID, sensorID, name):
    cmoai.AKUSetInputDeviceLevel(deviceID, sensorID, name)

def AKUSetInputDeviceLocation(deviceID, sensorID, name):
    cmoai.AKUSetInputDeviceLocation(deviceID, sensorID, name)

def AKUSetInputDevicePointer(deviceID, sensorID, name):
    cmoai.AKUSetInputDevicePointer(deviceID, sensorID, name)

def AKUSetInputDeviceTouch(deviceID, sensorID, name):
    cmoai.AKUSetInputDeviceTouch(deviceID, sensorID, name)

def AKUSetInputDeviceWheel(deviceID, sensorID, name):
    cmoai.AKUSetInputDeviceWheel(deviceID, sensorID, name)


# # input events api
def AKUEnqueueButtonEvent(deviceID, sensorID, down):
    cmoai.AKUEnqueueButtonEvent(deviceID, sensorID, down)

def AKUEnqueueCompassEvent(deviceID, sensorID, heading):
    cmoai.AKUEnqueueCompassEvent(deviceID, sensorID, heading)

def AKUEnqueueKeyboardAltEvent(deviceID, sensorID, down):
    cmoai.AKUEnqueueKeyboardAltEvent(deviceID, sensorID, down)

def AKUEnqueueKeyboardControlEvent(deviceID, sensorID, down):
    cmoai.AKUEnqueueKeyboardControlEvent(deviceID, sensorID, down)

def AKUEnqueueKeyboardEvent(deviceID, sensorID, keyID, down):
    cmoai.AKUEnqueueKeyboardEvent(deviceID, sensorID, keyID, down)

def AKUEnqueueKeyboardShiftEvent(deviceID, sensorID, down):
    cmoai.AKUEnqueueKeyboardShiftEvent(deviceID, sensorID, down)

def AKUEnqueueLevelEvent(deviceID, sensorID, x, y, z):
    cmoai.AKUEnqueueLevelEvent(deviceID, sensorID, x, y, z)

def AKUEnqueueLocationEvent(deviceID, sensorID, longitude, latitude, altitude, hAccuracy, vAccuracy, speed):
    cmoai.AKUEnqueueLocationEvent(deviceID, sensorID, longitude, latitude, altitude, hAccuracy, vAccuracy, speed)

def AKUEnqueuePointerEvent(deviceID, sensorID, x, y):
    cmoai.AKUEnqueuePointerEvent(deviceID, sensorID, x, y)

def AKUEnqueueTouchEvent(deviceID, sensorID, touchID, down, x, y):
    cmoai.AKUEnqueueTouchEvent(deviceID, sensorID, touchID, down, x, y)

def AKUEnqueueTouchEventCancel(deviceID, sensorID):
    cmoai.AKUEnqueueTouchEventCancel(deviceID, sensorID)

def AKUEnqueueWheelEvent(deviceID, sensorID, value):
    cmoai.AKUEnqueueWheelEvent(deviceID, sensorID, value)


# util host.h

def AKUInitializeUtil():
    cmoai.AKUInitializeUtil()

def AKUFinalizeUtil():
    cmoai.AKUFinalizeUtil()

# Lua extensions host.h    
def AKUExtLoadLuafilesystem ():
    cmoai.AKUExtLoadLuafilesystem()
    
def AKUExtLoadLuasocket ():
    cmoai.AKUExtLoadLuasocket()
    
def AKUExtLoadLuasql ():
    cmoai.AKUExtLoadLuasql()
    


__all_moai__ = [
"AKULoadLuaHeaders",
"AKUInitializeCallbacks",
"AKUSetFunc_OpenWindow",
"AKUSetFunc_SetSimStep",
"AKUSetFunc_EnterFullscreenMode",
"AKUSetFunc_ExitFullscreenMode",
"AKUCreateContext",
"AKUDeleteContext",
"AKUGetContext",
"AKUCreateContext",
"AKUFinalize",
"AKUSetContext",
"AKURunScript",
"AKURunString",
"AKUSetWorkingDirectory",
"AKUFinalizeSim",
"AKUInitializeSim",
"AKUDetectGfxContext",
"AKUGetSimStep",
"AKUPause",
"AKUReleaseGfxContext",
"AKURender",
"AKUSetOrientation",
"AKUSetScreenDpi",
"AKUSetScreenSize",
"AKUSetViewSize",
"AKUSoftReleaseGfxResources",
"AKUUpdate",
"AKUReserveInputDevices",
"AKUReserveInputDeviceSensors",
"AKUSetInputConfigurationName",
"AKUSetInputDevice",
"AKUSetInputDeviceActive",
"AKUSetInputDeviceButton",
"AKUSetInputDeviceCompass",
"AKUSetInputDeviceKeyboard",
"AKUSetInputDeviceLevel",
"AKUSetInputDeviceLocation",
"AKUSetInputDevicePointer",
"AKUSetInputDeviceTouch",
"AKUSetInputDeviceWheel",
"AKUEnqueueButtonEvent",
"AKUEnqueueCompassEvent",
"AKUEnqueueKeyboardAltEvent",
"AKUEnqueueKeyboardControlEvent",
"AKUEnqueueKeyboardEvent",
"AKUEnqueueKeyboardShiftEvent",
"AKUEnqueueLevelEvent",
"AKUEnqueueLocationEvent",
"AKUEnqueuePointerEvent",
"AKUEnqueueTouchEvent",
"AKUEnqueueTouchEventCancel",
"AKUEnqueueWheelEvent",
"AKUInitializeUtil",
"AKUFinalizeUtil",
"AKUExtLoadLuafilesystem",
"AKUExtLoadLuasocket",
"AKUExtLoadLuasql",
'LuaRuntime', 
'LuaError', 
'as_itemgetter', 
'as_attrgetter',
]

