#!

if __name__ == '__build__':
    raise Exception

import string

from OpenGL.GL import * #@UnusedWildImport
from OpenGL.GLUT import * #@UnusedWildImport
from OpenGL.GLU import *  #@UnusedWildImport
import numpy as np
import glFreeType #@UnusedImport
from Image import * #@UnusedWildImport


ESCAPE = '\033'

RETURN = '\015'

blockSeperator = 0.01
xLowerLimit = 0.0
xHigherLimit = 4.4
yLowerLimit = 0.0
yHigherLimit = 4.4
zLowerLimit = -4.4
zHigherLimit = 0.0

# Number of the glut window.
window = 0

rquadZ = 0.0
rquadX = 0.0

axisSelect = 0

cubeTmpSelect = 0
cubeSelect = 0

move = 0.1

cubeLoctions = np.array([[ 0.0,  0.0,  0.0],
       [ 2.0 + blockSeperator,  0.0,  0.0],
       [ 4.0 + 2*blockSeperator,  0.0,  0.0],
       [ 0.0 ,  0.0 , -2.0 - blockSeperator],
       [ 2.0 + blockSeperator,  0.0, -2.0 - blockSeperator],
       [ 4.0 + 2*blockSeperator,  0.0, -2.0 - blockSeperator],
       [ 0.0,  0.0 , -4.0 - 2*blockSeperator],
       [ 2.0 + blockSeperator,  0.0 , -4.0 - 2*blockSeperator],
       [ 4.0 + 2*blockSeperator,  0.0 , -4.0 - 2*blockSeperator],
       [ 0.0,  2.0 + blockSeperator,  0.0 ],
       [ 2.0 + blockSeperator,  2.0 + blockSeperator,  0.0 ],
       [ 4.0 + 2*blockSeperator,  2.0 + blockSeperator,  0.0 ],
       [ 0.0,  2.0 + blockSeperator, -2.0 - blockSeperator],
       [ 2.0 + blockSeperator,  2.0 + blockSeperator, -2.0 - blockSeperator],
       [ 4.0 + 2*blockSeperator,  2.0 + blockSeperator, -2.0 - blockSeperator],
       [ 0.0,  2.0 + blockSeperator, -4.0 - 2*blockSeperator],
       [ 2.0 + blockSeperator,  2.0 + blockSeperator, -4.0 - 2*blockSeperator],
       [ 4.0 + 2*blockSeperator,  2.0 + blockSeperator, -4.0 - 2*blockSeperator],
       [ 0.0,  4.0 + 2*blockSeperator,  0.0 ],
       [ 2.0 + blockSeperator,  4.0 + 2*blockSeperator,  0.0 ],
       [ 4.0 + 2*blockSeperator,  4.0 + 2*blockSeperator,  0.0 ],
       [ 0.0,  4.0 + 2*blockSeperator, -2.0 - blockSeperator],
       [ 2.0 + blockSeperator,  4.0 + 2*blockSeperator, -2.0 - blockSeperator],
       [ 4.0 + 2*blockSeperator,  4.0 + 2*blockSeperator, -2.0 - blockSeperator],
       [ 0.0,  4.0 + 2*blockSeperator, -4.0 - 2*blockSeperator],
       [ 2.0 + blockSeperator,  4.0 + 2*blockSeperator, -4.0 - 2*blockSeperator],
       [ 0.0,  0.0 ,  0.0 ]])


def LoadTextures():
    global textures
    textures = glGenTextures(26)

    for x in range(0, 26):
        image = open("./res/"+str(x+1)+".bmp")

        ix = image.size[0]
        iy = image.size[1]
        image = image.tostring("raw", "RGBX", 0, -1)

        # Create MipMapped Texture
        glBindTexture(GL_TEXTURE_2D, int(textures[x]))
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MAG_FILTER,GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D,GL_TEXTURE_MIN_FILTER,GL_LINEAR_MIPMAP_NEAREST)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3, ix, iy, GL_RGBA, GL_UNSIGNED_BYTE, image)

# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):
    global quadratic
    LoadTextures()

    quadratic = gluNewQuadric()
    gluQuadricNormals(quadratic, GLU_SMOOTH)        # Create Smooth Normals (NEW)
    gluQuadricTexture(quadratic, GL_TRUE)            # Create Texture Coords (NEW)
    glEnable(GL_TEXTURE_2D)
    # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


    return True


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

