--------------------------------------------------------------------------------
-- log.lua
-- 
-- Log output with support for log levels
--------------------------------------------------------------------------------


log = {}

--------------------------------------------------------------------------------
-- Log levels
--------------------------------------------------------------------------------

-- Detailed information, typically of interest only when diagnosing problems. 
-- Alias: log.console() to be overrided by IDE with output console
log.DEBUG = 1

-- Confirmation that things are working as expected.
log.INFO = 2

-- An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’). 
-- The software is still working as expected.
log.WARNING = 3

-- Due to a more serious problem, the software has not been able to perform some function.
log.ERROR = 4

-- A serious error, indicating that the program itself may be unable to continue running.
-- Alias: log.alert() that can be overrided with app-specific code to show gui alert to user
log.CRITICAL = 5


-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- Framework Log messages
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
log.NOT_ENOUGH_SPACE = "not_enough_space"


function log.setLogLevel(level)
    local empty = function() end
    
    log.console  = (level <= log.DEBUG)    and function(...) log.__console(...) end or empty
    log.debug    = (level <= log.DEBUG)    and log.__debug or empty
    log.info     = (level <= log.INFO)     and log.__info or empty
    log.warning  = (level <= log.WARNING)  and log.__warning or empty
    log.error    = (level <= log.ERROR)    and log.__error or empty
    log.critical = (level <= log.CRITICAL) and log.__critical or empty
    log.alert    = (level <= log.CRITICAL) and log.__alert or empty
end


local function __print(...)
    local n = select("#", ...)
    local output = {...}

    for i = 1, n do
        output[i] = tostring(output[i])
    end

    output[n + 1] = '\n'

    MOAILogMgr.log(table.concat(output, " "))
end

---
-- Logging functions exposed in module
-- User can modify them for custom messages or behavior

log.__print = print

function log.__console(...)
    __print("DEBUG:    ", ...)
end

function log.__debug(...)
    __print("DEBUG:    ", ...)
end

function log.__info(...)
    __print("INFO:     ", ...)
end

function log.__warning(...)
    __print("WARNING:  ", ...)
end

function log.__error(...)
    __print("ERROR:    ", ...)
end

function log.__critical(...)
    __print("CRITICAL: ", ...)
end

function log.__alert(...)
    __print("ALERT: ", ...)
end


log.setLogLevel(log.DEBUG)




