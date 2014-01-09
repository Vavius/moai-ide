import sys
from PySide.QtGui import *
from PySide.QtOpenGL import *
from OpenGL.GL import *
from OpenGL.GLU import *

class GLWidget(QGLWidget):
    def __init__(self, *args, **kwargs):
        QGLWidget.__init__(self,  *args, **kwargs)

    def initializeGL(self):
        glShadeModel(GL_SMOOTH)
        glEnable(GL_DEPTH_TEST)
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClearDepth(1.0)

    def resizeGL(self, w, h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, w, h)
        gluPerspective(45.0, w / h, 1, 1000)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glTranslatef(self.x(), self.y(), -6.0)
        glBegin(GL_TRIANGLES)
        glColor3f(1.0, 0.0, 0.0)           
        glVertex3f(0.0, 1.0, 0.0)        
        glColor3f(0.0, 0.0, 1.0)           
        glVertex3f(-1.0, -1.0, 0.0)        
        glColor3f(0.0, 1.0, 0.0)           
        glVertex3f(1.0, -1.0, 1.0)        
        glEnd()

class Window(QWidget):
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.scroll = QScrollArea(self)
        self.glWidget = GLWidget(self.scroll)
        self.glWidget.resize(600, 400)
        self.scroll.setWidget(self.glWidget)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.scroll)

        self.setLayout(self.layout)
        self.resize(400, 300)
        self.show()

app = QApplication(sys.argv)
win = Window()
sys.exit(app.exec_())