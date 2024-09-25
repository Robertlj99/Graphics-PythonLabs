# Import a library of functions called 'pygame'
import pygame
import numpy as np
from math import pi, sin, cos, tan

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

class Point3D:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        
class Line3D():

    def __init__(self, start, end):
        self.start = start
        self.end = end

def loadOBJ(filename):
    
    vertices = []
    indices = []
    lines = []

    f = open(filename, "r")
    for line in f:
        t = str.split(line)
        if not t:
            continue
        if t[0] == "v":
            vertices.append(Point3D(float(t[1]),float(t[2]),float(t[3])))
            
        if t[0] == "f":
            for i in range(1,len(t) - 1):
                index1 = int(str.split(t[i],"/")[0])
                index2 = int(str.split(t[i+1],"/")[0])
                indices.append((index1,index2))
            
    f.close()

    #Add faces as lines
    for index_pair in indices:
        index1 = index_pair[0]
        index2 = index_pair[1]
        lines.append(Line3D(vertices[index1 - 1],vertices[index2 - 1]))
        
    #Find duplicates
    duplicates = []
    for i in range(len(lines)):
        for j in range(i+1, len(lines)):
            line1 = lines[i]
            line2 = lines[j]
            
            # Case 1 -> Starts match
            if line1.start.x == line2.start.x and line1.start.y == line2.start.y and line1.start.z == line2.start.z:
                if line1.end.x == line2.end.x and line1.end.y == line2.end.y and line1.end.z == line2.end.z:
                    duplicates.append(j)
            # Case 2 -> Start matches end
            if line1.start.x == line2.end.x and line1.start.y == line2.end.y and line1.start.z == line2.end.z:
                if line1.end.x == line2.start.x and line1.end.y == line2.start.y and line1.end.z == line2.start.z:
                    duplicates.append(j)
                    
    duplicates = list(set(duplicates))
    duplicates.sort()
    duplicates = duplicates[::-1]

    #Remove duplicates
    for j in range(len(duplicates)):
        del lines[duplicates[j]]

    return lines

