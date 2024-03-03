import math

import pygame.draw
from random import randint
from vector import Vec2
import settings


ScreenSize = (1280, 720)

# @njit
# def collision(ball1pos, ball1vec,ball1rad, ball1Elas, ball2pos, ball2vec, ball2rad, ball2Elas):
#     vec1 = (ball1pos[0]-ball2pos[0], ball1pos[1]-ball2pos[1])
#     dis = (vec1[0]**2+vec1[1]**2)**0.5
#     totalRad = ball1rad + ball2rad
#
#     dif = totalRad-dis
#     normVec1 = (vec1[0]/dis, vec1[1]/dis)
#     halfDif = dif/2
#     finalPos1 = [ball1pos[0]+normVec1[0]*(halfDif),ball1pos[1]+normVec1[1]*(halfDif)]
#     finalPos2 = [ball2pos[0]+normVec1[0]*(-halfDif),ball2pos[1]+normVec1[1]*(-halfDif)]
#     aveElasticity = ((ball1Elas+ball2Elas)/2)
#     ball1vec = list(ball1vec)
#     ball2vec = list(ball2vec)
#
#     if finalPos1[1] - ball1rad < 0:
#         finalPos1[1] = ball1rad
#         ball1vec[1] = -abs(ball1vec[1]) * ball1Elas
#
#     elif finalPos1[1] + ball1rad > ScreenSize[1]:
#         finalPos1[1] = ScreenSize[1]-ball1rad
#         ball1vec[1] = abs(ball1vec[1]) * ball1Elas
#
#     if finalPos1[0] - ball1rad < 0:
#         finalPos1[0] = ball1rad
#         ball1vec[0] = abs(ball1vec[0]) * ball1Elas
#
#     elif finalPos1[0] + ball1rad > ScreenSize[0]:
#         finalPos1[0] = ScreenSize[0]-ball1rad
#         ball1vec[0] = -abs(ball1vec[0]) * ball1Elas
#
#
#     if finalPos2[1] - ball2rad < 0:
#         finalPos2[1] = ball2rad
#         ball2vec[1] = -abs(ball2vec[1]) * ball2Elas
#
#     elif finalPos2[1] + ball2rad > ScreenSize[1]:
#         finalPos2[1] = ScreenSize[1] - ball2rad
#         ball2vec[1] = abs(ball2vec[1]) * ball2Elas
#
#     if finalPos2[0] - ball2rad < 0:
#         finalPos2[0] = ball2rad
#         ball2vec[0] = abs(ball2vec[0]) * ball2Elas
#
#     elif finalPos2[0] + ball2rad > ScreenSize[0]:
#         finalPos2[0] = ScreenSize[0] - ball2rad
#         ball2vec[0] = -abs(ball2vec[0]) * ball2Elas
#
#     val = dif*aveElasticity*10
#     ball1vec = (ball1vec[0]+normVec1[0]*val, ball1vec[1]+normVec1[1]*val)
#     ball2vec = (ball2vec[0]+normVec1[0]*-val, ball2vec[1]+normVec1[1]*-val)
#
#     return (finalPos1, ball1vec, finalPos2, ball2vec)



