import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import numpy as np



def init():
    pygame.init()
    display = (1000, 1000)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-1.0, 1.0, -1.0, 1.0)


vertices= (
    
    (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1)
    
    )



edges = (   
         
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7) 
    
)

# vector array
v = []

for eg in edges:
    p_init = np.array(vertices[eg[0]])
    p_final = np.array(vertices[eg[1]])
    v.append((p_final-p_init))
        



def Cube():
    t=1 # the line remains 10% to connect.
    glBegin(GL_LINES)
    for i in range(len(edges)):
        p0 = np.array(vertices[edges[i][0]])
        p = p0 +  t * v[i]
        glVertex3fv(p0)
        glVertex3fv(p)
    glEnd()
    
    
   
def rotationMatrix(degree):
    radian = degree * np.pi / 180.0
    mat = np.array([
        [np.cos(radian), -np.sin(radian)],
        [np.sin(radian), np.cos(radian)],
    ])

    return mat

matrix = rotationMatrix(120)



def main():
    
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -5)
    
    while True:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        glRotatef(0, 0, 0, 0)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        glColor3f(1,1,1)
        pygame.display.flip()
        pygame.time.wait(10)        
        pygame.display.flip()
        pygame.time.wait(10)
        glRotatef(1, 3, 1, 1)


main()
