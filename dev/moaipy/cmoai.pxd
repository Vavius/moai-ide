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


cdef extern from "moai-core/host.h":
    ctypedef struct lua_State:
        pass
    ctypedef int AKUContextID

    void            AKUAppFinalize                  ()
    void            AKUAppInitialize                ()
    void            AKUClearMemPool                 ()
    int             AKUCheckContext                 ( AKUContextID context )
    int             AKUCountContexts                ()
    AKUContextID    AKUCreateContext                ()
    void            AKUDeleteContext                ( AKUContextID context )
    AKUContextID    AKUGetContext                   ()
    void*           AKUGetUserdata                  ()

    void            AKUInitMemPool                  ( size_t sizeInBytes )
    void            AKUSetContext                   ( AKUContextID context )
    void            AKUSetUserdata                  ( void* user )

    # management api
    lua_State*      AKUGetLuaState                  ()
    char*           AKUGetMoaiVersion               ( char* buffer, size_t length )
    char*           AKUGetWorkingDirectory          ( char* buffer, size_t length )
    int             AKUMountVirtualDirectory        ( char* virtualPath, char* archive )
    int             AKUSetWorkingDirectory          ( char* path )

    void            AKUCallFunc                     ()
    void            AKUCallFuncWithArgArray         ( char* exeName, char* scriptName, int argc, char** argv, int asParams )
    void            AKUCallFuncWithArgString        ( char* exeName, char* scriptName, char* args, int asParams )
    void            AKULoadFuncFromBuffer           ( void* data, size_t size, int dataType, int compressed )
    void            AKULoadFuncFromFile             ( const char* filename )
    void            AKULoadFuncFromString           ( const char* script )

    # ctypedef void ( *AKUErrorTracebackFunc )        ( char* message, lua_State* L, int level )
    # void            AKUSetFunc_ErrorTraceback       ( AKUErrorTracebackFunc func )

cdef extern from "moai-util/host.h":
    void            AKUUtilAppFinalize          ()
    void            AKUUtilAppInitialize        ()
    void            AKUUtilContextInitialize    ()

cdef extern from "moai-untz/host.h":
    void            AKUUntzAppFinalize          ()
    void            AKUUntzAppInitialize        ()
    void            AKUUntzContextInitialize    ()

cdef extern from "moai-box2d/host.h":
    void            AKUBox2DAppFinalize         ()
    void            AKUBox2DAppInitialize       ()
    void            AKUBox2DContextInitialize   ()

cdef extern from "moai-fmod-studio/host.h":
    void            AKUFmodStudioAppFinalize          ()
    void            AKUFmodStudioAppInitialize        ()
    void            AKUFmodStudioContextInitialize    ()
    void            AKUFmodStudioUpdate               ()

cdef extern from "moai-http-client/host.h":
    void            AKUHttpClientAppFinalize        ()
    void            AKUHttpClientAppInitialize      ()
    void            AKUHttpClientContextInitialize  ()
    void            AKUHttpClientUpdate             ()

cdef extern from "moai-crypto/host.h":
    void            AKUCryptoAppFinalize        ()
    void            AKUCryptoAppInitialize      ()
    void            AKUCryptoContextInitialize  ()

cdef extern from "moai-spine/host.h":
    void            AKUSpineAppFinalize        ()
    void            AKUSpineAppInitialize      ()
    void            AKUSpineContextInitialize  ()    

# cdef extern from "moai-plugins/host.h":
#     void            AKUPluginsAppFinalize           ()
#     void            AKUPluginsAppInitialize         ()
#     void            AKUPluginsContextInitialize     ()
#     void            AKUPluginsUpdate                ()

cdef extern from "lua-headers/moai_lua.h":
    cdef int moai_lua_SIZE
    cdef unsigned char moai_lua[]
    cdef int AKU_DATA_BYTECODE
    cdef int AKU_DATA_STRING
    cdef int AKU_DATA_ZIPPED
    cdef int AKU_DATA_UNCOMPRESSED

