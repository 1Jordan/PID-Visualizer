import pygame
import math

pygame.init()

size = width, height = 1000, 1000
screenCenter = width/2, height/2

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("PID Visualizer")
clock = pygame.time.Clock()

surf = pygame.Surface((800,100))
surf.fill(white)
surf.set_colorkey(red)
rect = pygame.Rect(0,0,800,100)

#PID Constants:
p = 0.001
d = 0.1
i = 0.00002

prevError = 0
integralSum = 0

def game_loop():
    global prevError
    global integralSum
    
    ended = False
    
    currentAngle = 0
    setpointAngle = 0
    angleChange = 0

    while not ended:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ended = True

            #if event.type == pygame.MOUSEBUTTONUP:
                #mousex, mousey = pygame.mouse.get_pos()
                #setpointAngle = get_setpoint_angle(mousex, mousey)
            #print(event)

        mousex, mousey = pygame.mouse.get_pos()
        setpointAngle = get_setpoint_angle(mousex, mousey)
                
        error = setpointAngle - currentAngle
        integralSum += error

        angleChange = pid(error, prevError, integralSum, angleChange)
        currentAngle += angleChange 
        update_rect(currentAngle)
        
        prevError = error
        pygame.display.update()
        clock.tick(60)

def pid(error, prevError, integralSum, change):
    angleAcceleration = (error)*p + (integralSum)*i  + (error - prevError)*d
    change += angleAcceleration+0.03
    return change

def get_setpoint_angle(mousex, mousey):
    x = mousex - screenCenter[0]
    y = mousey - screenCenter[1]

    angle = math.degrees(math.atan2(y, x))

    return -angle

def update_rect(angle):
    pygame.draw.rect(surf, (100,0,0), rect)
    
    where = screenCenter[0] - 400, screenCenter[1] - 50
    blittedRect = screen.blit(surf, where)
    oldCenter = blittedRect.center

    rotatedSurf = pygame.transform.rotate(surf, angle)
    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter

    screen.fill(black)
    screen.blit(rotatedSurf, rotRect)

game_loop()
pygame.quit()
quit()
