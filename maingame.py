import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

def init():
    pygame.init()
    display = (1000, 500)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    gluOrtho2D(-10.0, 10.0, -10.0, 10.0)
vertices = (
    (-10, -10, -10),  # 0
    (-10, -10, 10),  # 1
    (-6, -10, -10),  # 2
    (-6, -10, 10),  # 3
    (6, -10, -10),  # 4
    (6, -10, 10),  # 5
    (10, -10, 10),  # 6
    (10, -10, 10)  # 7
)
roadEdges = (
    (0, 1),
    (0,2),
    (1,3),
    (3, 2),
    (2, 4),
    (4, 5),
    (5, 3),
    (4, 6),
    (6, 7),
    (6, 7),
    (7, 5),
    
)


def road():
    glPointSize(10)

    glBegin(GL_LINES)   

    for edge in roadEdges:
        for vertex in edge:
             glVertex3fv(vertices[vertex])
    glEnd()


def main():
    init()
    display = (800, 700)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #glRotate(0, 0, 0, 0)
        #glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        road()
        pygame.display.flip()
        pygame.time.wait(30)


main()
