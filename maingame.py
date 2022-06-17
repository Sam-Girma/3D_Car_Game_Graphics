import pygame as pg
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from tkinter import *
import time
from camera import Camera
from TextureLoader import load_texture_pygame
from ObjLoader import ObjLoader
import pyrr


class MainGame:

    def __init__(self):
        self.initial_time = time.time()
        self.carcolorchange = False
        # CAMERA settings
        self.cam = Camera()
        WIDTH, HEIGHT = 1280, 720
        
        
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK,
                                    pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.set_mode((WIDTH, HEIGHT), pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        

        self.clock = pg.time.Clock()
        
        glClearColor(1.0, 1.2, 0.2, 1)


        # load here the 3d meshes
        self.car_indices, self.car_buffer = ObjLoader.load_model("objects/car.obj", False)
        self.road_indices, self.roadfinal_buffer = ObjLoader.load_model("objects/road.obj")
        self.environment_indices, self.environment_buffer = ObjLoader.load_model("objects/led.obj")

        shader = self.createShader('shaders/vertex.txt', 'shaders/fragment.txt')
                
        self.VAO = glGenVertexArrays(3)
        self.VBO = glGenBuffers(3)
        self.EBO = glGenBuffers(1)
        self.binder()

        self.textures = glGenTextures(3)
        self.textureloader()
        
        

        
        glUseProgram(shader)
        glClearColor(0, 0.1, 0.1, 1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
        self.car_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([6, 4, 0]))
        self.road_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 4, -4]))
        self.environment_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))

        self.model_loc = glGetUniformLocation(shader, "model")
        self.proj_loc = glGetUniformLocation(shader, "projection")
        self.view_loc = glGetUniformLocation(shader, "view")

        glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, self.projection)

        self.mainLoop()
        

 

    def binder(self):
        glBindVertexArray(self.VAO[0])
        # car Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[0])
        glBufferData(GL_ARRAY_BUFFER, self.car_buffer.nbytes, self.car_buffer, GL_STATIC_DRAW)

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.car_indices.nbytes, self.car_indices, GL_STATIC_DRAW)

        # car vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.car_buffer.itemsize * 8, ctypes.c_void_p(0))
        # car textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.car_buffer.itemsize * 8, ctypes.c_void_p(12))
        # car normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.car_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)

        # roadfinal VAO
        glBindVertexArray(self.VAO[1])
        # roadfinal Vertex Buffer Object
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO[1])
        glBufferData(GL_ARRAY_BUFFER, self.roadfinal_buffer.nbytes, self.roadfinal_buffer, GL_STATIC_DRAW)

        # roadfinal vertices
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.roadfinal_buffer.itemsize * 8, ctypes.c_void_p(0))
        # roadfinal textures
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.roadfinal_buffer.itemsize * 8, ctypes.c_void_p(12))
        # roadfinal normals
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.roadfinal_buffer.itemsize * 8, ctypes.c_void_p(20))
        glEnableVertexAttribArray(2)


    def textureloader(self):
        if not self.carcolorchange:
            load_texture_pygame("textures/car.jpg", self.textures[0])
        else:
            load_texture_pygame("textures/black.jpg", self.textures[0])
        load_texture_pygame("textures/road.jpg", self.textures[1])
        load_texture_pygame("textures/grass.jpg", self.textures[2])



        
        
        
    def createShader(self, vertexFilepath, fragmentFilepath):

        with open(vertexFilepath,'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilepath,'r') as f:
            fragment_src = f.readlines()
        
        shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER),
                                compileShader(fragment_src, GL_FRAGMENT_SHADER))
        
        return shader
    def mainLoop(self):
        running = True

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()
                    running = False
                elif  event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                    running = False

                if event.type == pg.VIDEORESIZE:
                    glViewport(0, 0, event.w, event.h)
                    projection = pyrr.matrix44.create_perspective_projection_matrix(45, event.w / event.h, 0.1, 100)
                    glUniformMatrix4fv(self.proj_loc, 1, GL_FALSE, projection)

            self.inputKeyHandler()


            ct = pg.time.get_ticks() / 1000

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            view = self.cam.get_view_matrix()
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)

            
            self.draw(0, self.car_indices)
            self.drawroad(1, self.road_indices)
            


            pg.display.flip()
           
    def draw(self, index, indices):
        rot_y = pyrr.Matrix44.from_y_rotation(0.2 )
        model = pyrr.matrix44.multiply(rot_y, self.car_pos)
        glBindVertexArray(self.VAO[index])
        glBindTexture(GL_TEXTURE_2D, self.textures[index])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
        

    def drawroad(self, index, indices):
        glBindVertexArray(self.VAO[index])
        glBindTexture(GL_TEXTURE_2D, self.textures[index])
        glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, self.road_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(self.road_indices))




    def inputKeyHandler(self):
        keys_pressed = pg.key.get_pressed()
        if keys_pressed[pg.K_a]:
            self.cam.process_keyboard("LEFT", 0.08)
        if keys_pressed[pg.K_d]:
            self.cam.process_keyboard("RIGHT", 0.08)
        if keys_pressed[pg.K_w]:
            self.cam.process_keyboard("FORWARD", 0.08)
        if keys_pressed[pg.K_s]:
            self.cam.process_keyboard("BACKWARD", 0.08)
        # keys = pg.key.get_pressed()
        if keys_pressed[pg.K_c]:
            self.carcolorchange = True
        # #left, right, up, down
        if keys_pressed[pg.K_LEFT]:
            pass
        elif keys_pressed[pg.K_RIGHT]:
            pass
        elif keys_pressed[pg.K_UP]:
            pass
        elif keys_pressed[pg.K_DOWN]:
            pass
    def quit(self):
        EndApp((time.time() - self.initial_time)*100000)
        glDeleteVertexArrays(1, (self.VAO,))
        glDeleteBuffers(1,(self.VBO,))
        pg.quit()


