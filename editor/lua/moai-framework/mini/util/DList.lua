-- Based on doubly linked list by Cosmin Apreutesei
-- https://code.google.com/p/lua-files/source/browse/dlist.lua
-- 

local List = class()


function List:init()
    self:clear()
end

function List:clear()
    self.head = nil
    self.tail = nil
end

function List:push(item)
    if self.tail then
        self.tail._next = item
        item._prev = self.tail
        self.tail = item
    else
        self.head = item
        self.tail = item
    end
end

function List:unshift(item)
    if self.head then
        self.head._prev = item
        item._next = self.head
        self.head = item
    else
        self.head = item
        self.tail = item
    end
end

function List:insertAfter(item, after)
    if not after then
        return self:push(item)
    end

    if after._next then
        after._next._prev = item
        item._next = after._next
    else
        self.tail = item
    end
    item._prev = after
    after._next = item
end

function List:insertBefore(item, before)
    if not before or not before._prev then
        return self:unshift(item)
    end
    return self:insertAfter(item, before._prev)
end

function List:remove(t)
    if t._next then
        if t._prev then
            t._next._prev = t._prev
            t._prev._next = t._next
        else
            t._next._prev = nil
            self.head = t._next
        end
    elseif t._prev then
        t._prev._next = nil
        self.tail = t._prev
    else
        self.head = nil
        self.tail = nil
    end

    t._deleted = true

    -- keep references to allow removal of current iterator head
    -- t._next = nil
    -- t._prev = nil

    return t
end

function List:isEmpty()
    return self.head == nil
end

function List:next(last)
    local n
    if last then
        n = last._next
    else
        n = self.head
    end
    if n and n._deleted then
        return self:next(n)
    end
    return n
end

function List:items()
    return self.next, self, nil
end

function List:prev(last)
    local p
    if last then
        p = last._prev
    else
        p = self.tail
    end
    if p and p._deleted then
        return self:prev(p)
    end
    return p
end

function List:reverse_items()
    return self.prev, self, nil
end

return List
