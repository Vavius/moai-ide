-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

---
-- Global namespace pollution + altering built-ins
require("util.globals.class")
require("util.globals.log")
require("util.globals.string")
require("util.globals.table")

App             = require("core.App")
Event           = require("core.Event")
EventDispatcher = require("core.EventDispatcher")
ResourceMgr     = require("core.ResourceMgr")
RenderMgr       = require("core.RenderMgr")
Runtime         = require("core.Runtime")