class StartApp:
    def __init__(self):
        
        input_Window= Tk()
        input_Window.title("Custom car Game.")
        input_Window.minsize(800, 400)
        input_Window['background']= "#CCCEB5"

        # Below is the heading for the input window.
        Label(input_Window, text="Welcome to custom car game!", font='times 25 italic', bg = '#CBCEB5').place(x=200, y=5)


        Label(input_Window, text="The following are instructions to follow! happy gaming!", bg='#CBCEB5',
                font='times 16').place(x=10, y=60) 
                    # label for choice of the first graph.
        Label(input_Window, text="To Move to the right use right arrow or letter D.", bg='#CBCEB5',
                font='times 13').place(x=30, y=100)  

        Label(input_Window, text="To Move to the left use left arrow or letter A.", bg='#CBCEB5',
                font='times 13').place(x=30, y=150)  
        Label(input_Window, text="To Move to the backward use down arrow or letter S.", bg='#CBCEB5',
                font='times 13').place(x=30, y=200)
        Label(input_Window, text="To Move to the forward use up arrow or letter W.", bg='#CBCEB5',
                font='times 13').place(x=30, y=250)
        Label(input_Window, text="To Change car color press C.", bg='#CBCEB5',
                font='times 13').place(x=30, y=300)

        #below is draw button with a command to display the graph on a pygame window.
        End_Button = Button(input_Window, text="Cancel", bg='red', fg='white', font='times 12 bold',command=lambda: input_Window.quit()).place(x=200,y=350)
        Start_Button = Button(input_Window, text="Start", bg='blue', fg='white', font='times 12 bold',command=lambda: MainGame()).place(x=400,y=350)


        mainloop()
class EndApp:
    def __init__(self, score):
        final= Tk()
        final.title("Custom car Game.")
        final.minsize(750, 400)
        final['background']= "#CCCEB5"

        Label(final, text="Yayyy you made it to the End!", font='times 25 italic', bg = '#CBCEB5').place(x=200, y=5)
        Label(final, text="Your Score is!", font='times 20 italic', bg = '#CBCEB5').place(x=300, y=100)

        Label(final, text= score, font='times 15 italic', bg = '#CBCEB5').place(x=350, y=150)
        
        End_Button = Button(final, text="End Game", bg='red', fg='white', font='times 12 bold',command=lambda: final.quit()).place(x=210,y=220)
        Start_Button = Button(final, text="Replay Game", bg='blue', fg='white', font='times 12 bold',command=lambda: StartApp()).place(x=410,y=220)

        mainloop()
if __name__ == "__main__":
    GameWindow= StartApp()