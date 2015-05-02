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


def AKUAppInitialize():
    cmoai.AKUAppInitialize()

def AKUCreateContext():
    return cmoai.AKUCreateContext()

def AKUCheckContext(context):
    return cmoai.AKUCheckContext(context)

def AKUCountContexts():
    return cmoai.AKUCountContexts()


def AKUDeleteContext(context):
    cmoai.AKUDeleteContext(context)

def AKUGetContext():
    return cmoai.AKUGetContext()

def AKUAppFinalize():
    cmoai.AKUAppFinalize()

def AKUSetContext(context):
    cmoai.AKUSetContext(context)

# def AKUGetLuaState():
#     cdef long pointer = <long> cmoai.AKUGetLuaState()
#     return pointer

# char*           AKUGetMoaiVersion               ( char* buffer, size_t length )
# char*           AKUGetWorkingDirectory          ( char* buffer, size_t length )
# int             AKUMountVirtualDirectory        ( char* virtualPath, char* archive )

def AKURunScript(filename):
    cmoai.AKULoadFuncFromFile(filename)
    cmoai.AKUCallFunc()

def AKURunString(script):
    cmoai.AKULoadFuncFromString(script)
    cmoai.AKUCallFunc()

def AKUSetWorkingDirectory(path):
    cmoai.AKUSetWorkingDirectory(path)

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

def AKUInitMemPool(sizeInBytes):
    cmoai.AKUInitMemPool(sizeInBytes)

def AKUClearMemPool():
    cmoai.AKUClearMemPool()


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

def AKUEnqueueKeyboardCharEvent(deviceID, sensorID, unicodeChar):
    cmoai.AKUEnqueueKeyboardCharEvent(deviceID, sensorID, unicodeChar)

def AKUEnqueueKeyboardEditEvent(deviceID, sensorID, text, start, editLength, maxLength):
    cmoai.AKUEnqueueKeyboardEditEvent(deviceID, sensorID, text, start, editLength, maxLength)

def AKUEnqueueKeyboardKeyEvent(deviceID, sensorID, keyID, down):
    cmoai.AKUEnqueueKeyboardKeyEvent(deviceID, sensorID, keyID, down)

def AKUEnqueueKeyboardTextEvent(deviceID, sensorID, text):
    cmoai.AKUEnqueueKeyboardTextEvent(deviceID, sensorID, text)

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


# Modules

def AKUModulesAppInitialize():
    cmoai.AKUUtilAppInitialize()
    cmoai.AKUSimAppInitialize()
    cmoai.AKULuaExtAppInitialize()
    cmoai.AKUFmodStudioAppInitialize()
    cmoai.AKUUntzAppInitialize()
    cmoai.AKUHttpClientAppInitialize()
    cmoai.AKUCryptoAppInitialize()
    cmoai.AKUSpineAppInitialize()
    cmoai.AKUBox2DAppInitialize()
    # cmoai.AKUPluginsAppInitialize()

def AKUModulesAppFinalize():
    cmoai.AKUUtilAppFinalize()
    cmoai.AKUSimAppFinalize()
    cmoai.AKULuaExtAppFinalize()
    cmoai.AKUFmodStudioAppFinalize()
    cmoai.AKUUntzAppFinalize()
    cmoai.AKUHttpClientAppFinalize()
    cmoai.AKUCryptoAppFinalize()
    cmoai.AKUSpineAppFinalize()
    cmoai.AKUBox2DAppFinalize()
    # cmoai.AKUPluginsAppFinalize()

def AKUModulesContextInitialize():
    cmoai.AKUUtilContextInitialize()
    cmoai.AKUSimContextInitialize()
    cmoai.AKULuaExtContextInitialize()
    cmoai.AKUFmodStudioContextInitialize()
    cmoai.AKUUntzContextInitialize()
    cmoai.AKUHttpClientContextInitialize()
    cmoai.AKUCryptoContextInitialize()
    cmoai.AKUSpineContextInitialize()
    cmoai.AKUBox2DContextInitialize()
    # cmoai.AKUPluginsContextInitialize()

def AKUModulesUpdate():
    cmoai.AKUFmodStudioUpdate()
    cmoai.AKUHttpClientUpdate()
    # cmoai.AKUPluginsUpdate()
    cmoai.AKUUpdate()

def AKUModulesRunLuaAPIWrapper():
    cmoai.AKULoadFuncFromBuffer ( cmoai.moai_lua, cmoai.moai_lua_SIZE, cmoai.AKU_DATA_STRING, cmoai.AKU_DATA_ZIPPED )
    cmoai.AKUCallFunc()

