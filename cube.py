import pygame
import numpy
import time

black = (0, 0, 0)
red = (255, 0, 0)
white = (255, 255, 255)
#######
x = 640
y = 480
xcenter = x / 2
ycenter = y / 2
#######
pygame.init()
surface = pygame.display.set_mode((x, y))
#######
theta = 0
thetax = 0
thetay = 0

projection = numpy.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])


#######
scale_tax = 50
radius = 6
thickness = 3
vertices = numpy.array([
    [-1, 1, 1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, -1],
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
])

#######
def center_origin(surf, p):
    return [p[0] + surf.get_width() // 2, p[1] + surf.get_height() // 2]

def scale(p):
    return p * scale_tax

######
def drawCircles(surface, color, points, radius):
    for x, y in points:
        pygame.draw.circle(surface, color, (x, y), radius)

def drawLines(surface, color, points, idxi, idxf, thickness):
    pygame.draw.line(surface, color, points[idxi], points[idxf], thickness)

######
last_call = False
t1 = 0
t2 = 0
deltaT = 0
last_timex = 0
last_timey = 0

deltaS = 0
speedx = 0
speedy = 0

accConst = 9.8 # no specific reason

######
count = 0
run = True

vertices = scale(vertices)
while run:
    surface.fill(white)

    rotation_x = numpy.array([
        [1, 0, 0],
        [0, numpy.cos(thetax), -numpy.sin(thetax)],
        [0, numpy.sin(thetax), numpy.cos(thetax)]
        ])

    rotation_y = numpy.array([
        [numpy.cos(thetay), 0, numpy.sin(thetay)],
        [0, 1, 0],
        [-numpy.sin(thetay), 0, numpy.cos(thetay)]
        ])

    rotation_z = numpy.array([
        [numpy.cos(theta), -numpy.sin(theta), 0],
        [numpy.sin(theta), numpy.cos(theta), 0],
        [0, 0, 1]
        ])

    vertices2d = numpy.array(numpy.zeros((8, 2)))
    for idx, points in enumerate(vertices):
        rotated = numpy.matmul(rotation_x, points) #x matrix
        rotated = numpy.matmul(rotation_y, rotated) #y matrix
        #rotated = numpy.matmul(rotation_z, rotated)  #z matrix
        
        projected = numpy.matmul(projection, rotated)[:2]

        projected = center_origin(surface, projected)

        vertices2d[idx] = projected

    vertices2d = numpy.round(vertices2d).astype(int)
    drawCircles(surface, red, vertices2d, radius)

    drawLines(surface, black, vertices2d, 0, 1, thickness)
    drawLines(surface, black, vertices2d, 1, 2, thickness)
    drawLines(surface, black, vertices2d, 2, 3, thickness)
    drawLines(surface, black, vertices2d, 3, 0, thickness)

    drawLines(surface, black, vertices2d, 4, 5, thickness)
    drawLines(surface, black, vertices2d, 5, 6, thickness)
    drawLines(surface, black, vertices2d, 6, 7, thickness)
    drawLines(surface, black, vertices2d, 7, 4, thickness)

    drawLines(surface, black, vertices2d, 0, 4, thickness)
    drawLines(surface, black, vertices2d, 1, 5, thickness)
    drawLines(surface, black, vertices2d, 3, 7, thickness)
    drawLines(surface, black, vertices2d, 2, 6, thickness)


    if pygame.mouse.get_pressed()[0] and not last_call:
        pygame.mouse.get_rel()
        t1 = time.time()
        last_call = True

    if not pygame.mouse.get_pressed()[0] and last_call:
        deltaS = pygame.mouse.get_rel()
        t2 = time.time()
        last_call = False
        deltaT = numpy.round(t2 - t1, decimals=2)
        speedx = numpy.round((deltaS[0] / deltaT), decimals=2)
        speedy = numpy.round((deltaS[1] / deltaT), decimals=2) * -1
        speedx = speedx / 300000
        speedy = speedy / 300000


    
    ##########
    if speedx > 0:
        speedx = speedx - accConst * 0.0000004
    elif speedx < 0:
        speedx = speedx + accConst * 0.0000004
    else:
        speedx = 0
    
    if speedy > 0:
        speedy = speedy - accConst * 0.0000004
    elif speedy < 0:
        speedy = speedy + accConst * 0.0000004
    else:
        speedy = 0


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.flip()
    

    thetax = thetax + 0.000 + speedy
    thetay = thetay + 0.000 + speedx
    count = count + 1
    

pygame.quit()