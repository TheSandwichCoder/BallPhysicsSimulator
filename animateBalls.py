import pygame
from vector import Vec2
from Chunk import Chunks
import math
import numpy
screen = pygame.display.set_mode((1280,720))

pygame.init()

clock = pygame.time.Clock()

pygame.font.init()
pygame.font.get_init()

font = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", 15)

#   WOAH YOU FOUND AN EASTER EGG!

i = 0
def draw_dashed_line(start_pos, end_pos, width=1, dash_length=10, color = (255,255,255)):



    x1, y1 = start_pos
    x2, y2 = end_pos
    x1 = int(x1)
    y1 = int(y1)
    x2 = int(x2)
    y2 = int(y2)




    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(screen, color, start, end, width)

def draw_arrow(start_pos, end_pos, dotted, color):
    width = 3
    length = 20
    angle = 40

    pos = (start_pos-end_pos).position
    true_angle = math.atan2(pos[1], pos[0])
    a1 = true_angle+angle/180*math.pi
    a2 = true_angle-angle/180*math.pi
    pos1 = (Vec2((math.cos(a1), math.sin(a1)))*length+end_pos)
    pos2 = (Vec2((math.cos(a2), math.sin(a2)))*length+end_pos)

    if dotted:
        draw_dashed_line(start_pos.position, end_pos.position, width=width, color=color)
        # draw_dashed_line(end_pos.position, pos1.position, width=width)
        # draw_dashed_line(end_pos.position, pos2.position, width=width)
        pygame.draw.line(screen, color, end_pos.position, pos1.position, width)
        pygame.draw.line(screen, color, end_pos.position, pos2.position, width)

    else:
        pygame.draw.line(screen, color, start_pos.position, end_pos.position, width)
        pygame.draw.line(screen, color, end_pos.position, pos1.position, width)
        pygame.draw.line(screen, color, end_pos.position, pos2.position, width)



class Text:
    def __init__(self, text, pos):
        self.pos = pos
        self.text = text

    def draw(self):
        text = font.render(self.text,1,(255,255,255))
        size = Vec2(text.get_size())
        screen.blit(text, (self.pos-size*0.5).position)



class CircleThing():
    def __init__(self):
        self.radius = 50
        self.pos = Vec2((203,360))
        self.direction = Vec2((50,-200))
        self.mainDirection = Vec2((0,-150))
        self.gravity = False
        self.gravVec = Vec2((0,0))
        self.prevPos = self.pos
        self.color = (250,150,240)
        self.posText = Text("r", (0,0))
        self.radiusText = Text("r", (0,0))
        self.drawState = 0


    def draw(self):
        pygame.draw.circle(screen, (0, 0, 0), self.pos.position, self.radius)
        pygame.draw.circle(screen, self.color, self.pos.position, self.radius-6)
        pygame.draw.circle(screen, (0,0,0), self.pos.position, 3)



    def drag(self):
        if pygame.mouse.get_pressed()[0]:
            if (Vec2(pygame.mouse.get_pos()) - self.pos).mag < self.radius:
                self.pos = Vec2(pygame.mouse.get_pos())
                draw_dashed_line(self.pos.position, self.prevPos.position, width=3)



        else:
            self.prevPos = Vec2(self.pos.position)


        self.posText.text = f"pos = {self.pos.int().position}"
        self.posText.pos = (self.pos + Vec2((0, self.radius+10)))

        if self.drawState >= 1:
            self.posText.draw()

    def scale(self):
        if pygame.mouse.get_pressed()[2]:
            mag = (Vec2(pygame.mouse.get_pos()) - self.pos).mag
            if mag < self.radius+50:
                self.radius = int(mag)
        self.radiusText.pos = (self.pos + Vec2((self.radius/2, -10)))
        self.radiusText.text = f"r = {self.radius}"


        if self.drawState >= 3:
            self.radiusText.draw()
            draw_dashed_line(self.pos.int().position, ((self.pos + Vec2((self.radius, 0))).int().position), width=3)

    def makeVec(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_v]:
            if pygame.mouse.get_pressed()[0]:
                self.direction = Vec2(pygame.mouse.get_pos())-self.pos
                self.mainDirection = self.direction


        if self.drawState >= 2:
            draw_arrow(self.pos.int(), (self.pos+self.mainDirection).int(), True, (200,200,200))

    def gravitise(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_g]:
            self.gravity = True

        if self.gravity:
            self.gravVec = Vec2((0,9.807))
            draw_arrow(self.pos.int(), (self.pos + Vec2((0,9.807*10))).int(), True, (200, 200, 50))


    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_m]:
            # self.mainDirection += self.direction
            self.mainDirection += self.gravVec
            self.pos += self.mainDirection*0.01

    def containerPhy(self):
        if self.pos.y+self.radius > 720:

            self.mainDirection = Vec2((self.mainDirection.x, -self.mainDirection.y * 0.7))
            self.pos.update(self.pos.x, 720 - self.radius)

        if self.pos.x - self.radius < 0:
            self.mainDirection = Vec2((-self.mainDirection.x*0.7, self.mainDirection.y))
            self.pos.update(self.radius, self.pos.y)

        if self.pos.x + self.radius > 405:
            self.mainDirection = Vec2((-self.mainDirection.x*0.7, self.mainDirection.y))
            self.pos.update(405-self.radius, self.pos.y)

