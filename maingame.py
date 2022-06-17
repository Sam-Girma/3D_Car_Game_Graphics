
import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader
from tkinter import *
import numpy as np
from camera import Camera
from TextureLoader import load_texture_pygame
from ObjLoader import ObjLoader
import pyrr

class Cube:

    def __init__(self, position, eulers):

        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)

class MainGame:

    def __init__(self):

        # CAMERA settings
        cam = Camera()
        WIDTH, HEIGHT = 1280, 720
        lastX, lastY = WIDTH / 2, HEIGHT / 2
        first_mouse = True
        
        vertex_src = """
        # version 330
        layout(location = 0) in vec3 a_position;
        layout(location = 1) in vec2 a_texture;
        layout(location = 2) in vec3 a_normal;
        uniform mat4 model;
        uniform mat4 projection;
        uniform mat4 view;
        out vec2 v_texture;
        void main()
        {
            gl_Position = projection * view * model * vec4(a_position, 1.0);
            v_texture = a_texture;
        }
        """

        fragment_src = """
        # version 330
        in vec2 v_texture;
        out vec4 out_color;
        uniform sampler2D s_texture;
        void main()
        {
            out_color = texture(s_texture, v_texture);
        }
        """
        def mouse_look(xpos, ypos):
            global first_mouse, lastX, lastY

            if first_mouse:
                lastX = xpos
                lastY = ypos
                first_mouse = False

            xoffset = xpos - lastX
            yoffset = lastY - ypos

            lastX = xpos
            lastY = ypos

            cam.process_mouse_movement(xoffset, yoffset)

        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((1000, 800), pg.OPENGL|pg.DOUBLEBUF)


        pg.mouse.set_visible(False)
        pg.event.set_grab(True)

        # load here the 3d meshes
        car, car_buffer = ObjLoader.load_model("objects/carfinal.obj", False)
        roadfinal, roadfinal_buffer = ObjLoader.load_model("objects/roadfinal.obj")
        environmentfinal, environment_final = ObjLoader.load_model("objects/environmentfinal.obj")

        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

                # VAO and VBO
        VAO = glGenVertexArrays(3)
        VBO = glGenBuffers(3)
        EBO = glGenBuffers(1)

        # car VAO
        glBindVertexArray(VAO[0])
        # car Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
        glBufferData(GL_ARRAY_BUFFER, car_buffer.nbytes, car_buffer, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, car.nbytes, car, GL_STATIC_DRAW)

        # car vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, car_buffer.itemsize * 8, ctypes.c_void_p(0))
        # car textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, car_buffer.itemsize * 8, ctypes.c_void_p(12))
        # car normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, car_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # roadfinal VAO
        glBindVertexArray(VAO[1])
        # roadfinal Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
        glBufferData(GL_ARRAY_BUFFER, roadfinal_buffer.nbytes, roadfinal_buffer, GL_STATIC_DRAW)

        # roadfinal vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, roadfinal_buffer.itemsize * 8, ctypes.c_void_p(0))
        # roadfinal textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, roadfinal_buffer.itemsize * 8, ctypes.c_void_p(12))
        # roadfinal normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, roadfinal_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # environmentfinal VAO
        glBindVertexArray(VAO[2])
        # environment Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
        glBufferData(GL_ARRAY_BUFFER, environment_final.nbytes, environment_final, GL_STATIC_DRAW)

        # environment vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, environment_final.itemsize * 8, ctypes.c_void_p(0))
        # environment textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, environment_final.itemsize * 8, ctypes.c_void_p(12))
        # environment normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, environment_final.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        textures = glGenTextures(3)
        load_texture_pygame("textures/car.jpg", textures[0])
        load_texture_pygame("textures/road.jpg", textures[1])
        load_texture_pygame("textures/grass.jpg", textures[2])

        
        glUseProgram(shader)
        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
        cube_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([6, 4, 0]))
        monkey_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 4, -4]))
        floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

        model_loc = glGetUniformLocation(shader, "model")
        proj_loc = glGetUniformLocation(shader, "projection")
        view_loc = glGetUniformLocation(shader, "view")

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif  event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False

                if event.type == pg.VIDEORESIZE:
                    glViewport(0, 0, event.w, event.h)
                    projection = pyrr.matrix44.create_perspective_projection_matrix(45, event.w / event.h, 0.1, 100)
                    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

            keys_pressed = pg.key.get_pressed()
            if keys_pressed[pg.K_a]:
                cam.process_keyboard("LEFT", 0.08)
            if keys_pressed[pg.K_d]:
                cam.process_keyboard("RIGHT", 0.08)
            if keys_pressed[pg.K_w]:
                cam.process_keyboard("FORWARD", 0.08)
            if keys_pressed[pg.K_s]:
                cam.process_keyboard("BACKWARD", 0.08)


            mouse_pos = pg.mouse.get_pos()
            mouse_look(mouse_pos[0], mouse_pos[1])

            # to been able to look around 360 degrees, still not perfect
            if mouse_pos[0] <= 0:
                pg.mouse.set_pos((1279, mouse_pos[1]))
            elif mouse_pos[0] >= 1279:
                pg.mouse.set_pos((0, mouse_pos[1]))


            ct = pg.time.get_ticks() / 1000

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            view = cam.get_view_matrix()
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

            rot_y = pyrr.Matrix44.from_y_rotation(0.8 * ct)
            model = pyrr.matrix44.multiply(rot_y, cube_pos)

            # draw the cube
            glBindVertexArray(VAO[0])
            glBindTexture(GL_TEXTURE_2D, textures[0])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
            glDrawElements(GL_TRIANGLES, len(car), GL_UNSIGNED_INT, None)

            # draw the monkey
            glBindVertexArray(VAO[1])
            glBindTexture(GL_TEXTURE_2D, textures[1])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, monkey_pos)
            glDrawArrays(GL_TRIANGLES, 0, len(roadfinal))

            # draw the floor
            glBindVertexArray(VAO[2])
            glBindTexture(GL_TEXTURE_2D, textures[2])
            glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
            glDrawArrays(GL_TRIANGLES, 0, len(environmentfinal))

            pg.display.flip()
        

    pg.quit()









        
        
        
    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader
    def mainLoop(self):
        proj_loc = glGetUniformLocation(self.shader, "projection")
        view_loc = glGetUniformLocation(self.shader, "view")
        projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)

        
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        while(True):
            for event in pg.event.get():
                if (event.type == pg.QUIT):
                    
                    self.quit()
                    break
            self.handleKeys()
            RenderObj("objects/roadfinal.obj","textures/road.jpg")
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # self.renderPass.render(scene, self)

            pg.display.flip()

            glClear(GL_COLOR_BUFFER_BIT)

            
            glUseProgram(self.shader)

            view_transform = pyrr.matrix44.create_look_at(
                eye=np.array([-10, 0, 4], dtype=np.float32),
                target=np.array([0, 0, 4], dtype=np.float32),
                up=np.array([0, 0, 1], dtype=np.float32), dtype=np.float32
            )
            glUniformMatrix4fv(self.viewMatrixLocation, 1,
                            GL_FALSE, view_transform)

            # mountains
            glUniform3fv(self.colorLoc, 1, 1.0, 0.4, 0.5)
            modelTransform = pyrr.matrix44.create_identity(dtype=np.float32)
            modelTransform = pyrr.matrix44.multiply(
                m1=modelTransform,
                m2=pyrr.matrix44.create_from_z_rotation(
                    theta=np.radians(90), dtype=np.float32)
            )
            modelTransform = pyrr.matrix44.multiply(
                m1=modelTransform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array([32, 0, 0], dtype=np.float32))
            )
            glUniformMatrix4fv(self.modelMatrixLocation,
                            1, GL_FALSE, modelTransform)
            glBindVertexArray(self.road.vao)
            glDrawArrays(GL_LINES, 0, self.road.vertex_count)

            
            # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            # glUseProgram(self.shader)
            # model_transform = pyrr.matrix44.create_identity(dtype=np.float32)
            # model_transform = pyrr.matrix44.create_from_translation([0, 0, -11])
            # glUniformMatrix4fv(self.modelMatrixLocation,1,GL_FALSE,model_transform)
            # glBindVertexArray(self.road.vao)
            # glDrawArrays(GL_TRIANGLES, 0, self.road.vertex_count)
            
            

            #the below is the chess boared

            
            # glBindVertexArray(self.road.vao)
            # glDrawArrays(GL_TRIANGLES, 0, self.road.vertex_count)
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

class RenderObj:
    def __init__(self, objFile, texture):
        self.objFile=objFile
        self.texture=texture
        self.renderObj()
    def renderObj(self):
        obj=Mesh(self.objFile)
        texture=Material(self.texture)

        glBindVertexArray(obj.vao)
        glDrawArrays(GL_TRIANGLES, 0, obj.vertex_count)


class Material:

    def __init__(self, filepath):
        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        image = pg.image.load(filepath).convert()
        image_width, image_height = image.get_rect().size
        img_data = pg.image.tostring(image, 'RGBA')
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))




if __name__ == "__main__":
    GameWindow= MainGame()