class Ball:
    def __init__(self,pos, vec, size):
        self.pos = Vec2(pos)
        self.vec = Vec2(vec)
        self.size = settings.BALLSIZE
        self.radius = self.size/2
        self.elasticity = settings.BALLELASTICITY
        self.maincolor = (randint(0,255), randint(0,255), randint(0,255))
        self.color = self.maincolor
        self.pressure = 0
        self.angularMomentum = 0
        self.angle = 0

    def is_containerCollision(self):
        n1 = False
        n2 = False
        n3 = False
        n4 = False

        if self.pos.x - self.radius < 0:
            n1 = True

        if self.pos.x + self.radius > ScreenSize[0]:
            n2 = True

        if self.pos.y - self.radius < 0:
            n3 = True

        if self.pos.y + self.radius > ScreenSize[1]:
            n4 = True

        return (n1,n2,n3,n4)

    def containerCollisionPhysics(self):
        collisionBool = self.is_containerCollision()
        if collisionBool[3]:
            self.pos = Vec2((self.pos.x, ScreenSize[1]-self.radius))
            self.vec = Vec2((self.vec.x, -abs(self.vec.y)*self.elasticity))

            if settings.ANGLECALCULATIONS and self.angularMomentum < abs(self.vec.x/self.size / math.pi * 180):
                self.angularMomentum -= self.vec.x/ self.size / math.pi * 180 * 0.01

        elif collisionBool[2]:
            self.pos = Vec2((self.pos.x, self.radius))
            self.vec = Vec2((self.vec.x, abs(self.vec.y)*self.elasticity))

        elif collisionBool[0]:
            self.pos = Vec2((self.radius, self.pos.y))
            self.vec = Vec2((abs(self.vec.x)*self.elasticity, self.vec.y))

        elif collisionBool[1]:
            self.pos = Vec2((ScreenSize[0]-self.radius, self.pos.y))
            self.vec = Vec2((-abs(self.vec.x)*self.elasticity, self.vec.y))


    def is_ballCollision(self, ball):
        dis = self.pos- ball.pos

        if dis.mag < (self.radius+ball.radius):
            return True
        return False

    def ballCollisionPhysics(self, ball):
        if self.is_ballCollision(ball):
            dis = self.pos - ball.pos
            if settings.ANGLECALCULATIONS:
                perpendicularDis = dis.perpendicular_norm()

                self.angularMomentum /= 2
                ball.angularMomentum /= 2

            dif = self.radius+ball.radius-dis.mag

            dis.normalise_self()
            ave_elasticity = ((self.elasticity+ball.elasticity)/2)
            d1 = dis * (dif/2)
            d2 = dis * dif * ave_elasticity * 10

            self.pos.increment(d1)
            ball.pos.increment(-d1)
            # self.containerCollisionPhysics()
            # ball.containerCollisionPhysics()

            self.vec.increment(d2)
            ball.vec.increment(-d2)

            self.pressure += d2.mag

            if settings.ANGLECALCULATIONS:
                thing = (ball.vec-self.vec).overlap(perpendicularDis)
                thing2 = (thing/self.radius)*180/math.pi
                self.angularMomentum += thing2
                ball.angularMomentum -= thing2

            return True
        return False

    # def compiledBallCollisionPhysics(self, ball):
    #     if self.is_ballCollision(ball):
    #         values = collision(self.pos.position, self.vec.position, self.radius, self.elasticity, ball.pos.position, ball.vec.position, ball.radius, ball.elasticity)
    #         self.pos = Vec2(values[0])
    #         self.vec = Vec2(values[1])
    #         ball.pos = Vec2(values[2])
    #         ball.vec = Vec2(values[3])
    #         self.pressure += 1
    #         return True
    #     return False




    def gravity(self, delta):
        self.vec.increment(settings.GRAVITYVEC*delta)

    def update(self, delta):
        self.size = settings.BALLSIZE
        self.elasticity = settings.BALLELASTICITY
        self.radius = self.size/2
        self.pressure = 0
        self.gravity(delta)
        self.containerCollisionPhysics()
        self.pos.increment(self.vec*delta)
        self.angle += (self.angularMomentum)*delta
        self.angle %= 360

        if self.vec.mag > 1000:
            self.vec = self.vec.normalise()*1000

        # self.angularMomentum /= 1.01


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.position, self.radius)
        if settings.ANGLECALCULATIONS:
            angleRadian = self.angle*math.pi/180
            pygame.draw.line(screen, (0,0,0), *(self.pos.position, (self.pos+Vec2((math.sin(angleRadian), math.cos(angleRadian)))*self.radius).position),1)
        if settings.DRAWVECTOR:
            self.drawVector(screen)
        self.color = self.maincolor

    def drawVector(self, screen):
        pygame.draw.line(screen, self.maincolor, *(self.pos.position,(self.pos+self.vec.normalise()*self.size*1.5).position))
