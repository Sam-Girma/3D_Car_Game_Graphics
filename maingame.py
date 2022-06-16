import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader

class MainGame:

    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((1000, 800), pg.OPENGL|pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(1.0, 1.0, 0.5, 1)
        

        self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
        glUseProgram(self.shader)
        

        self.road = Mesh("objects/road.obj")
        

        

        
        self.mainLoop()
    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader
    def mainLoop(self):

        while(True):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    
                    self.quit()
                    break
            self.handleKeys()
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)
            glBindVertexArray(self.road.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.road.vertex_count)

            # # glBindVertexArray(self.car.vao)
            # # glDrawArrays(GL_TRIANGLES, 0, self.car.vertex_count)

            # glBindVertexArray(self.environment.vao)
            # glDrawArrays(GL_TRIANGLES, 0, self.environment.vertex_count)

            # glBindVertexArray(self.cloud.vao)
            # glDrawArrays(GL_TRIANGLES, 0, self.cloud.vertex_count)
            glClear(GL_COLOR_BUFFER_BIT)
            pg.display.flip()
            
            self.clock.tick(60)
    def handleKeys(self):
        pass
        # keys = pg.key.get_pressed()

        # #left, right, up, down
        # if keys[pg.K_LEFT]:
        #     pass
        # elif keys[pg.K_RIGHT]:
        #     pass
        # elif keys[pg.K_UP]:
        #     pass
        # elif keys[pg.K_DOWN]:
        #     pass
    def quit(self):
        self.car.destroy()
        self.cloud.destroy()
        self.environment.destroy()
        self.road.destroy()
        pg.quit()

class Mesh:
    def __init__(self, filename):
       
        self.vertices = self.loadMesh(filename)
        self.vertex_count = len(self.vertices)//8
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        #position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        #texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
    def loadMesh(self, filename):

        #raw, unassembled data
        v = []
        vt = []
        vn = []
        
        #final, assembled and packed result
        vertices = []

        #open the obj file and read the data
        with open(filename,'r') as f:
            line = f.readline()
            while line:
                firstSpace = line.find(" ")
                flag = line[0:firstSpace]
                if flag=="v":
                    #vertex
                    line = line.replace("v ","")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    v.append(l)
                elif flag=="vt":
                    #texture coordinate
                    line = line.replace("vt ","")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vt.append(l)
                elif flag=="vn":
                    #normal
                    line = line.replace("vn ","")
                    line = line.split(" ")
                    l = [float(x) for x in line]
                    vn.append(l)
                elif flag=="f":
                    #face, three or more vertices in v/vt/vn form
                    line = line.replace("f ","")
                    line = line.replace("\n","")
                    #get the individual vertices for each line
                    line = line.split(" ")
                    faceVertices = []
                    faceTextures = []
                    faceNormals = []
                    for vertex in line:
                        #break out into [v,vt,vn],
                        #correct for 0 based indexing.
                        l = vertex.split("/")
                        position = int(l[0]) - 1
                        faceVertices.append(v[position])
                        texture = int(l[1]) - 1 
                        faceTextures.append(vt[texture])
                        normal = int(l[2]) - 1
                        faceNormals.append(vn[normal])
                    # obj file uses triangle fan format for each face individually.
                    # unpack each face
                    triangles_in_face = len(line) - 2

                    vertex_order = []
                    """
                        eg. 0,1,2,3 unpacks to vertices: [0,1,2,0,2,3]
                    """
                    for i in range(triangles_in_face):
                        vertex_order.append(0)
                        vertex_order.append(i+1)
                        vertex_order.append(i+2)
                    for i in vertex_order:
                        for x in faceVertices[i]:
                            vertices.append(x)
                        for x in faceTextures[i]:
                            vertices.append(x)
                        for x in faceNormals[i]:
                            vertices.append(x)
                line = f.readline()
        return vertices
    
    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1,(self.vbo,))
class Render:
    pass


if __name__ == "__main__":
    GameWindow= MainGame()