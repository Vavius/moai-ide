----------------------------------------------------------------------------------------------------
-- @type Runtime
--
-- This is a utility class which starts immediately upon library load
-- and acts as the single handler for different MOAI events from MOAIAppIOS and MOAISim. 
----------------------------------------------------------------------------------------------------
local Event = require("core.Event")
local EventDispatcher = require("core.EventDispatcher")

local Runtime = EventDispatcher()

-- initialize
function Runtime:initialize()
    MOAIGfxDevice.setListener(MOAIGfxDevice.EVENT_RESIZE, self.onResize)

    if MOAIAppIOS then
        MOAIAppIOS.setListener(MOAIAppIOS.DID_BECOME_ACTIVE, self.onSessionStart)
        MOAIAppIOS.setListener(MOAIAppIOS.WILL_RESIGN_ACTIVE, self.onSessionEnd)
        MOAIAppIOS.setListener(MOAIAppIOS.DID_RECIEVE_MEMORY_WARNING, self.onMemoryWarning)
        MOAIAppIOS.setListener(MOAIAppIOS.APP_OPENED_FROM_URL, self.onOpenedFromUrl)
    elseif MOAIAppAndroid then
        MOAIAppAndroid.setListener(MOAIAppAndroid.ACTIVITY_ON_START, self.onSessionStart)
        MOAIAppAndroid.setListener(MOAIAppAndroid.ACTIVITY_ON_STOP, self.onSessionEnd)
        MOAIAppAndroid.setListener(MOAIAppAndroid.APP_OPENED_FROM_URL, self.onOpenedFromUrl)
        MOAIAppAndroid.setListener(MOAIAppAndroid.BACK_BUTTON_PRESSED, self.onBackButtonPressed)
    end

    MOAISim.setListener(MOAISim.EVENT_PAUSE, self.onPause)
    MOAISim.setListener(MOAISim.EVENT_RESUME, self.onResume)
end

-- view resize
function Runtime.onResize(width, height)
    local e = Event(Event.RESIZE)
    e.width = width
    e.height = height
    Runtime:dispatchEvent(e)
end

function Runtime.onPause()
    Runtime:dispatchEvent(Event.PAUSE)
end

function Runtime.onResume()
    Runtime:dispatchEvent(Event.RESUME)
end

function Runtime.onSessionStart(resumed)
    local e = Event(Event.SESSION_START)
    log.info('========================== Session Start ==========================')
    e.resumed = resumed
    Runtime:dispatchEvent(e)
end

function Runtime.onSessionEnd()
    log.info('========================== Session End ==========================')
    Runtime:dispatchEvent(Event.SESSION_END)
end

function Runtime.onMemoryWarning()
    ResourceMgr:softReleaseResources(10)
end

-- cache event for performance
local backButtonEvent = Event(Event.BACK_BUTTON_PRESSED)
function Runtime.onBackButtonPressed()
    Runtime:dispatchEvent(backButtonEvent)
    return backButtonEvent.stopFlag
end

function Runtime.onOpenedFromUrl(url)
    local e = Event(Event.OPENED_FROM_URL)
    e.url = url
    Runtime:dispatchEvent(e)    
end

return Runtime