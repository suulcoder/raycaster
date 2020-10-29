import sys, os, pygame, time
from pygame.locals import *
from math import *

import random
 
pygame.init()

####------Colours------####
BLACK     = (  0,   0,   0)
BLUE      = (  0,   0, 255)
DARKBLUE  = (  0,   0,  64)
DARKGREY  = ( 64,  64,  64)
DARKRED   = ( 64,   0,   0)
WHITE     = (255, 255, 255)
RED = (255,0,0)
GREEN = (0,200,0)
BRIGHT_RED = (255,0,0)
BRIGHT_GREEN = (0,255,0)
####-------------------####

block_color = (53,115,255)


WIDTH    = 1360
HEIGHT   = 768
map_size = int((WIDTH / 680) * 64)

CLOCK    = pygame.time.Clock()
FPS      = 60
SCREEN   = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Raycaster")

map_colour     = BLUE
floor_colour   = BLACK
ceiling_colour = DARKRED

rotate_speed   = 0.03
move_speed     = 0.15
strafe_speed   = 0.04
wall_height    = 1.27
resolution     = 6 #Pixels per line

texture   = pygame.image.load('pacman.jpeg')
texWidth  = texture.get_width()
texHeight = texture.get_height()
texArray  = pygame.PixelArray(texture)


old = 0

hand = pygame.image.load('./player.png')
mira = pygame.image.load('./mira.png')

