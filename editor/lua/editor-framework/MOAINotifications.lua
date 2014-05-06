--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------


local MOAINotifications = {  }

MOAINotifications.LOCAL_NOTIFICATION_MESSAGE_RECEIVED = 0
MOAINotifications.REMOTE_NOTIFICATION_MESSAGE_RECEIVED = 2

local listenerTable = {  }

function MOAINotifications.setListener(event, callback)
    listenerTable[event] = callback
end

function MOAINotifications.dispatchEvent(event, ...)
    if listenerTable[event] then
        listenerTable[event](...)
    end
end

return MOAINotifications