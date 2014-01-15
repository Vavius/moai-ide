from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

setup(
    cmdclass = {'build_ext': build_ext},
    ext_modules = [
        Extension("moaipy", ["moaipy.pyx", "lock.pxi"], 
            language="c++",
            extra_objects=[
                'libmoai-box2d.a',
                'libmoai-chipmunk.a',
                'libmoai-core.a',
                'libmoai-luaext.a',
                'libmoai-sim.a',
                'libmoai-test.a',
                'libmoai-util.a',
                'libthird-party.a',
                'libzlcore.a',
                'libluasocket.a',
            ],

            extra_link_args=[
            '-framework', 'OpenGL',
            '-framework', 'GLUT',
            '-framework', 'CoreServices',
            '-framework', 'ApplicationServices',
            '-framework', 'AudioToolbox',
            '-framework', 'AudioUnit',
            '-framework', 'CoreAudio',
            '-framework', 'CoreGraphics',
            '-framework', 'CoreLocation',
            '-framework', 'Foundation',
            '-framework', 'GameKit',
            '-framework', 'QuartzCore',
            '-framework', 'StoreKit',
            '-framework', 'SystemConfiguration',
            ],

            include_dirs=[
            '/Users/vavius/moai/moai-new/src/',
            '/Users/vavius/moai/moai-new/3rdparty/lua-5.1.3src/'
            ])
    ]
)