cdef extern from "moai-luaext/host.h":
    void            AKULuaExtAppFinalize      ()
    void            AKULuaExtAppInitialize    ()
    void            AKULuaExtContextInitialize()

cdef extern from "moai-sim/host.h":
    # setup
    void            AKUSimAppFinalize              ()
    void            AKUSimAppInitialize            ()
    void            AKUSimContextInitialize        ()

    # management api
    void            AKUDetectGfxContext             ()
    double          AKUGetSimStep                   ()
    void            AKUPause                        ( bint pause )
    void            AKURender                       ()
    void            AKUSetOrientation               ( int orientation )
    void            AKUSetScreenDpi                 ( int dpi )
    void            AKUSetScreenSize                ( int width, int height )
    void            AKUSetViewSize                  ( int width, int height )
    void            AKUUpdate                       ()

    # callback management
    ctypedef void ( *AKUEnterFullscreenModeFunc )    ()
    ctypedef void ( *AKUExitFullscreenModeFunc )     ()
    ctypedef void ( *AKUOpenWindowFunc )             ( const char* title, int width, int height )
    ctypedef void ( *AKUSetSimStepFunc )             ( double step )

    void        AKUSetFunc_OpenWindow           ( AKUOpenWindowFunc func )
    void        AKUSetFunc_SetSimStep           ( AKUSetSimStepFunc func )
    void        AKUSetFunc_EnterFullscreenMode  ( AKUEnterFullscreenModeFunc func )
    void        AKUSetFunc_ExitFullscreenMode   ( AKUExitFullscreenModeFunc func )

    # input device api
    void            AKUReserveInputDevices          ( int total )
    void            AKUReserveInputDeviceSensors    ( int deviceID, int total )
    void            AKUSetInputConfigurationName    ( char* name )
    void            AKUSetInputDevice               ( int deviceID, char* name )
    void            AKUSetInputDeviceActive         ( int deviceID, bint active )
    void            AKUSetInputDeviceButton         ( int deviceID, int sensorID, char* name )
    void            AKUSetInputDeviceCompass        ( int deviceID, int sensorID, char* name )
    void            AKUSetInputDeviceKeyboard       ( int deviceID, int sensorID, char* name )
    void            AKUSetInputDeviceLevel          ( int deviceID, int sensorID, char* name )
    void            AKUSetInputDeviceLocation       ( int deviceID, int sensorID, char* name )
    void            AKUSetInputDevicePointer        ( int deviceID, int sensorID, char* name )
    void            AKUSetInputDeviceTouch          ( int deviceID, int sensorID, char* name )
    void            AKUSetInputDeviceWheel          ( int deviceID, int sensorID, char* name )

    # input events api
    void            AKUEnqueueButtonEvent           ( int deviceID, int sensorID, bint down )
    void            AKUEnqueueCompassEvent          ( int deviceID, int sensorID, float heading )
    void            AKUEnqueueKeyboardCharEvent     ( int deviceID, int sensorID, int unicodeChar )
    void            AKUEnqueueKeyboardEditEvent     ( int deviceID, int sensorID, char* text, int start, int editLength, int maxLength)
    void            AKUEnqueueKeyboardKeyEvent      ( int deviceID, int sensorID, int keyID, int down )
    void            AKUEnqueueKeyboardTextEvent     ( int deviceID, int sensorID, char* text )
    void            AKUEnqueueLevelEvent            ( int deviceID, int sensorID, float x, float y, float z )
    void            AKUEnqueueLocationEvent         ( int deviceID, int sensorID, double longitude, double latitude, double altitude, float hAccuracy, float vAccuracy, float speed )
    void            AKUEnqueuePointerEvent          ( int deviceID, int sensorID, int x, int y )
    void            AKUEnqueueTouchEvent            ( int deviceID, int sensorID, int touchID, bint down, float x, float y )
    void            AKUEnqueueTouchEventCancel      ( int deviceID, int sensorID )
    void            AKUEnqueueWheelEvent            ( int deviceID, int sensorID, float value )

