--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------


local MOAIApp = {}

MOAIApp.APP_OPENED_FROM_URL = 0
MOAIApp.SESSION_START = 1
MOAIApp.SESSION_END = 2
MOAIApp.BACK_BUTTON_PRESSED = 3

local listenerTable = {  }

function MOAIApp.setListener(event, callback)
    if event then
        listenerTable[event] = callback
    end
end

function MOAIApp.dispatchEvent(event, ...)
    if listenerTable[event] then
        listenerTable[event](...)
    end
end

return MOAIApp