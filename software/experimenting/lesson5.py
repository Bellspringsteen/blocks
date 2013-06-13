#!

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception

import string
__version__ = string.split('$Revision: 1.1.1.1 $')[1]
__date__ = string.join(string.split('$Date: 2007/02/15 19:25:21 $')[1:3], ' ')
__author__ = 'Tarn Weisner Burton <twburton@users.sourceforge.net>'

#
# Ported to PyOpenGL 2.0 by Tarn Weisner Burton 10May2001
#
# This code was created by Richard Campbell '99 (ported to Python/PyOpenGL by John Ferguson and Tony Colston 2000)
# To be honst I stole all of John Ferguson's code and just added the changed stuff for lesson 5. So he did most
# of the hard work.
#
# The port was based on the PyOpenGL tutorial module: dots.py  
#
# If you've found this code useful, please let me know (email John Ferguson at hakuin@voicenet.com).
# or Tony Colston (tonetheman@hotmail.com)
#
# See original source and C based tutorial at http:#nehe.gamedev.net
#
# Note:
# -----
# This code is not a good example of Python and using OO techniques.  It is a simple and direct
# exposition of how to use the Open GL API in Python via the PyOpenGL package.  It also uses GLUT,
# which in my opinion is a high quality library in that it makes my work simpler.  Due to using
# these APIs, this code is more like a C program using function based programming (which Python
# is in fact based upon, note the use of closures and lambda) than a "good" OO program.
#
# To run this code get and install OpenGL, GLUT, PyOpenGL (see http:#www.python.org), and NumPy.
# Installing PyNumeric means having a C compiler that is configured properly, or so I found.  For 
# Win32 this assumes VC++, I poked through the setup.py for Numeric, and chased through disutils code
# and noticed what seemed to be hard coded preferences for VC++ in the case of a Win32 OS.  However,
# I am new to Python and know little about disutils, so I may just be not using it right.
#
# NumPy is not a hard requirement, as I am led to believe (based on skimming PyOpenGL sources) that
# PyOpenGL could run without it. However preformance may be impacted since NumPy provides an efficient
# multi-dimensional array type and a linear algebra library.
#
# BTW, since this is Python make sure you use tabs or spaces to indent, I had numerous problems since I 
# was using editors that were not sensitive to Python.
#
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import sys
import glFreeType 
# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# Rotation angle for the triangle. 
rquadZ = 0.0

# Rotation angle for the quadrilateral.
rquadX = 0.0
our_font = None
cubeLoctions = np.array([[ 0. ,  0. ,  0. ],
       [ 2.2,  0. ,  0. ],
       [ 4.4,  0. ,  0. ],
       [ 0. ,  0. , -2.2],
       [ 2.2,  0. , -2.2],
       [ 4.4,  0. , -2.2],
       [ 0. ,  0. , -4.4],
       [ 2.2,  0. , -4.4],
       [ 4.4,  0. , -4.4],
       [ 0. ,  2.2,  0. ],
       [ 2.2,  2.2,  0. ],
       [ 4.4,  2.2,  0. ],
       [ 0. ,  2.2, -2.2],
       [ 2.2,  2.2, -2.2],
       [ 4.4,  2.2, -2.2],
       [ 0. ,  2.2, -4.4],
       [ 2.2,  2.2, -4.4],
       [ 4.4,  2.2, -4.4],
       [ 0. ,  4.4,  0. ],
       [ 2.2,  4.4,  0. ],
       [ 4.4,  4.4,  0. ],
       [ 0. ,  4.4, -2.2],
       [ 2.2,  4.4, -2.2],
       [ 4.4,  4.4, -2.2],
       [ 0. ,  4.4, -4.4],
       [ 2.2,  4.4, -4.4],
       [ 0. ,  0. ,  0. ]])

def drawText( value, x,y,  windowHeight, windowWidth, step = 18 ):
    """Draw the given text at given 2D position in window
    """
    glMatrixMode(GL_PROJECTION);
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPushMatrix()
    matrix = glGetDouble( GL_PROJECTION_MATRIX )
    
    glLoadIdentity();
    glOrtho(0.0, windowHeight or 32, 0.0, windowWidth or 32, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW);
    glPushMatrix();
    glLoadIdentity();
    glRasterPos2i(x, y);
    lines = 0
##	import pdb
##	pdb.set_trace()
    for character in value:
        if character == '\n':
            glRasterPos2i(x, y-(lines*18))
        else:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(character));
    glPopMatrix();
    glMatrixMode(GL_PROJECTION);
    # For some reason the GL_PROJECTION_MATRIX is overflowing with a single push!
    # glPopMatrix();
    glLoadMatrixd( matrix ) # should have un-decorated alias for this...
    
    glMatrixMode(GL_MODELVIEW);
    
# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):
    global our_font
    # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
    our_font = glFreeType.font_data ("Test.ttf", 16)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
	    Height = 1

    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def glut_print( x,  y,  font,  text, r,  g , b , a):

    blending = False 
    if glIsEnabled(GL_BLEND) :
        blending = True

    #glEnable(GL_BLEND)
    glColor3f(1,1,1)
    glRasterPos2f(x,y)
    for ch in text :
        glutBitmapCharacter( font , ctypes.c_int( ord(ch) ) )


    if not blending :
        glDisable(GL_BLEND)