chunk = Chunks()
chunk.intervals = 100

def drawGridLines():
    chunk.draw(screen)

def get_TransRect(hitbox,alpha, color, screen):
    s = pygame.Surface((hitbox[2], hitbox[3]))
    s.set_alpha(alpha)
    s.fill(color)
    screen.blit(s, (hitbox[0], hitbox[1]))

def get_TransCircle(radius,pos, alpha, color, screen):
    surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surface, (color[0], color[1], color[2], alpha), (radius, radius), radius)
    screen.blit(surface, (pos[0]-radius, pos[1]-radius))



def draw_surroundingObjects(pos, index, opacity, screen):
    x_index = pos.x // 100
    y_index = pos.y // 100

    offset = (index//3-1, index%3-1)


    y_index1 = y_index + offset[1]
    x_index1 = x_index + offset[0]

    if index == 7:
        get_TransRect(pygame.Rect((x_index1) * 100, (y_index1) * 100, 100, 100), 150*opacity, (0, 255, 0), screen)

    else:
        get_TransRect(pygame.Rect((x_index1) * 100, (y_index1) * 100, 100, 100), 150*opacity, (255,0,0), screen)

def clamp(min, max, var):
    if var < min:
        return min
    elif var > max:
        return max
    return var




circleThing = CircleThing()
circleThing2 = CircleThing()

chunkThingIndex = 0
chunkThingIndex_timer = 30
newTimer = 0

circleThing2.pos.update(200,100)
thing = True

posArrayThing = ()
prev_posArrayThing = ()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    screen.fill((30, 30, 30))
    drawGridLines()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q]:
        if thing:
            # circleThing.drawState += 1
            thing = False
    else:
        thing = True




    circleThing.makeVec()

    circleThing.draw()


    circleThing.drag()
    circleThing.scale()
    circleThing.gravitise()
    circleThing.containerPhy()

    circleThing.move()


    circleThing2.makeVec()

    circleThing2.draw()

    circleThing2.drag()
    circleThing2.scale()
    circleThing2.gravitise()
    circleThing2.containerPhy()

    circleThing2.move()

    if not thing:

        if chunkThingIndex_timer % 30 == 0 and chunkThingIndex != 8:
            chunkThingIndex += 1


        percentage = chunkThingIndex_timer%30/30
        finalVal = -(percentage-0.5)**2*4+1



        if chunkThingIndex == 7:
            get_TransCircle(50, circleThing.pos.position, 100, (0, 250, 0), screen)

        if not chunkThingIndex == 8:
            chunkThingIndex_timer += 1
            draw_surroundingObjects(circleThing2.pos, chunkThingIndex%9,(finalVal) ,screen)
        else:
            chunkThingIndex_timer = 1

        if chunkThingIndex == 8:
            newTimer += 0.6




            if newTimer <= 40:
                percentage = (newTimer / 15) ** 3
                percentage = clamp(0.01, 1, percentage)
                draw_dashed_line(circleThing.pos.position, (circleThing.pos+(circleThing2.pos-circleThing.pos)*percentage).position, width=3, dash_length=5)

            elif newTimer>40 and newTimer <= 75:



                mag = ((circleThing.radius+circleThing2.radius)-abs((circleThing.pos - circleThing2.pos).mag))/abs((circleThing.pos - circleThing2.pos).mag)

                percentage = (-(((newTimer - 40) / 25) ** 3) + 1)*1/mag
                percentage = clamp(1, 1/mag, percentage)

                print("mag",percentage)
                pos1 = (circleThing2.pos + (circleThing.pos - circleThing2.pos) * (percentage) * mag).position
                pos2 = (circleThing.pos + (circleThing2.pos - circleThing.pos) * (percentage) * mag).position

                draw_dashed_line(pos1,pos2,width=3, dash_length=5)

            elif newTimer > 75 and newTimer <= 105:
                percentage = -(((newTimer - 75) / 30) ** 3) +1
                percentage = clamp(0.5, 1, percentage)
                print(percentage)

                mag = ((circleThing.radius + circleThing2.radius) - abs((circleThing.pos - circleThing2.pos).mag)) / abs((circleThing.pos - circleThing2.pos).mag)

                pos1 = (circleThing2.pos + (circleThing.pos - circleThing2.pos) * percentage * mag).position
                pos2 = (circleThing.pos + (circleThing2.pos - circleThing.pos) * mag).position
                posArrayThing = (pos1, pos2)
                # pygame.draw.line(screen, (255, 255, 255), *posArrayThing, 3)
                prev_posArrayThing = (circleThing.pos, circleThing2.pos)
                draw_dashed_line(pos1, pos2, width=3, dash_length=2)

            elif newTimer > 110 and newTimer < 160:
                percentage = ((newTimer - 110) / 50) ** 3 * 2
                percentage = clamp(0.01, 1, percentage)



                dis = prev_posArrayThing[0] - prev_posArrayThing[1]
                dif = circleThing.radius + circleThing2.radius - dis.mag
                dis.normalise_self()
                # pygame.draw.line(screen,(255,255,255), *posArrayThing,3)
                draw_dashed_line(posArrayThing[0], posArrayThing[1], width=3, dash_length=2)
                circleThing.pos = prev_posArrayThing[0]+((dis * (dif/2))*percentage)
                circleThing2.pos = prev_posArrayThing[1]-((dis * (dif/2))*percentage)


            if newTimer > 150:
                percentage = ((newTimer - 150) / 10) ** 3 * 2
                percentage = clamp(0.01, 1, percentage)

                draw_arrow(circleThing.pos,
                           circleThing.pos + ((circleThing2.pos - circleThing.pos).normalise()) * -100 * percentage,
                           False, (255, 255, 255))
                draw_arrow(circleThing2.pos,
                           circleThing2.pos - ((circleThing2.pos - circleThing.pos).normalise()) * -100 * percentage,
                           False, (255, 255, 255))

                circleThing.pos += ((prev_posArrayThing[1]-prev_posArrayThing[0]).normalise())*-3
                circleThing2.pos += ((prev_posArrayThing[0]-prev_posArrayThing[1]).normalise())*-3
                # draw_dashed_line(posArrayThing[0], posArrayThing[1], width=3, dash_length=2)






    i += 1
    clock.tick(60)
    pygame.display.flip()




















