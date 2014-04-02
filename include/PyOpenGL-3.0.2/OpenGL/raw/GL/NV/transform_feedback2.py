'''Autogenerated by get_gl_extensions script, do not edit!'''
from OpenGL import platform as _p, constants as _cs, arrays
from OpenGL.GL import glget
import ctypes
EXTENSION_NAME = 'GL_NV_transform_feedback2'
def _f( function ):
    return _p.createFunction( function,_p.GL,'GL_NV_transform_feedback2',False)
_p.unpack_constants( """GL_TRANSFORM_FEEDBACK_NV 0x8E22
GL_TRANSFORM_FEEDBACK_BUFFER_PAUSED_NV 0x8E23
GL_TRANSFORM_FEEDBACK_BUFFER_ACTIVE_NV 0x8E24
GL_TRANSFORM_FEEDBACK_BINDING_NV 0x8E25""", globals())
glget.addGLGetConstant( GL_TRANSFORM_FEEDBACK_BUFFER_PAUSED_NV, (1,) )
glget.addGLGetConstant( GL_TRANSFORM_FEEDBACK_BUFFER_ACTIVE_NV, (1,) )
glget.addGLGetConstant( GL_TRANSFORM_FEEDBACK_BINDING_NV, (1,) )
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint)
def glBindTransformFeedbackNV( target,id ):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glDeleteTransformFeedbacksNV( n,ids ):pass
@_f
@_p.types(None,_cs.GLsizei,arrays.GLuintArray)
def glGenTransformFeedbacksNV( n,ids ):pass
@_f
@_p.types(_cs.GLboolean,_cs.GLuint)
def glIsTransformFeedbackNV( id ):pass
@_f
@_p.types(None,)
def glPauseTransformFeedbackNV(  ):pass
@_f
@_p.types(None,)
def glResumeTransformFeedbackNV(  ):pass
@_f
@_p.types(None,_cs.GLenum,_cs.GLuint)
def glDrawTransformFeedbackNV( mode,id ):pass


def glInitTransformFeedback2NV():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( EXTENSION_NAME )