# The main drawing function.
def DrawGLScene():
    global rquadZ, rquadX, our_font
    global textures, quadratic
    global cubeLoctions

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    # Reset The View

    currentX =  0.0
    currentY = 0.0
    currentZ =  0.0
    glTranslatef(-2.0,-2.0,-15.0);
    glTranslatef(3.2,3.2,-3.2);
    glRotatef(rquadX,0.0,1.0,0.0);        # Rotate The Cube On X, Y & Z
    glRotatef(rquadZ,1.0,0.0,0.0);
    glTranslatef(-3.2,-3.2,3.2);


    for x in range(0, 26):
        # Move Right And Into The Screen

        glBindTexture(GL_TEXTURE_2D, int(textures[x]))

        glBegin(GL_QUADS)                # Start Drawing The Cube

        glColor3f(0.0,1.0,0.0);
        # Front Face (note that the texture's corners have to match the quad's corners)
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)    # Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)    # Top Left Of The Texture and Quad

        glColor3f(0.0,1.0,1.0);
        # Back Face
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)    # Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    # Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    # Top Left Of The Texture and Quad
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)    # Bottom Left Of The Texture and Quad

        glColor3f(0.5,1.0,1.0);
        # Top Face
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    # Top Left Of The Texture and Quad
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)    # Bottom Left Of The Texture and Quad
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)    # Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    # Top Right Of The Texture and Quad

        glColor3f(0.5,0.5,0.5);
        # Bottom Face
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)    # Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)    # Top Left Of The Texture and Quad
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad

        glColor3f(1.0,0.5,0.25);
        # Right face
        glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)    # Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    # Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)    # Top Left Of The Texture and Quad
        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad

        glColor3f(0.25,.75,0.25);
        # Left Face
        glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)    # Bottom Left Of The Texture and Quad
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)    # Top Right Of The Texture and Quad
        glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    # Top Left Of The Texture and Quad

        glEnd();                # Done Drawing The Cube
        currentX = cubeLoctions[x+1][0] - cubeLoctions[x][0]
        currentY = cubeLoctions[x+1][1] - cubeLoctions[x][1]
        currentZ = cubeLoctions[x+1][2] - cubeLoctions[x][2]
        glTranslatef(currentX,currentY,currentZ);

    glutSwapBuffers()

def moveOtherCubes(cubeNumber,deltaX,deltaY,deltaZ,arrayToExclude):
    global cubeLoctions
    for x in range(0, 26):
        print str(abs(cubeLoctions[x][0]-cubeLoctions[cubeNumber][0]))
        print str(abs(cubeLoctions[x][1]-cubeLoctions[cubeNumber][1]))
        print str(abs(cubeLoctions[x][2]-cubeLoctions[cubeNumber][2]))
        if ((abs(cubeLoctions[x][0]-(cubeLoctions[cubeNumber][0]+deltaX))<2.0) & (abs(cubeLoctions[x][1]-(cubeLoctions[cubeNumber][1]+deltaY))<2.0) & (abs(cubeLoctions[x][2]-(cubeLoctions[cubeNumber][2]+deltaZ))<2.0)&(not np.in1d([x],arrayToExclude))):
            return moveCube(x,deltaX,deltaY,deltaZ,np.concatenate((arrayToExclude,np.array([x])),axis=0))
    return -1

def moveCube(cubeNumber,deltaX,deltaY,deltaZ,arrayToExclude):
    global cubeLoctions,lowerLimit,higherLimit
    print "moveCube "+ str(deltaX)+" "+str(deltaY)+" "+str(deltaZ)+" "+str(cubeNumber)
    print "cubeLoctions "+str(cubeLoctions[cubeNumber][0])+" "+str(cubeLoctions[cubeNumber][1])+" "+str(cubeLoctions[cubeNumber][2])+" "
    if ((xLowerLimit<=(cubeLoctions[cubeNumber][0]+deltaX)<=xHigherLimit)&(yLowerLimit<=(cubeLoctions[cubeNumber][1]+deltaY)<=yHigherLimit)&(zLowerLimit<=(cubeLoctions[cubeNumber][2]+deltaZ)<=zHigherLimit)):
        if (moveOtherCubes(cubeNumber,deltaX,deltaY,deltaZ,arrayToExclude)):
            cubeLoctions[cubeNumber][0] = cubeLoctions[cubeNumber][0] + deltaX
            cubeLoctions[cubeNumber][1] = cubeLoctions[cubeNumber][1] + deltaY
            cubeLoctions[cubeNumber][2] = cubeLoctions[cubeNumber][2] + deltaZ
            return 1
        else:
            return 0
    else:
        return 0


