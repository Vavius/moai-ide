cimport cmoai

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

def AKUGetLuaState():
    cdef long pointer = <long> cmoai.AKUGetLuaState()
    return pointer

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
# int             AKUSetWorkingDirectory          ( char* path )
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
