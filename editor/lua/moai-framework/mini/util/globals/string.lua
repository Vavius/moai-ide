--------------------------------------------------------------------------------
-- String extensions
--------------------------------------------------------------------------------
local DEFAULT_SEP = package.config:sub(1, 1)

-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
-- string interpolation:
-- "%[key] = %[value]" % {key = "speed", value = 345.24}     => speed = 345.24
-- "progress: %[some]" % "single arg"                        => progress: single arg
local function interp(s, tab)
    if type(tab) == "table" then
        if #tab > 0 then
            return string.format(s, unpack(tab))
        else
            return (s:gsub('(%%%b[])', function(w) return tab[w:sub(3, -2)] or w end))
        end
    else
        return string.format(s, tab)
    end
end
getmetatable("").__mod = interp
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

function string.endswith(s, send)
    return #s >= #send and s:find(send, #s-#send+1, true) and true or false
end

function string.pathDir(path)
    return path:match(".*" .. DEFAULT_SEP)
end

function string.pathFile(path)
    local dir = string.pathDir(path)
    if dir then
        return path:sub(#dir + 1)
    else
        return path
    end
end

local function join(leading, trailing)
    leading = leading or ""
    
    if not trailing then
        return leading
    end
    
    if trailing:sub(1, 1) == DEFAULT_SEP then
        return trailing
    end

    if leading == "." then
        leading = ""
    end
    
    if leading:len() > 0 and not leading:endswith(DEFAULT_SEP) then
        leading = leading .. DEFAULT_SEP
    end
    
    return leading .. trailing
end

function string.pathJoin(...)
    local components = {...}
    local result = components[1]
    for i = 2, #components do
        result = join(result, components[i])
    end
    return result
end

-- example: FF0066FF -> 1.0, 0, 0.4
function string.hexToRGBA(s)
    local a = string.sub(s, 7, 8)
    if #a == 0 then
        a = 1.0
    else 
        a = tonumber(a, 16) / 255.0
    end
    return  tonumber(string.sub(s, 1, 2), 16) / 255.0,
            tonumber(string.sub(s, 3, 4), 16) / 255.0,
            tonumber(string.sub(s, 5, 6), 16) / 255.0,
            a
end
