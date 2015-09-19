--------------------------------------------------------------------------------
-- Table extensions (lua-enumerable)
--------------------------------------------------------------------------------
local serpent = require("util.Serpent")

table.includes = function(list, value)
    for i,x in ipairs(list) do
        if (x == value) then
            return(true)
        end
    end
    return(false)
end

table.detect = function(list, func)
    for i,x in ipairs(list) do
        if (func(x, i)) then
            return(x)
        end
    end
    return(nil)
end

table.without = function(list, item)
    return table.reject(list, function (x) 
        return x == item 
    end)
end

table.indexOf = function(list, item)
    for i, v in ipairs(list) do
        if v == item then
            return i
        end
    end
    return 0
end

table.removeElement = function(list, item)
    local i = table.indexOf(list, item)
    if i > 0 then
        table.remove(list, i)
    end
    return i
end

table.each = function(list, func)
    for i,v in ipairs(list) do
        func(v, i)
    end
end

table.every = function(list, func)
    for i,v in pairs(list) do
        func(v, i)
    end
end

table.select = function(list, func)
    local results = {}
    for i,x in ipairs(list) do
        if (func(x, i)) then
            table.insert(results, x)
        end
    end
    return(results)
end

table.reject = function(list, func)
    local results = {}
    for i,x in ipairs(list) do
        if (func(x, i) == false) then
            table.insert(results, x)
        end
    end
    return(results)
end

table.partition = function(list, func)
    local matches = {}
    local rejects = {}
    
    for i,x in ipairs(list) do
        if (func(x, i)) then
            table.insert(matches, x)
        else
            table.insert(rejects, x)
        end
    end
    
    return matches, rejects
end

table.merge = function(source, destination)
    for k,v in pairs(destination) do source[k] = v end
    return source
end

table.unshift = function(list, val)
    table.insert(list, 1, val)
end

table.shift = function(list)
    return table.remove(list, 1)
end

table.pop = function(list)
    return table.remove(list)
end

table.push = function(list, item)
    return table.insert(list, item)
end

table.insertIfAbsent = function(list, item)
    if table.includes(list, item) then
        return false
    end
    list[#list+1]=item
    return true
end

table.collect = function(source, func) 
    local result = {}
    for i,v in ipairs(source) do table.insert(result, func(v)) end
    return result
end

table.empty = function(source) 
    return source == nil or next(source) == nil
end

table.present = function(source)
    return not(table.empty(source))
end

table.random = function(source)
    return source[math.random(1, #source)]
end

table.times = function(limit, func)
    for i = 1, limit do
        func(i)
    end
end

table.reverse = function(source)
    local result = {}
    for i,v in ipairs(source) do table.unshift(result, v) end
    return result
end

table.dup = function(source)
    local result = {}
    for k,v in pairs(source) do result[k] = v end
    return result
end

-- fisher-yates shuffle
table.shuffle = function(t)
    local n = #t
    while n > 2 do
        local k = math.random(n)
        t[n], t[k] = t[k], t[n]
        n = n - 1
    end
    return t
end

table.keys = function(source)
    local result = {}
    for k,v in pairs(source) do
        table.push(result, k)
    end
    return result
end

table.concatWith = function(t1, t2)
    local res = t1
    for i = 1, #t2 do 
        res[#res + 1] = t2[i]
    end
    return res
end

table.deepcompare = function (t1, t2)
    local ty1 = type(t1)
    local ty2 = type(t2)
    if ty1 ~= ty2 then return false end
    -- non-table types can be directly compared
    if ty1 ~= 'table' and ty2 ~= 'table' then return t1 == t2 end

    for k1,v1 in pairs(t1) do
        local v2 = t2[k1]
        if v2 == nil or not table.deepcompare(v1, v2) then return false end
    end
    for k2,v2 in pairs(t2) do
        local v1 = t1[k2]
        if v1 == nil or not table.deepcompare(v1, v2) then return false end
    end
    return true
end

local function escape ( str )
    if str then
        -- convert line endings
        str = string.gsub ( str, "\n", "\r\n" )        
        -- escape all special characters
        str = string.gsub ( str, "([^%w ])",
            function ( c ) 
                return string.format ( "%%%02X", string.byte ( c )) 
            end
        )
        -- convert spaces to "+" symbols
        str = string.gsub ( str, " ", "+" )
    end    
    return str
end

table.urlEncode = function(source)
    local s = ""
    for k, v in pairs ( source ) do
        s = s .. "&" .. escape ( k ) .. "=" .. escape ( v )
    end
    return string.sub ( s, 2 ) -- remove first '&'
end

table.count = function(t)
    local c = 0
    for k, v in pairs(t) do
        c = c + 1
    end
    return c
end

table.pretty = function ( t, ignoredKeys )
    return serpent.pretty ( t, {keyignore = ignoredKeys} )
end