def AKUInitParticlePresets():
    cmoai.ParticlePresets()


# Expose Key codes enum values
MOAI_KEY_BACKSPACE      = cmoai.MOAI_KEY_BACKSPACE
MOAI_KEY_TAB            = cmoai.MOAI_KEY_TAB
MOAI_KEY_RETURN         = cmoai.MOAI_KEY_RETURN
MOAI_KEY_SHIFT          = cmoai.MOAI_KEY_SHIFT
MOAI_KEY_CONTROL        = cmoai.MOAI_KEY_CONTROL
MOAI_KEY_ALT            = cmoai.MOAI_KEY_ALT
MOAI_KEY_PAUSE          = cmoai.MOAI_KEY_PAUSE
MOAI_KEY_CAPS_LOCK      = cmoai.MOAI_KEY_CAPS_LOCK
MOAI_KEY_ESCAPE         = cmoai.MOAI_KEY_ESCAPE
MOAI_KEY_SPACE          = cmoai.MOAI_KEY_SPACE
MOAI_KEY_PAGE_UP        = cmoai.MOAI_KEY_PAGE_UP
MOAI_KEY_PAGE_DOWN      = cmoai.MOAI_KEY_PAGE_DOWN
MOAI_KEY_END            = cmoai.MOAI_KEY_END
MOAI_KEY_HOME           = cmoai.MOAI_KEY_HOME
MOAI_KEY_LEFT           = cmoai.MOAI_KEY_LEFT
MOAI_KEY_UP             = cmoai.MOAI_KEY_UP
MOAI_KEY_RIGHT          = cmoai.MOAI_KEY_RIGHT
MOAI_KEY_DOWN           = cmoai.MOAI_KEY_DOWN
MOAI_KEY_PRINT_SCREEN   = cmoai.MOAI_KEY_PRINT_SCREEN
MOAI_KEY_INSERT         = cmoai.MOAI_KEY_INSERT
MOAI_KEY_DELETE         = cmoai.MOAI_KEY_DELETE
MOAI_KEY_DIGIT_0        = cmoai.MOAI_KEY_DIGIT_0
MOAI_KEY_DIGIT_1        = cmoai.MOAI_KEY_DIGIT_1
MOAI_KEY_DIGIT_2        = cmoai.MOAI_KEY_DIGIT_2
MOAI_KEY_DIGIT_3        = cmoai.MOAI_KEY_DIGIT_3
MOAI_KEY_DIGIT_4        = cmoai.MOAI_KEY_DIGIT_4
MOAI_KEY_DIGIT_5        = cmoai.MOAI_KEY_DIGIT_5
MOAI_KEY_DIGIT_6        = cmoai.MOAI_KEY_DIGIT_6
MOAI_KEY_DIGIT_7        = cmoai.MOAI_KEY_DIGIT_7
MOAI_KEY_DIGIT_8        = cmoai.MOAI_KEY_DIGIT_8
MOAI_KEY_DIGIT_9        = cmoai.MOAI_KEY_DIGIT_9
MOAI_KEY_A              = cmoai.MOAI_KEY_A
MOAI_KEY_B              = cmoai.MOAI_KEY_B
MOAI_KEY_C              = cmoai.MOAI_KEY_C
MOAI_KEY_D              = cmoai.MOAI_KEY_D
MOAI_KEY_E              = cmoai.MOAI_KEY_E
MOAI_KEY_F              = cmoai.MOAI_KEY_F
MOAI_KEY_G              = cmoai.MOAI_KEY_G
MOAI_KEY_H              = cmoai.MOAI_KEY_H
MOAI_KEY_I              = cmoai.MOAI_KEY_I
MOAI_KEY_J              = cmoai.MOAI_KEY_J
MOAI_KEY_K              = cmoai.MOAI_KEY_K
MOAI_KEY_L              = cmoai.MOAI_KEY_L
MOAI_KEY_M              = cmoai.MOAI_KEY_M
MOAI_KEY_N              = cmoai.MOAI_KEY_N
MOAI_KEY_O              = cmoai.MOAI_KEY_O
MOAI_KEY_P              = cmoai.MOAI_KEY_P
MOAI_KEY_Q              = cmoai.MOAI_KEY_Q
MOAI_KEY_R              = cmoai.MOAI_KEY_R
MOAI_KEY_S              = cmoai.MOAI_KEY_S
MOAI_KEY_T              = cmoai.MOAI_KEY_T
MOAI_KEY_U              = cmoai.MOAI_KEY_U
MOAI_KEY_V              = cmoai.MOAI_KEY_V
MOAI_KEY_W              = cmoai.MOAI_KEY_W
MOAI_KEY_X              = cmoai.MOAI_KEY_X
MOAI_KEY_Y              = cmoai.MOAI_KEY_Y
MOAI_KEY_Z              = cmoai.MOAI_KEY_Z
MOAI_KEY_GUI            = cmoai.MOAI_KEY_GUI
MOAI_KEY_APPLICATION    = cmoai.MOAI_KEY_APPLICATION
MOAI_KEY_NUM_0          = cmoai.MOAI_KEY_NUM_0
MOAI_KEY_NUM_1          = cmoai.MOAI_KEY_NUM_1
MOAI_KEY_NUM_2          = cmoai.MOAI_KEY_NUM_2
MOAI_KEY_NUM_3          = cmoai.MOAI_KEY_NUM_3
MOAI_KEY_NUM_4          = cmoai.MOAI_KEY_NUM_4
MOAI_KEY_NUM_5          = cmoai.MOAI_KEY_NUM_5
MOAI_KEY_NUM_6          = cmoai.MOAI_KEY_NUM_6
MOAI_KEY_NUM_7          = cmoai.MOAI_KEY_NUM_7
MOAI_KEY_NUM_8          = cmoai.MOAI_KEY_NUM_8
MOAI_KEY_NUM_9          = cmoai.MOAI_KEY_NUM_9
MOAI_KEY_NUM_MULTIPLY   = cmoai.MOAI_KEY_NUM_MULTIPLY
MOAI_KEY_NUM_PLUS       = cmoai.MOAI_KEY_NUM_PLUS
MOAI_KEY_NUM_MINUS      = cmoai.MOAI_KEY_NUM_MINUS
MOAI_KEY_NUM_DECIMAL    = cmoai.MOAI_KEY_NUM_DECIMAL
MOAI_KEY_NUM_DIVIDE     = cmoai.MOAI_KEY_NUM_DIVIDE
MOAI_KEY_F1             = cmoai.MOAI_KEY_F1
MOAI_KEY_F2             = cmoai.MOAI_KEY_F2
MOAI_KEY_F3             = cmoai.MOAI_KEY_F3
MOAI_KEY_F4             = cmoai.MOAI_KEY_F4
MOAI_KEY_F5             = cmoai.MOAI_KEY_F5
MOAI_KEY_F6             = cmoai.MOAI_KEY_F6
MOAI_KEY_F7             = cmoai.MOAI_KEY_F7
MOAI_KEY_F8             = cmoai.MOAI_KEY_F8
MOAI_KEY_F9             = cmoai.MOAI_KEY_F9
MOAI_KEY_F10            = cmoai.MOAI_KEY_F10
MOAI_KEY_F11            = cmoai.MOAI_KEY_F11
MOAI_KEY_F12            = cmoai.MOAI_KEY_F12
MOAI_KEY_NUM_LOCK       = cmoai.MOAI_KEY_NUM_LOCK
MOAI_KEY_SCROLL_LOCK    = cmoai.MOAI_KEY_SCROLL_LOCK
MOAI_KEY_OEM_1          = cmoai.MOAI_KEY_OEM_1
MOAI_KEY_OEM_PLUS       = cmoai.MOAI_KEY_OEM_PLUS
MOAI_KEY_OEM_COMMA      = cmoai.MOAI_KEY_OEM_COMMA
MOAI_KEY_OEM_MINUS      = cmoai.MOAI_KEY_OEM_MINUS
MOAI_KEY_OEM_PERIOD     = cmoai.MOAI_KEY_OEM_PERIOD
MOAI_KEY_OEM_2          = cmoai.MOAI_KEY_OEM_2
MOAI_KEY_OEM_3          = cmoai.MOAI_KEY_OEM_3
MOAI_KEY_OEM_4          = cmoai.MOAI_KEY_OEM_4
MOAI_KEY_OEM_5          = cmoai.MOAI_KEY_OEM_5
MOAI_KEY_OEM_6          = cmoai.MOAI_KEY_OEM_6
MOAI_KEY_OEM_7          = cmoai.MOAI_KEY_OEM_7
MOAI_KEY_OEM_8          = cmoai.MOAI_KEY_OEM_8
MOAI_KEY_OEM_102        = cmoai.MOAI_KEY_OEM_102
MOAI_KEY_TOTAL          = cmoai.MOAI_KEY_TOTAL
MOAI_KEY_INVALID        = cmoai.MOAI_KEY_INVALID

