----------------------------------------------------------------------------------------------------
-- @type EventListener
-- 
-- A virtual superclass for EventListeners.
-- Classes which inherit from this class become able to receive events.
-- Currently intended for internal use only.
----------------------------------------------------------------------------------------------------

local Event = require("core.Event")

local EventListener = class()

---
-- The constructor.
-- @param eventType The type of event.
-- @param callback The callback function.
-- @param source The source.
-- @param priority The priority.
-- @param safecall  Don't propagate errors inside listener callback (pcall)
function EventListener:init(eventType, callback, source, priority, safecall)
    self.type = eventType
    self.callback = callback
    self.source = source
    self.priority = priority or 0
    
    if safecall then
        self.call = self.pcall
    end
end

---
-- Call the event listener.
-- @param event Event
function EventListener:call(event)
    if self.source then
        self.callback(self.source, event)
    else
        self.callback(event)
    end
end


function EventListener:pcall(event)
    local status, msg
    if self.source then
        status, msg = pcall(self.callback, self.source, event)
    else
        status, msg = pcall(self.callback, event)
    end

    if not status then
        if EventListener.TracebackHandler then
            EventListener.TracebackHandler(msg)
        else
            log.error(msg, '\n', debug.traceback())
        end
    end
end

return EventListener
