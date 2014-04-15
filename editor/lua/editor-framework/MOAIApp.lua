--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------


local MOAIApp = {  }

MOAIApp.APP_OPENED_FROM_URL = 0
MOAIApp.SESSION_START = 1
MOAIApp.SESSION_END = 2

local listenerTable = {  }

function MOAIApp.setListener(event, callback)
    listenerTable[event] = callback
end

function MOAIApp.dispatchEvent(event, ...)
    if listenerTable[event] then
        listenerTable[event](...)
    end
end

return MOAIApp