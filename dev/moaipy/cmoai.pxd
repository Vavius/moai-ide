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

cdef extern from "moai-fmod-studio/host.h":
    void            AKUFmodStudioAppFinalize          ()
    void            AKUFmodStudioAppInitialize        ()
    void            AKUFmodStudioContextInitialize    ()
    void            AKUFmodStudioUpdate               ()

cdef extern from "moai-http-client/host.h":
    void            AKUHttpClientAppFinalize        ()
    void            AKUHttpClientAppInitialize      ()
    void            AKUHttpClientContextInitialize  ()

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
    void            AKUEnqueueKeyboardAltEvent      ( int deviceID, int sensorID, bint down )
    void            AKUEnqueueKeyboardControlEvent  ( int deviceID, int sensorID, bint down )
    void            AKUEnqueueKeyboardEvent         ( int deviceID, int sensorID, int keyID, bint down )
    void            AKUEnqueueKeyboardShiftEvent    ( int deviceID, int sensorID, bint down )
    void            AKUEnqueueLevelEvent            ( int deviceID, int sensorID, float x, float y, float z )
    void            AKUEnqueueLocationEvent         ( int deviceID, int sensorID, double longitude, double latitude, double altitude, float hAccuracy, float vAccuracy, float speed )
    void            AKUEnqueuePointerEvent          ( int deviceID, int sensorID, int x, int y )
    void            AKUEnqueueTouchEvent            ( int deviceID, int sensorID, int touchID, bint down, float x, float y )
    void            AKUEnqueueTouchEventCancel      ( int deviceID, int sensorID )
    void            AKUEnqueueWheelEvent            ( int deviceID, int sensorID, float value )




