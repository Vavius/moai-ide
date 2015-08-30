--------------------------------------------------------------------------------
--
--
--
--------------------------------------------------------------------------------

--============================================================================--
-- Console
--============================================================================--

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
local Console = {}

local __print
local p = print

function Console.setPrint(func1, func2)
    __print = function(...)
        local n = select("#", ...)
        local arg = {...}
        local out = {}
        for i = 1, n do
            p(i, arg[i])
            table.insert(out, tostring(arg[i]))
        end
        func1(table.concat(out, '\t'))
    end

    log.__console = function(...)
        local n = select("#", ...)
        local arg = {...}
        local out = {}
        for i = 1, n do
            p(i, arg[i])
            table.insert(out, tostring(arg[i]))
        end
        func2(table.concat(out, '\t'))
    end
end

function Console.output(obj)
    local out = table.pretty(obj)
    return out
end

function Console.outputCommand(...)
    local n = select("#", ...)
    local arg = {...}

    -- pcall failed. bail
    if not arg[1] then
        local msg = arg[2]
        return msg .. '\n' .. debug.traceback()
    end

    local output = {}
    -- print all results
    for i = 2, n do
        local obj = arg[i]
        local more = i < n
        if type(obj) == 'table' then
            local out = table.pretty(obj)
            if i > 2 then out = '\n' .. out end
            if more then out = out .. ',\n' end
            table.insert(output, out)
        else
            local out = table.pretty(obj)
            if more then out = out .. ', ' end
            table.insert(output, out)
        end
    end
    return table.concat(output)
end

function Console.run(command)
    local result, msg = loadstring(command)
    if not result then
        return Console.output(msg)
    end

    if __print then
        local env = {}
        env.print = __print
        setmetatable(env, {__index = _G, __newindex = _G})
        setfenv(result, env)
    end

    return Console.outputCommand(pcall(result))
end


return Console