class Raycaster(object):
    def __init__(self, width, heigth):
        self.width = width
        self.heigth = heigth       

    def point(self, x, y, c = None):
      SCREEN.set_at((x, y), c)

    def draw_player(self, player, xi, yi, w = 256, h = 256, size=32):
      for x in range(xi, xi + w):
        for y in range(yi, yi + h):
          tx = int((x - xi) * size/w)
          ty = int((y - yi) * size/h)
          c = player.get_at((tx, ty))
          if c != (152, 0, 136, 255) and c!= (0, 0, 0, 0):
            self.point(x, y, c)

    def button(self,msg,x,y,w,h,ic,ac,action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            pygame.draw.rect(SCREEN, ac,(x,y,w,h))

            if click[0] == 1 and action != None:
                action()         
        else:
            pygame.draw.rect(SCREEN, ic,(x,y,w,h))

        smallText = pygame.font.SysFont("comicsansms",20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(w/2)), (y+(h/2)) )
        SCREEN.blit(textSurf, textRect)
     
    def text_objects(self,text, font, color=BLACK):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()        
        
    def message(self, message,  font_size, x, y, color):
        largeText = pygame.font.SysFont("comicsansms",font_size, color)
        TextSurf, TextRect = self.text_objects(message, largeText, color)
        TextRect.center = (x,y)
        SCREEN.blit(TextSurf, TextRect)

    def game_intro(self, game,quit):

        intro = True

        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            SCREEN.fill(BLACK)
            self.message("PAINT IT FIRST", 115,(WIDTH/2),(HEIGHT/2), WHITE)
            self.button("GO!",550,450,100,50,GREEN,BRIGHT_GREEN,game)
            self.button("Quit",700,450,100,50,RED,BRIGHT_RED,quit)

            pygame.display.update()
            CLOCK.tick(15)

    def success(self):

        success = True

        while success:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
            SCREEN.fill(BLACK)
            self.message("SUCCESS", 115,(WIDTH/2),(HEIGHT/2), WHITE)
            self.button("Quit",625,450,100,50,RED,BRIGHT_RED,self.Quit)

            pygame.display.update()
            CLOCK.tick(15)

    def create_level(self,file):
        if file[-4:] != '.txt': file += '.txt'
        f = open(file, 'r')
        file = f.readlines()

        for i, line in enumerate(file):
            file[i] = list(line.rstrip('\n'))
            for j, char in enumerate(file[i]):
                if char == ' ': file[i][j] = 0
                else:           file[i][j] = int(char)
        f.close()

        map_x  = len(file)
        map_y  = len(file[0])
        map_buffer    = []

        for i, line in enumerate(file):
            map_buffer.append([])
            for j, char in enumerate(file[i]):
                if char != 0:
                    map_buffer[i].append(char)
                else:
                    map_buffer[i].append(0)

        return map_x, map_y, map_buffer

    def Quit(self):
        pygame.quit()
        sys.exit()
            

    def draw_rectangle(self, x, y, texture):
      for cx in range(x, x + 50):
        for cy in range(y, y + 50):
          tx = int((cx - x)*128 / 50)
          ty = int((cy - y)*128 / 50)
          c = texture.get_at((tx, ty))
          self.point(cx, cy, c)

    def load_map(self, filename):
      with open(filename) as f:
        for line in f.readlines():
          self.map.append(list(line))

    def game(self):
        map_x, map_y, map_buffer = self.create_level('map')

        position_x, position_y    = 7.4442835833842285, 10.119874124901372

        direction_x, direction_y     = -0.005715065212402226, 1.2806120950661122
        plane_x, plane_y = -0.5135283099460273, -0.41459459099700735

        SCREEN.fill(BLACK)
        while True:
            if(position_y>12.5):
              self.success()
            difference = 0
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.Quit()
                    return
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.Quit()
                        return

            pygame.draw.rect(SCREEN, ceiling_colour, (0,                       0, WIDTH, (HEIGHT - map_size) / 2))
            pygame.draw.rect(SCREEN,   floor_colour, (0, (HEIGHT - map_size) / 2, WIDTH, (HEIGHT - map_size) / 2))

            for x in range(0, WIDTH, resolution):
                camera_x    = 2 * x / WIDTH - 1
                rayposition_x    = position_x
                rayposition_y   = position_y
                mapX = int(rayposition_x)
                mapY = int(rayposition_y)
                raydirection_x    = direction_x + plane_x * camera_x + 0.000000000000001
                raydirection_y    = direction_y + plane_y * camera_x + 0.000000000000001
                deltaDistX = sqrt(1 + raydirection_y ** 2 / raydirection_x ** 2)
                deltaDistY = sqrt(1 + raydirection_x ** 2 / raydirection_y ** 2)
                zBuffer    = []

                if raydirection_x < 0:
                    stepX = -1
                    sideDistX = (rayposition_x - mapX) * deltaDistX
                else:
                    stepX = 1
                    sideDistX = (mapX + 1 - rayposition_x) * deltaDistX

                if raydirection_y < 0:
                    stepY = -1
                    sideDistY = (rayposition_y- mapY) * deltaDistY
                else:
                    stepY = 1
                    sideDistY = (mapY + 1 - rayposition_y) * deltaDistY

                while True:
                    if sideDistX < sideDistY:
                        sideDistX += deltaDistX
                        mapX += stepX
                        side = 0
                    else:
                        sideDistY += deltaDistY
                        mapY += stepY
                        side = 1

                    if mapX >= map_x or mapY >= map_y or mapX < 0 or mapY < 0 or map_buffer[mapX][mapY] > 0:
                        break

                if side == 0: rayLength = (mapX - rayposition_x + (1 - stepX) / 2) / raydirection_x
                else:         rayLength = (mapY - rayposition_y+ (1 - stepY) / 2) / raydirection_y

                lineHeight = (HEIGHT / rayLength) * wall_height

                drawStart  = -lineHeight / 2 + (HEIGHT - map_size) / 2
                drawEnd    =  lineHeight / 2 + (HEIGHT - map_size) / 2

                if side == 0: wallX = rayposition_y+ rayLength * raydirection_y
                else:         wallX = rayposition_x + rayLength * raydirection_x
                wallX = abs((wallX - floor(wallX)) - 1)

                texX = int(wallX * texWidth)
                if side == 0 and raydirection_x > 0: texX = texWidth - texX - 1
                if side == 1 and raydirection_y < 0: texX = texWidth - texX - 1

                for y in range(texHeight):
                    if drawStart + (lineHeight / texHeight) * (y + 1) < 0: continue
                    if drawStart + (lineHeight / texHeight) * y > HEIGHT - map_size: break

                    colour = pygame.Color(texArray[texX][y])

                    c = 255.0 - abs(int(rayLength * 32)) * 0.85
                    if c < 1:   c = 1
                    if c > 255: c = 255

                    if side == 1: c = c * 0.5

                    new_colour = []
                    for i, value in enumerate(colour):
                        if i == 0: continue
                        new_colour.append(value * (c / 255))
                    colour = tuple(new_colour)

                    pygame.draw.line(SCREEN, colour, (x, drawStart + (lineHeight / texHeight) * y), (x, drawStart + (lineHeight / texHeight) * (y + 1)), resolution)

            for x in range(self.width):
                for y in range(self.heigth):
                    if map_buffer[y][x] != 0: pygame.draw.rect(SCREEN, map_colour, ((x * (map_size / map_x) + WIDTH) - map_size, y * (map_size / map_y) + HEIGHT - map_size, (map_size / map_x), (map_size / map_y)))

            myPosition = (position_y* (map_size / map_y) + WIDTH - map_size, position_x * (map_size / map_x) + HEIGHT - map_size)

            pygame.draw.rect(SCREEN, (  0, 255,   0), myPosition + (2, 2))
            pygame.draw.line(SCREEN, (  0, 170, 170), myPosition, ((direction_y + position_y+ plane_y) * (map_size / map_y) + WIDTH - map_size, (direction_x + position_x + plane_x) * (map_size / map_x) + HEIGHT - map_size))
            pygame.draw.line(SCREEN, (  0, 170, 170), myPosition, ((direction_y + position_y- plane_y) * (map_size / map_y) + WIDTH - map_size, (direction_x + position_x - plane_x) * (map_size / map_y) + HEIGHT - map_size))
            pygame.draw.line(SCREEN, (  0, 170, 170), ((direction_y + position_y+ plane_y) * (map_size / map_y) + WIDTH - map_size, (direction_x + position_x + plane_x) * (map_size / map_x) + HEIGHT - map_size), ((direction_y + position_y- plane_y) * (map_size / map_y) + WIDTH - map_size, (direction_x + position_x - plane_x) * (map_size / map_y) + HEIGHT - map_size))

            keys = pygame.key.get_pressed()

            if keys[K_w]:
                if not map_buffer[int(position_x + direction_x * move_speed)][int(position_y)]: position_x += direction_x * move_speed
                if not map_buffer[int(position_x)][int(position_y+ direction_y * move_speed)]: position_y+= direction_y * move_speed

            if keys[K_a]:
                if not map_buffer[int(position_x + direction_y * strafe_speed)][int(position_y)]: position_x += direction_y * strafe_speed
                if not map_buffer[int(position_x)][int(position_y- direction_x * strafe_speed)]: position_y-= direction_x * strafe_speed

            if keys[K_s]:
                if not map_buffer[int(position_x - direction_x * move_speed)][int(position_y)]: position_x -= direction_x * move_speed
                if not map_buffer[int(position_x)][int(position_y- direction_y * move_speed)]: position_y-= direction_y * move_speed

            if keys[K_d]:
                if not map_buffer[int(position_x - direction_y * strafe_speed)][int(position_y)]: position_x -= direction_y * strafe_speed
                if not map_buffer[int(position_x)][int(position_y+ direction_x * strafe_speed)]: position_y+= direction_x * strafe_speed

            if keys[K_q]: difference = -5
            if keys[K_e]: difference = 5

            if difference != 0:
                cosrot = cos(difference * rotate_speed)
                sinrot = sin(difference * rotate_speed)
                old    = direction_x
                direction_x   = direction_x * cosrot - direction_y * sinrot
                direction_y   = old  * sinrot + direction_y * cosrot
                old    = plane_x
                plane_x = plane_x * cosrot - plane_y * sinrot
                plane_y = old    * sinrot + plane_y * cosrot

            self.message("PAINT IT FIRST LAB 1", 50,(WIDTH/2),HEIGHT-100, WHITE)
            self.message("USE w to move up, s to move down, a to move left, d to move right.", 30,(WIDTH/2-50),HEIGHT-70, WHITE)
            self.message("USE q to turn the head left, e to turn the head right.", 30,(WIDTH/2-50),HEIGHT-45, WHITE)
            self.message("MOVE FORWARD TO WIN", 30,(WIDTH/2-50),HEIGHT-20, RED)
            self.draw_player(hand,1000 - 256 - 128, 650 - 256)
            self.draw_player(mira,int(WIDTH/2 - 80 ),int(HEIGHT/2 - 100),120,120,512)
            pygame.display.update()
            CLOCK.tick(FPS)


def main():
    r = Raycaster(21, 22) 
    r.game_intro(r.game,r.Quit)
    r.game()
    pygame.quit()
    r.quit()

if __name__=="__main__": main()