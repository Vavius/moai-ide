#ifndef	GIIHELPER_H
#define	GIIHELPER_H
#include <moai-core/pch.h>
#include <moai-core/MOAILogMessages.h>

#include <moai-sim/pch.h>
#include <moai-sim/MOAIActionMgr.h>
#include <moai-sim/MOAIGfxDevice.h>
#include <moai-sim/MOAIInputMgr.h>
#include <moai-sim/MOAINodeMgr.h>
#include <moai-sim/MOAISim.h>
// #include <moaicore/MOAITextureBase.h>
// #include <moaicore/MOAIDebugLines.h>
#include <moai-sim/MOAIFrameBuffer.h>
#include <moai-sim/MOAIProp.h>


class GIIHelper:
	public MOAIGlobalClass < GIIHelper, MOAILuaObject > 
{
private:
	
	//----------------------------------------------------------------//
	static int _stepSim             ( lua_State* L );
	static int _updateInput         ( lua_State* L );
	static int _setBufferSize       ( lua_State* L );
	static int _renderFrameBuffer   ( lua_State* L );
	static int _setVertexTransform  ( lua_State* L );

public:
	
	DECL_LUA_SINGLETON ( GIIHelper )

	//
	void stepSim( double step );
	void updateInput();

	//----------------------------------------------------------------//
	GIIHelper();
	~GIIHelper();
	
	void			RegisterLuaClass	( MOAILuaState& state );
};

extern "C"{
	void registerGIIHelper();
}


#endif