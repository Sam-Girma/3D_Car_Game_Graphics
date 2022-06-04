from turtle import dot
import numpy as np
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
def rotationMatrix(degree):
    radian = degree * np.pi / 180.0
    mat = np.array([
        [np.cos(radian), -np.sin(radian)],
        [np.sin(radian), np.cos(radian)],
    ])

    return mat
def init():
    pygame.init()
    display = (500, 500)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(-2.0, 2.0, -2.0, 2.0)
def xyplane():
    glColor3f(1.0, 0.0, 1.0)
    glPointSize(2)
    glBegin(GL_LINES)
    glVertex2f(-20.0, 0.0)
    glVertex2f(20.0, 0.0)
    glVertex2f(0.0, 8.0)
    glVertex2f(0.0, -8.0)
    glEnd()
    glFlush()

def draw(po1, po2, x, y, t):
    mat=rotationMatrix(60)
    glBegin(GL_LINE_STRIP)
    V = np.array([x, y])
    Po = [po1, po2]
    P = Po + (t * V)
    
    P1=np.dot(P ,mat)
    glVertex2f(po1, po2)
    glVertex2f(P1[0], P1[1])
    glEnd()
def cube():
    # glRotatef(1,0,1,1)
    glClear(GL_COLOR_BUFFER_BIT)
    #for the quadrants
    draw(0, 0, 1,1, 0.5)
    draw(0, 0, -1,1, 0.5)
    draw(-0.5, 0.5, 0, -1, 0.5)
    draw(0.5,0.5 ,0, -1, 0.5)
    draw(0,0 ,0, -1, 0.5)
    draw(0,-0.5 ,1, 1, 0.5)
    draw(0,-0.5 ,-1, 1, 0.5)
    draw(-0.5,0.5 ,1, 1, 0.5)
    draw(0.5,0.5 ,-1, 1, 0.5)
    draw(0.5,0.5 ,-1, 1, 0.5)
    
    draw(-0.5,0 ,1, 1, 0.5)
    draw(0.5,0 ,-1, 1, 0.5)
    draw(0,0.5 ,0, 1, 0.5)

    
    

    
    
def main():
    init()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        xyplane()
        cube()
        pygame.display.flip()
        pygame.time.wait(10)
        
main()