def buildTempSelect(select):
    global cubeTmpSelect
    if (cubeTmpSelect==0):
            cubeTmpSelect = select
    else:
            cubeTmpSelect=cubeTmpSelect*10 + select

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(key, x, y):
    selected = 0
    global rquadX,rquadZ,cubeTmpSelect,cubeSelect,axisSelect,move

    key = string.upper(key)

    if key == ESCAPE:
            sys.exit()
    elif key == 'J':
            rquadX = rquadX - 1.15
    elif key == 'L':
            rquadX = rquadX + 1.15
    elif key == 'K':
            rquadZ = rquadZ - 1.15
    elif key == 'I':
            rquadZ = rquadZ + 1.15
    elif key == '1':
            selected = 1
            print "Pressed 1"
            buildTempSelect(selected)
    elif key == '2':
            selected = 2
            print "Pressed 2"
            buildTempSelect(selected)
    elif key == '3':
            selected = 3
            print "Pressed 3"
            buildTempSelect(selected)
    elif key == '4':
            selected = 4
            print "Pressed 4"
            buildTempSelect(selected)
    elif key == '5':
            selected = 5
            print "Pressed 5"
            buildTempSelect(selected)
    elif key == '6':
            selected = 6
            print "Pressed 6"
            buildTempSelect(selected)
    elif key == '7':
            selected = 7
            print "Pressed 7"
            buildTempSelect(selected)
    elif key == '8':
            selected = 8
            print "Pressed 8"
            buildTempSelect(selected)
    elif key == '9':
            selected = 9
            print "Pressed 9"
            buildTempSelect(selected)
    elif key == RETURN:
            print "Pressed RETURN"
            cubeSelect = cubeTmpSelect -1
            cubeTmpSelect = 0
    elif key == 'A':
            print "Pressed A and Axis is "+ str(axisSelect)+" and cube number " + str(cubeSelect)
            if (axisSelect == 0):
                    if moveCube(cubeSelect,move,0.0,0.0,np.array([cubeSelect])):
                        print "Moved"
                    else:
                        print "COULD NOT MOVE"
            elif (axisSelect == 1):
                    if moveCube(cubeSelect,0.0,move,0.0,np.array([cubeSelect])):
                        print "Moved"
                    else:
                        print "COULD NOT MOVE"
            elif (axisSelect == 2):
                    if moveCube(cubeSelect,0.0,0.0,move,np.array([cubeSelect])):
                        print "Moved"
                    else:
                        print "COULD NOT MOVE"
    elif key == 'D':
            print "Pressed D and Axis is "+ str(axisSelect)+" and cube number " + str(cubeSelect)
            if (axisSelect == 0):
                    if moveCube(cubeSelect,-move,0.0,0.0,np.array([cubeSelect])):
                        print "Moved"
                    else:
                        print "COULD NOT MOVE"
            elif (axisSelect == 1):
                    if moveCube(cubeSelect,0.0,-move,0.0,np.array([cubeSelect])):
                        print "Moved"
                    else:
                        print "COULD NOT MOVE"
            elif (axisSelect == 2):
                    if moveCube(cubeSelect,0.0,0.0,-move,np.array([cubeSelect])):
                        print "Moved"
                    else:
                        print "COULD NOT MOVE"
    elif key == 'X':
            print "Selected X Axis"
            axisSelect = 0
    elif key == 'Y':
            print "Selected Y Axis"
            axisSelect = 1
    elif key == 'Z':
            print "Selected Z Axis"
            axisSelect = 2



def main():
    global window
    glutInit(sys.argv)


    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

    glutInitWindowSize(480, 480)

    glutInitWindowPosition(0, 0)

    window = glutCreateWindow("Blocks")

    glutDisplayFunc(DrawGLScene)


    glutIdleFunc(DrawGLScene)

    glutReshapeFunc(ReSizeGLScene)

    glutKeyboardFunc(keyPressed)

    InitGL(640, 480)

    glutMainLoop()

print "Hit ESC key to quit."
main()