# The main drawing function. 
def DrawGLScene():
	global rquadZ, rquadX, our_font
	

        currentX =  0.0
        currentY = 0.0
        currentZ =  0.0
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);	# Clear The Screen And The Depth Buffer	
        glLoadIdentity();
        glTranslatef(-2.0,-2.0,-15.0);
        glTranslatef(3.2,3.2,-3.2);
        glRotatef(rquadX,0.0,1.0,0.0);		# Rotate The Cube On X, Y & Z
        glRotatef(rquadZ,1.0,0.0,0.0);
        glTranslatef(-3.2,-3.2,3.2);

	
##	glColor3ub (0xff, 0, 0)
##
##	glPushMatrix ()
##	glLoadIdentity ()
##	glRotatef (cnt1, 0, 0, 1)
##	glScalef (1, 0.8 + 0.3* cos (cnt1/5), 1)
##	glTranslatef (-180, 0, 0)
##	our_font.glPrint (320, 240, "Active FreeType Text - %7.2f" % (cnt1))
##	glPopMatrix ()
	
        for x in range(0, 26):
                # Move Right And Into The Screen
 
                glBegin(GL_QUADS);			# Start Drawing The Cube


                glColor3f(0.0,1.0,0.0);			# Set The Color To Blue
                glVertex3f( 1.0, 1.0,-1.0);		# Top Right Of The Quad (Top)
                glVertex3f(-1.0, 1.0,-1.0);		# Top Left Of The Quad (Top)
                glVertex3f(-1.0, 1.0, 1.0);		# Bottom Left Of The Quad (Top)
                glVertex3f( 1.0, 1.0, 1.0);		# Bottom Right Of The Quad (Top)

                glColor3f(1.0,0.5,0.0);			# Set The Color To Orange
                glVertex3f( 1.0,-1.0, 1.0);		# Top Right Of The Quad (Bottom)
                glVertex3f(-1.0,-1.0, 1.0);		# Top Left Of The Quad (Bottom)
                glVertex3f(-1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Bottom)
                glVertex3f( 1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Bottom)

                glColor3f(1.0,0.0,0.0);			# Set The Color To Red
                glVertex3f( 1.0, 1.0, 1.0);		# Top Right Of The Quad (Front)
                glVertex3f(-1.0, 1.0, 1.0);		# Top Left Of The Quad (Front)
                glVertex3f(-1.0,-1.0, 1.0);		# Bottom Left Of The Quad (Front)
                glVertex3f( 1.0,-1.0, 1.0);		# Bottom Right Of The Quad (Front)

                glColor3f(1.0,1.0,0.0);			# Set The Color To Yellow
                glVertex3f( 1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Back)
                glVertex3f(-1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Back)
                glVertex3f(-1.0, 1.0,-1.0);		# Top Right Of The Quad (Back)
                glVertex3f( 1.0, 1.0,-1.0);		# Top Left Of The Quad (Back)

                glColor3f(0.0,0.0,1.0);			# Set The Color To Blue
                glVertex3f(-1.0, 1.0, 1.0);		# Top Right Of The Quad (Left)
                glVertex3f(-1.0, 1.0,-1.0);		# Top Left Of The Quad (Left)
                glVertex3f(-1.0,-1.0,-1.0);		# Bottom Left Of The Quad (Left)
                glVertex3f(-1.0,-1.0, 1.0);		# Bottom Right Of The Quad (Left)

                glColor3f(1.0,0.0,1.0);			# Set The Color To Violet
                glVertex3f( 1.0, 1.0,-1.0);		# Top Right Of The Quad (Right)
                glVertex3f( 1.0, 1.0, 1.0);		# Top Left Of The Quad (Right)
                glVertex3f( 1.0,-1.0, 1.0);		# Bottom Left Of The Quad (Right)
                glVertex3f( 1.0,-1.0,-1.0);		# Bottom Right Of The Quad (Right)
                glEnd();				# Done Drawing The Quad

                currentX = cubeLoctions[x+1][0] - cubeLoctions[x][0]
                currentY = cubeLoctions[x+1][1] - cubeLoctions[x][1]
                currentZ = cubeLoctions[x+1][2] - cubeLoctions[x][2]
        	glTranslatef(currentX,currentY,currentZ);
        
                        
                
                
 
	# What values to use?  Well, if you have a FAST machine and a FAST 3D Card, then
	# large values make an unpleasant display with flickering and tearing.  I found that
	# smaller values work better, but this was based on my experience.
	#rquadX = rquadX - 0.15                 # Decrease The Rotation Variable For The Quad


	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
##def keyPressed(*args):
##	# If escape is pressed, kill everything.
##    if args[0] == ESCAPE:
##	    sys.exit()

	    # The function called whenever a key is pressed
def keyPressed(key, x, y):
        global rquadX,rquadZ
        # If escape is pressed, kill everything.
        key = string.upper(key)
        if key == ESCAPE:
                our_font.release ()
                sys.exit()
        elif key == 'J':
                rquadX = rquadX - 1.15
        elif key == 'L': #  switch the texture
                rquadX = rquadX + 1.15
        elif key == 'K':
                rquadZ = rquadZ - 1.15
        elif key == 'I': #  switch the texture
                rquadZ = rquadZ + 1.15

def main():
	global window
	glutInit(sys.argv)

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(480, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("Jeff Molofee's GL Code Tutorial ... NeHe '99")

   	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	glutDisplayFunc(DrawGLScene)
	
	# Uncomment this line to get full screen.
	# glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)

	# Initialize our window. 
	InitGL(640, 480)

	# Start Event Processing Engine	
	glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
print "Hit ESC key to quit."
main()
    	
