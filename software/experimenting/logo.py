# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception


import string
__version__ = string.split('$Revision: 1.1.1.1 $')[1]
__date__ = string.join(string.split('$Date: 2007/02/15 19:25:13 $')[1:3], ' ')
__author__ = 'John Popplewell <john@johnnypops.demon.co.uk>'
from OpenGL.GL import *

def define_logo():
	n = glNormal3f
	v = glVertex3f
	glBegin(GL_TRIANGLES)
	n(0,0,-1)
	v(64.375,5.5,-1)
	n(0,0,-1)
	
	glEnd()
