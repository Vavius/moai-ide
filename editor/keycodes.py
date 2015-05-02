# converts Qt key codes to MOAI
import moaipy
from PySide.QtCore import Qt

keymap = {
	Qt.Key_Backspace 		:	moaipy.MOAI_KEY_BACKSPACE,
	Qt.Key_Tab 				:	moaipy.MOAI_KEY_TAB,
	Qt.Key_Return			:	moaipy.MOAI_KEY_RETURN,
	Qt.Key_Shift			:	moaipy.MOAI_KEY_SHIFT,
	Qt.Key_Control			:	moaipy.MOAI_KEY_CONTROL,
	Qt.Key_Alt				:	moaipy.MOAI_KEY_ALT,
	Qt.Key_Pause			:	moaipy.MOAI_KEY_PAUSE,
	Qt.Key_CapsLock			:	moaipy.MOAI_KEY_CAPS_LOCK,
	Qt.Key_Escape			:	moaipy.MOAI_KEY_ESCAPE,
	Qt.Key_Space			:	moaipy.MOAI_KEY_SPACE,
	Qt.Key_PageUp			:	moaipy.MOAI_KEY_PAGE_UP,
	Qt.Key_PageDown			:	moaipy.MOAI_KEY_PAGE_DOWN,
	Qt.Key_End				:	moaipy.MOAI_KEY_END,
	Qt.Key_Home				:	moaipy.MOAI_KEY_HOME,
	Qt.Key_Left				:	moaipy.MOAI_KEY_LEFT,
	Qt.Key_Up				:	moaipy.MOAI_KEY_UP,
	Qt.Key_Right			:	moaipy.MOAI_KEY_RIGHT,
	Qt.Key_Down				:	moaipy.MOAI_KEY_DOWN,
	Qt.Key_Print			:	moaipy.MOAI_KEY_PRINT_SCREEN,
	Qt.Key_Insert			:	moaipy.MOAI_KEY_INSERT,
	Qt.Key_Delete			:	moaipy.MOAI_KEY_DELETE,
	Qt.Key_0 				:	moaipy.MOAI_KEY_DIGIT_0,
	Qt.Key_1 				:	moaipy.MOAI_KEY_DIGIT_1,
	Qt.Key_2 				:	moaipy.MOAI_KEY_DIGIT_2,
	Qt.Key_3 				:	moaipy.MOAI_KEY_DIGIT_3,
	Qt.Key_4 				:	moaipy.MOAI_KEY_DIGIT_4,
	Qt.Key_5 				:	moaipy.MOAI_KEY_DIGIT_5,
	Qt.Key_6 				:	moaipy.MOAI_KEY_DIGIT_6,
	Qt.Key_7 				:	moaipy.MOAI_KEY_DIGIT_7,
	Qt.Key_8 				:	moaipy.MOAI_KEY_DIGIT_8,
	Qt.Key_9 				:	moaipy.MOAI_KEY_DIGIT_9,
	Qt.Key_A 				:	moaipy.MOAI_KEY_A,
	Qt.Key_B 				:	moaipy.MOAI_KEY_B,
	Qt.Key_C 				:	moaipy.MOAI_KEY_C,
	Qt.Key_D 				:	moaipy.MOAI_KEY_D,
	Qt.Key_E 				:	moaipy.MOAI_KEY_E,
	Qt.Key_F 				:	moaipy.MOAI_KEY_F,
	Qt.Key_G 				:	moaipy.MOAI_KEY_G,
	Qt.Key_H 				:	moaipy.MOAI_KEY_H,
	Qt.Key_I 				:	moaipy.MOAI_KEY_I,
	Qt.Key_J 				:	moaipy.MOAI_KEY_J,
	Qt.Key_K 				:	moaipy.MOAI_KEY_K,
	Qt.Key_L 				:	moaipy.MOAI_KEY_L,
	Qt.Key_M 				:	moaipy.MOAI_KEY_M,
	Qt.Key_N 				:	moaipy.MOAI_KEY_N,
	Qt.Key_O 				:	moaipy.MOAI_KEY_O,
	Qt.Key_P 				:	moaipy.MOAI_KEY_P,
	Qt.Key_Q 				:	moaipy.MOAI_KEY_Q,
	Qt.Key_R 				:	moaipy.MOAI_KEY_R,
	Qt.Key_S 				:	moaipy.MOAI_KEY_S,
	Qt.Key_T 				:	moaipy.MOAI_KEY_T,
	Qt.Key_U 				:	moaipy.MOAI_KEY_U,
	Qt.Key_V 				:	moaipy.MOAI_KEY_V,
	Qt.Key_W 				:	moaipy.MOAI_KEY_W,
	Qt.Key_X 				:	moaipy.MOAI_KEY_X,
	Qt.Key_Y 				:	moaipy.MOAI_KEY_Y,
	Qt.Key_Z 				:	moaipy.MOAI_KEY_Z,
	Qt.Key_Super_L 			:	moaipy.MOAI_KEY_GUI,
	Qt.Key_Super_R 			:	moaipy.MOAI_KEY_GUI,
	Qt.Key_ApplicationLeft	 :	moaipy.MOAI_KEY_APPLICATION,
	Qt.Key_ApplicationRight	:	moaipy.MOAI_KEY_APPLICATION,
	Qt.Key_F1				:	moaipy.MOAI_KEY_F1,
	Qt.Key_F2				:	moaipy.MOAI_KEY_F2,
	Qt.Key_F3				:	moaipy.MOAI_KEY_F3,
	Qt.Key_F4				:	moaipy.MOAI_KEY_F4,
	Qt.Key_F5				:	moaipy.MOAI_KEY_F5,
	Qt.Key_F6				:	moaipy.MOAI_KEY_F6,
	Qt.Key_F7				:	moaipy.MOAI_KEY_F7,
	Qt.Key_F8				:	moaipy.MOAI_KEY_F8,
	Qt.Key_F9				:	moaipy.MOAI_KEY_F9,
	Qt.Key_F10				:	moaipy.MOAI_KEY_F10,
	Qt.Key_F11				:	moaipy.MOAI_KEY_F11,
	Qt.Key_F12				:	moaipy.MOAI_KEY_F12,
	Qt.Key_NumLock			:	moaipy.MOAI_KEY_NUM_LOCK,
	Qt.Key_ScrollLock		:	moaipy.MOAI_KEY_SCROLL_LOCK,
	Qt.Key_Semicolon		:	moaipy.MOAI_KEY_OEM_1,
	Qt.Key_Plus				:	moaipy.MOAI_KEY_OEM_PLUS,
	Qt.Key_Comma			:	moaipy.MOAI_KEY_OEM_COMMA,
	Qt.Key_Minus			:	moaipy.MOAI_KEY_OEM_MINUS,
	Qt.Key_Period			:	moaipy.MOAI_KEY_OEM_PERIOD,
	Qt.Key_Slash			:	moaipy.MOAI_KEY_OEM_2,
	Qt.Key_QuoteLeft		:	moaipy.MOAI_KEY_OEM_3,
	Qt.Key_BracketLeft		:	moaipy.MOAI_KEY_OEM_4,
	Qt.Key_Backslash		:	moaipy.MOAI_KEY_OEM_5,
	Qt.Key_BracketRight		:	moaipy.MOAI_KEY_OEM_6,
	Qt.Key_QuoteDbl			:	moaipy.MOAI_KEY_OEM_7,
}


# no num pad support yet

# moaipy.MOAI_KEY_NUM_0
# moaipy.MOAI_KEY_NUM_1
# moaipy.MOAI_KEY_NUM_2
# moaipy.MOAI_KEY_NUM_3
# moaipy.MOAI_KEY_NUM_4
# moaipy.MOAI_KEY_NUM_5
# moaipy.MOAI_KEY_NUM_6
# moaipy.MOAI_KEY_NUM_7
# moaipy.MOAI_KEY_NUM_8
# moaipy.MOAI_KEY_NUM_9
# moaipy.MOAI_KEY_NUM_MULTIPLY
# moaipy.MOAI_KEY_NUM_PLUS
# moaipy.MOAI_KEY_NUM_MINUS
# moaipy.MOAI_KEY_NUM_DECIMAL
# moaipy.MOAI_KEY_NUM_DIVIDE



def getMoaiKeyCode(code):
	try:
		return keymap[code]
	except KeyError:
		return moaipy.MOAI_KEY_INVALID
