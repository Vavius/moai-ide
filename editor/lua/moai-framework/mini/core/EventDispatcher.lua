----------------------------------------------------------------------------------------------------
-- @type EventDispatcher
--
-- This class is responsible for event notifications.
----------------------------------------------------------------------------------------------------
local Event = require("core.Event")
local EventListener = require("core.EventListener")
local DList = require("util.DList")

local EventDispatcher = class()

EventDispatcher.EVENT_CACHE = {}



--------------------------------------------------------------------------------
-- The constructor.
-- @param eventType (option)The type of event.
--------------------------------------------------------------------------------
function EventDispatcher:init()
    self.eventListenersMap = {}
end


function EventDispatcher:addEventListenerSafe(eventType, callback, source, priority)
    self:addEventListener(eventType, callback, source, priority, true)
end

---
-- Adds an event listener.
-- will now catch the events that are sent in the dispatchEvent.
-- @param eventType Target event type.
-- @param callback The callback function.
-- @param source (option)The first argument passed to the callback function.
-- @param priority (option)Notification order.
function EventDispatcher:addEventListener(eventType, callback, source, priority, safe)
    assert(eventType)
    assert(callback)

    if self:hasEventListener(eventType, callback, source) then
        return false
    end

    if not self.eventListenersMap[eventType] then
        self.eventListenersMap[eventType] = DList()
    end

    local listener = EventListener(eventType, callback, source, priority, safe)
    
    local list = self.eventListenersMap[eventType]
    local before
    for i in list:items() do
        if listener.priority <= i.priority then
            before = i
            break
        end
    end
    if before then
        list:insertBefore(listener, before)
    else
        list:push(listener)
    end
    return true
end

---
-- Removes an event listener.
-- @param eventType Type of event to be deleted
-- @param callback Callback function of event to be deleted
-- @param source (option)Source of event to be deleted
-- @return True if it can be removed
function EventDispatcher:removeEventListener(eventType, callback, source)
    assert(eventType)
    assert(callback)

    local list = self.eventListenersMap[eventType]
    if not list then
        return false
    end

    local item
    for i in list:items() do
        if i.type == eventType and i.callback == callback and i.source == source then
            item = i
        end
    end

    if item then 
        list:remove(item)
        return true
    end
    return false
end

---
-- Returns true if you have an event listener.
-- @param eventType
-- @param callback
-- @param source
-- @return Returns true if you have an event listener matching the criteria.
function EventDispatcher:hasEventListener(eventType, callback, source)
    assert(eventType)

    local list = self.eventListenersMap[eventType]
    if not list or list:isEmpty() then
        return false
    end

    if callback == nil and source == nil then
        return true
    end

    for i in list:items() do
        if i.type == eventType and i.callback == callback and i.source == source then
            return true
        end
    end
    return false
end

---
-- Dispatches the event.
-- @param event Event object or Event type name.
-- @param data Data that is set in the event.
function EventDispatcher:dispatchEvent(event, data)
    local eventName = type(event) == "string" and event
    if eventName then
        event = EventDispatcher.EVENT_CACHE[eventName] or Event(eventName)
        EventDispatcher.EVENT_CACHE[eventName] = nil
    end

    assert(event.type)

    event.stopFlag = false
    event.target = self.eventTarget or self
    if data ~= nil then
        event.data = data
    end

    local list = self.eventListenersMap[event.type]
    if not list then return end

    for i in list:items() do
        if i.type == event.type then
            event:setListener(i.callback, i.source)
            i:call(event)
            if event.stopFlag == true then
                break
            end
        end
    end

    if eventName then
        EventDispatcher.EVENT_CACHE[eventName] = event
    end

    -- reset properties to free resources used in cached events
    event.data = nil
    event.target = nil
    event:setListener(nil, nil)
end

---
-- Remove all event listeners.
function EventDispatcher:clearEventListeners()
    self.eventListenersMap = {}
end


return EventDispatcher