cdef extern from "moai-sim/MOAIKeyCodeEnum.h":
    enum MOAIKeyCodes:
        MOAI_KEY_BACKSPACE
        MOAI_KEY_TAB
        MOAI_KEY_RETURN
        MOAI_KEY_SHIFT
        MOAI_KEY_CONTROL
        MOAI_KEY_ALT
        MOAI_KEY_PAUSE
        MOAI_KEY_CAPS_LOCK
        MOAI_KEY_ESCAPE
        MOAI_KEY_SPACE
        MOAI_KEY_PAGE_UP
        MOAI_KEY_PAGE_DOWN
        MOAI_KEY_END
        MOAI_KEY_HOME
        MOAI_KEY_LEFT
        MOAI_KEY_UP
        MOAI_KEY_RIGHT
        MOAI_KEY_DOWN
        MOAI_KEY_PRINT_SCREEN
        MOAI_KEY_INSERT
        MOAI_KEY_DELETE
        MOAI_KEY_DIGIT_0
        MOAI_KEY_DIGIT_1
        MOAI_KEY_DIGIT_2
        MOAI_KEY_DIGIT_3
        MOAI_KEY_DIGIT_4
        MOAI_KEY_DIGIT_5
        MOAI_KEY_DIGIT_6
        MOAI_KEY_DIGIT_7
        MOAI_KEY_DIGIT_8
        MOAI_KEY_DIGIT_9
        MOAI_KEY_A
        MOAI_KEY_B
        MOAI_KEY_C
        MOAI_KEY_D
        MOAI_KEY_E
        MOAI_KEY_F
        MOAI_KEY_G
        MOAI_KEY_H
        MOAI_KEY_I
        MOAI_KEY_J
        MOAI_KEY_K
        MOAI_KEY_L
        MOAI_KEY_M
        MOAI_KEY_N
        MOAI_KEY_O
        MOAI_KEY_P
        MOAI_KEY_Q
        MOAI_KEY_R
        MOAI_KEY_S
        MOAI_KEY_T
        MOAI_KEY_U
        MOAI_KEY_V
        MOAI_KEY_W
        MOAI_KEY_X
        MOAI_KEY_Y
        MOAI_KEY_Z
        MOAI_KEY_GUI
        MOAI_KEY_APPLICATION
        MOAI_KEY_NUM_0
        MOAI_KEY_NUM_1
        MOAI_KEY_NUM_2
        MOAI_KEY_NUM_3
        MOAI_KEY_NUM_4
        MOAI_KEY_NUM_5
        MOAI_KEY_NUM_6
        MOAI_KEY_NUM_7
        MOAI_KEY_NUM_8
        MOAI_KEY_NUM_9
        MOAI_KEY_NUM_MULTIPLY
        MOAI_KEY_NUM_PLUS
        MOAI_KEY_NUM_MINUS
        MOAI_KEY_NUM_DECIMAL
        MOAI_KEY_NUM_DIVIDE
        MOAI_KEY_F1
        MOAI_KEY_F2
        MOAI_KEY_F3
        MOAI_KEY_F4
        MOAI_KEY_F5
        MOAI_KEY_F6
        MOAI_KEY_F7
        MOAI_KEY_F8
        MOAI_KEY_F9
        MOAI_KEY_F10
        MOAI_KEY_F11
        MOAI_KEY_F12
        MOAI_KEY_NUM_LOCK
        MOAI_KEY_SCROLL_LOCK
        MOAI_KEY_OEM_1
        MOAI_KEY_OEM_PLUS
        MOAI_KEY_OEM_COMMA
        MOAI_KEY_OEM_MINUS
        MOAI_KEY_OEM_PERIOD
        MOAI_KEY_OEM_2
        MOAI_KEY_OEM_3
        MOAI_KEY_OEM_4
        MOAI_KEY_OEM_5
        MOAI_KEY_OEM_6
        MOAI_KEY_OEM_7
        MOAI_KEY_OEM_8
        MOAI_KEY_OEM_102
        MOAI_KEY_TOTAL
        MOAI_KEY_INVALID


cdef extern from "ParticlePresets.h":
    void            ParticlePresets                 ()


