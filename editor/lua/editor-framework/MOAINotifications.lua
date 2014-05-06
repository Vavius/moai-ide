--------------------------------------------------------------------------------
-- MOAINotifications.lua
-- 
-- Mock class to test notifications in simulator
--------------------------------------------------------------------------------


local MOAINotifications = {  }

MOAINotifications.LOCAL_NOTIFICATION_MESSAGE_RECEIVED = 0
MOAINotifications.REMOTE_NOTIFICATION_MESSAGE_RECEIVED = 2

local listenerTable = {  }

local badgeNumber = 0

function MOAINotifications.setListener(event, callback)
    listenerTable[event] = callback
end

function MOAINotifications.dispatchEvent(event, ...)
    if listenerTable[event] then
        listenerTable[event](...)
    end
end

--------------------------------------------------------------------------------
-- Mock methods

function MOAINotifications.getAppIconBadgeNumber()
    return badgeNumber
end

function MOAINotifications.localNotificationInSeconds()
    -- pass
end

function MOAINotifications.registerForRemoteNotifications()
    -- pass
end

function MOAINotifications.setAppIconBadgeNumber(num)
    badgeNumber = num
end

function MOAINotifications.unregisterForRemoteNotifications()
    -- pass
end


return MOAINotifications