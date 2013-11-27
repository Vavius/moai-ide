cdef extern from "moai-core/host.h":
    ctypedef struct lua_State:
        pass
    ctypedef int AKUContextID

    void            AKUClearMemPool                 ()
    AKUContextID    AKUCreateContext                ()
    void            AKUDeleteContext                ( AKUContextID context )
    AKUContextID    AKUGetContext                   ()
    void*           AKUGetUserdata                  ()
    void            AKUFinalize                     ()
    void            AKUInitMemPool                  ( size_t sizeInBytes )
    void            AKUSetContext                   ( AKUContextID context )
    void            AKUSetUserdata                  ( void* user )

    # management api
    lua_State*      AKUGetLuaState                  ()
    char*           AKUGetMoaiVersion               ( char* buffer, size_t length )
    char*           AKUGetWorkingDirectory          ( char* buffer, size_t length )
    int             AKUMountVirtualDirectory        ( char* virtualPath, char* archive )
    void            AKURunData                      ( void* data, size_t size, int dataType, int compressed )
    void            AKURunScript                    ( char* filename )
    void            AKURunString                    ( char* script )
    int             AKUSetWorkingDirectory          ( char* path )
    void            AKUSetArgv                      ( char **argv )

cdef extern from "moai-sim/host.h":
    # setup
    void            AKUFinalizeSim              ()
    void            AKUInitializeSim            ()

    # management api
    void            AKUDetectGfxContext             ()
    double          AKUGetSimStep                   ()
    void            AKUPause                        ( bint pause )
    void            AKUReleaseGfxContext            ()
    void            AKURender                       ()
    void            AKUSetOrientation               ( int orientation )
    void            AKUSetScreenDpi                 ( int dpi )
    void            AKUSetScreenSize                ( int width, int height )
    void            AKUSetViewSize                  ( int width, int height )
    void            AKUSoftReleaseGfxResources      ( int age )
    void            AKUUpdate                       ()

    # callback management
    #void            AKUSetFunc_EnterFullscreenMode  ( AKUEnterFullscreenModeFunc func );
    #void            AKUSetFunc_ExitFullscreenMode   ( AKUExitFullscreenModeFunc func );
    #void            AKUSetFunc_OpenWindow           ( AKUOpenWindowFunc func );
    #void            AKUSetFunc_SetSimStep           ( AKUSetSimStepFunc func );

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