def loadHouse():
    house = []
    #Floor
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(5, 0, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 0, 5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(-5, 0, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 0, -5)))
    #Ceiling
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 5, -5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(5, 5, 5), Point3D(-5, 5, 5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(-5, 5, -5)))
    #Walls
    house.append(Line3D(Point3D(-5, 0, -5), Point3D(-5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(5, 0, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(-5, 0, 5), Point3D(-5, 5, 5)))
    #Door
    house.append(Line3D(Point3D(-1, 0, 5), Point3D(-1, 3, 5)))
    house.append(Line3D(Point3D(-1, 3, 5), Point3D(1, 3, 5)))
    house.append(Line3D(Point3D(1, 3, 5), Point3D(1, 0, 5)))
    #Roof
    house.append(Line3D(Point3D(-5, 5, -5), Point3D(0, 8, -5)))
    house.append(Line3D(Point3D(0, 8, -5), Point3D(5, 5, -5)))
    house.append(Line3D(Point3D(-5, 5, 5), Point3D(0, 8, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(5, 5, 5)))
    house.append(Line3D(Point3D(0, 8, 5), Point3D(0, 8, -5)))
	
    return house

def loadCar():
    car = []
    #Front Side
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-2, 3, 2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(2, 3, 2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(3, 2, 2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 1, 2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(-3, 1, 2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 2, 2)))

    #Back Side
    car.append(Line3D(Point3D(-3, 2, -2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(-2, 3, -2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, -2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 2, -2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(3, 1, -2), Point3D(-3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, -2), Point3D(-3, 2, -2)))
    
    #Connectors
    car.append(Line3D(Point3D(-3, 2, 2), Point3D(-3, 2, -2)))
    car.append(Line3D(Point3D(-2, 3, 2), Point3D(-2, 3, -2)))
    car.append(Line3D(Point3D(2, 3, 2), Point3D(2, 3, -2)))
    car.append(Line3D(Point3D(3, 2, 2), Point3D(3, 2, -2)))
    car.append(Line3D(Point3D(3, 1, 2), Point3D(3, 1, -2)))
    car.append(Line3D(Point3D(-3, 1, 2), Point3D(-3, 1, -2)))

    return car

def loadTire():
    tire = []
    #Front Side
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-.5, 1, .5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(.5, 1, .5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(1, .5, .5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, -.5, .5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(.5, -1, .5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(-.5, -1, .5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-1, -.5, .5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, .5, .5)))

    #Back Side
    tire.append(Line3D(Point3D(-1, .5, -.5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, -.5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, -.5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, .5, -.5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, -.5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(.5, -1, -.5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, -.5), Point3D(-1, -.5, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, -.5), Point3D(-1, .5, -.5)))

    #Connectors
    tire.append(Line3D(Point3D(-1, .5, .5), Point3D(-1, .5, -.5)))
    tire.append(Line3D(Point3D(-.5, 1, .5), Point3D(-.5, 1, -.5)))
    tire.append(Line3D(Point3D(.5, 1, .5), Point3D(.5, 1, -.5)))
    tire.append(Line3D(Point3D(1, .5, .5), Point3D(1, .5, -.5)))
    tire.append(Line3D(Point3D(1, -.5, .5), Point3D(1, -.5, -.5)))
    tire.append(Line3D(Point3D(.5, -1, .5), Point3D(.5, -1, -.5)))
    tire.append(Line3D(Point3D(-.5, -1, .5), Point3D(-.5, -1, -.5)))
    tire.append(Line3D(Point3D(-1, -.5, .5), Point3D(-1, -.5, -.5)))
    
    return tire


DISPLAY_HEIGHT = 512
DISPLAY_WIDTH = 512

class Camera:
    def __init__(self, x, y, z, r):
        self.x = x
        self.y = y
        self.z = z
        self.r = np.deg2rad(r)

    def go_home(self):
        self.x = 0
        self.y = 0
        self.z = 10
        self.r = np.deg2rad(180)

    def move_left(self):
        self.x = self.x + 0.25

    def move_right(self):
        self.x = self.x - 0.25

    def move_forward(self):
        self.z = self.z - 0.25

    def move_backward(self):
        self.z = self.z + 0.25

    def move_up(self):
        self.y = self.y + 0.25

    def move_down(self):
        self.y = self.y - 0.25

    def turn_left(self):
        self.r = self.r - np.deg2rad(2)

    def turn_right(self):
        self.r = self.r + np.deg2rad(2)

# TODO: Define global variables for camera position and properties
camera = Camera(0, 0, 10, 180)
NEAR = 1.0
FAR = 1000.0
FOV_X = np.deg2rad(100)
FOV_Y = np.deg2rad(100)
SCREEN = (1920, 1080)


def buildProjectionMatrix():	

    # TODO: Implement world-to-camera and camera-to-projection matrices
    # World to camera
    Ry = np.array([[np.cos(-camera.r), 0, np.sin(-camera.r), 0],
                   [0, 1, 0, 0],
                   [-np.sin(-camera.r), 0, np.cos(-camera.r), 0],
                   [0, 0, 0, 1]])

    T = np.array([[1, 0, 0, -camera.x],
                  [0, 1, 0, -camera.y],
                  [0, 0, 1, -camera.z],
                  [0, 0, 0, 1]])

    zoom_x = 1 / np.tan(FOV_X / 2)
    zoom_y = 1 / np.tan(FOV_Y / 2)
    m1 = (FAR + NEAR)/ (FAR - NEAR)
    m2 = (-2*NEAR*FAR)/(FAR-NEAR)

    clip_matrix = np.array([[zoom_x, 0, 0, 0],
                            [0, zoom_y, 0, 0],
                            [0, 0, m1, m2],
                            [0, 0, 1, 0]])

    return clip_matrix@Ry@T


def clipTest(pt1, pt2):

    w1 = pt1[3]
    w2 = pt2[3]

    if pt1[0] > w1 or pt1[0] < -w1 or pt1[1] > w1 or pt1[1] < -w1 or pt1[2] > w1 or pt1[2] < -w1:
        if pt2[0] > w2 or pt2[0] < -w2 or pt2[1] > w2 or pt2[1] < -w2 or pt2[2] > w2 or pt2[2] < -w2:
            return False

    return True

def toScreen(pt):

    # TODO: Implement the homogenous divide and screen transform
    w = pt[3]
    pn = pt/w
    S = np.array([[DISPLAY_WIDTH / 2, 0, 0, DISPLAY_WIDTH / 2],
                  [0, -DISPLAY_HEIGHT / 2, 0, DISPLAY_HEIGHT / 2],
                  [0, 0, 1, 0],
                  [0, 0, 0, 1]])

    pns = S@pn
    final = Point(pns[0][0].item(), pns[1][0].item())
    return final


# Initialize the game engine
pygame.init()
 
# Define the colors we will use in RGB format
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)

# Set the height and width of the screen
size = [DISPLAY_WIDTH, DISPLAY_HEIGHT]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Shape Drawing")
 
#Set needed variables
done = False
clock = pygame.time.Clock()
start = Point(0.0,0.0)
end = Point(0.0,0.0)
linelist = loadHouse()

#Loop until the user clicks the close button.
while not done:
 
    # This limits the while loop to a max of 100 times per second.
    # Leave this out and we will use all CPU we can.
    clock.tick(100)

    # Clear the screen and set the screen background
    screen.fill(BLACK)

    #Controller Code#
    #####################################################################

    for event in pygame.event.get():
        if event.type == pygame.QUIT: # If user clicked close
            done=True
            
    pressed = pygame.key.get_pressed()

    if pressed[pygame.K_a]:
        camera.move_left()

    if pressed[pygame.K_d]:
        camera.move_right()

    if pressed[pygame.K_w]:
        camera.move_forward()

    if pressed[pygame.K_s]:
        camera.move_backward()

    if pressed[pygame.K_r]:
        camera.move_up()

    if pressed[pygame.K_f]:
        camera.move_down()

    if pressed[pygame.K_h]:
        camera.go_home()

    if pressed[pygame.K_q]:
        camera.turn_left()

    if pressed[pygame.K_e]:
        camera.turn_right()


    #Viewer Code#
    #####################################################################

    project = buildProjectionMatrix()

    for s in linelist:
        
        pt1_w = np.matrix([[s.start.x],[s.start.y],[s.start.z],[1]])
        pt2_w = np.matrix([[s.end.x],[s.end.y],[s.end.z],[1]])
        
        pt1_c = project*pt1_w
        pt2_c = project*pt2_w
        
        if clipTest(pt1_c,pt2_c):
            pt1_s = toScreen(pt1_c)
            pt2_s = toScreen(pt2_c)
            pygame.draw.line(screen, BLUE, (pt1_s.x, pt1_s.y), (pt2_s.x, pt2_s.y))

    # Go ahead and update the screen with what we've drawn.
    # This MUST happen after all the other drawing commands.
    pygame.display.flip()

# Be IDLE friendly
pygame.quit()
