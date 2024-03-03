import pygame

import settings
from ball import Ball
from vector import Vec2
from random import randint
from Chunk import Chunks
import time


pygame.init()

pygame.font.init()
pygame.font.get_init()

screenSize = (1280, 720)



pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screenSize,pygame.RESIZABLE)

font = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", 15)

ballArray = []
chunks = Chunks()

generalDelta = 0.06
delta = 0.1
intervals = 50
see_chunks = False
paused = False

gravityVecChangeRandomVar = False
gravityVecChangeRandomVec = Vec2((0,0))

def clamp(min, max, n):
    if n > max:
        return max
    elif n < min:
        return min
    return n

def keyinputs(ballArray):
    global delta
    global generalDelta
    global see_chunks
    global chunks
    global gravityVecChangeRandomVar
    global gravityVecChangeRandomVec

    keys = pygame.key.get_pressed()
    pos = pygame.mouse.get_pos()

    if keys[pygame.K_g] and pygame.mouse.get_pressed()[0]:
        if gravityVecChangeRandomVar:
            settings.GRAVITYVEC = (Vec2(pygame.mouse.get_pos()) - gravityVecChangeRandomVec)*0.1
        else:
            gravityVecChangeRandomVec = Vec2(pygame.mouse.get_pos())
        gravityVecChangeRandomVar = True

        pygame.draw.circle(screen, (255,255,255), pygame.mouse.get_pos(), 30)
        pygame.draw.circle(screen, (255,255,255), gravityVecChangeRandomVec.position, 30,3)

        return
    else:
        gravityVecChangeRandomVar = False

    if pygame.mouse.get_pressed()[0] and not keys[pygame.K_BACKSPACE]:
        n_balls = 5
        randomness1 = 30
        randomness2 = 60
        randomness3 = 20
        randomness4 = 20
        pos = pygame.mouse.get_pos()
        for i in range(n_balls):
            ballArray.append(
                Ball((pos[0] + randint(-randomness1, randomness1), pos[1] + randint(-randomness1, randomness1)),
                     (randint(-randomness2, randomness2), randint(-randomness2, randomness2)),
                     randint(randomness3, randomness4)))

    if keys[pygame.K_BACKSPACE]:
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:

            ballArray.clear()
        elif pygame.mouse.get_pressed()[0]:
            for ball in ballArray:
                if (ball.pos-Vec2(pygame.mouse.get_pos())).mag < 50:
                    ballArray.remove(ball)


    if keys[pygame.K_e]:
        ballArray.append(Ball(pos, (0,0),10))

    if keys[pygame.K_a]:
        settings.ANGLECALCULATIONS = not settings.ANGLECALCULATIONS


    if keys[pygame.K_q] and settings.BALLSIZE > 5:
        settings.BALLSIZE -= 1
        chunks = Chunks()
    elif keys[pygame.K_w]:
        settings.BALLSIZE += 1
        chunks = Chunks()

    if keys[pygame.K_r]:
        settings.BALLELASTICITY -= 0.01
    elif keys[pygame.K_t]:
        settings.BALLELASTICITY += 0.01

    if keys[pygame.K_p]:
        for ball in ballArray:
            ball.vec = Vec2((0,0))

    if keys[pygame.K_c]:
        see_chunks = True

    else:
        see_chunks = False


    if keys[pygame.K_s]:
        maxspeed = 300
        for ball in ballArray:
            intensity = clamp(0,255,255*ball.vec.mag/maxspeed)
            ball.color = (intensity,intensity,intensity)

    elif keys[pygame.K_d]:
        maxpressure = 30
        for ball in ballArray:
            intensity = clamp(0,255,255*ball.pressure/maxpressure)
            ball.color = (intensity,intensity,intensity)

    if keys[pygame.K_v]:
        settings.DRAWVECTOR = True
    else:
        settings.DRAWVECTOR = False


    if pygame.mouse.get_pressed()[2]:
        if not keys[pygame.K_LSHIFT]:
            for ball in ballArray:
                vec = Vec2((pos[0] - ball.pos.x, pos[1] - ball.pos.y)).normalise()*100*delta
                ball.vec.increment(vec)
        else:
            for ball in ballArray:
                vec = Vec2((pos[0] - ball.pos.x, pos[1] - ball.pos.y)).normalise()*-100*delta
                ball.vec.increment(vec)



def delta_stuff():
    global paused
    global delta
    global generalDelta
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        paused = True
    else:
        paused = False



    if keys[pygame.K_LEFT]:
        if generalDelta > 0.001:
            generalDelta -= 0.001
    elif keys[pygame.K_RIGHT]:
        if generalDelta < 10:
            generalDelta += 0.001

    elif keys[pygame.K_DOWN]:
        generalDelta = 0.1

    delta = generalDelta


def chunking(ballArray):
    chunks.clear()
    for ball in ballArray:
        ball.containerCollisionPhysics()

    chunks.addBalls(ballArray)
    if see_chunks:
        chunks.draw(screen)
        for ball in ballArray:
            chunks.draw_surroundingObjects(ball.pos, screen)
        chunks.seeOccupiedChunks(screen)

        chunks.highlightChunk((255, 0, 0), chunks.get_chunkIndex(Vec2(pygame.mouse.get_pos())), screen)
    # for ball in ballArray:
        # chunks.get_surroundingObjects(ball.pos, screen)

collisionNum = 0

def ballCollision(ballArray):
    global collisionNum
    collisionNum = 0
    for ball in ballArray:
        if ball.pos.y-ball.radius < 0:
            continue


        surroundingBalls = chunks.get_surroundingObjects(ball.pos)
        n = 1
        for ball2 in surroundingBalls:
            if ball == ball2:
                continue
            collisionNum += 1
            ball.ballCollisionPhysics(ball2)





while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
    screen.fill((30, 30, 30))


    delta_stuff()
    keyinputs(ballArray)

    keys = pygame.key.get_pressed()



    if not paused:

        pos = chunks.get_chunkIndex(Vec2(pygame.mouse.get_pos()))


        chunking(ballArray)


        for ball in ballArray:
            ball.update(delta)


        st = time.time()
        ballCollision(ballArray)
        et = time.time()

    for ball in ballArray:
        ball.draw(screen)

    balls_onscreen = 0
    total_energy = 0


    array = []
    for ball in ballArray:
        if ball.pos.y > 0:
            balls_onscreen += 1
            total_energy += ball.vec.mag
        array.append(ball.pos.position)

    # f.write(str(array)+",")

    screen.blit(font.render("FPS:" + str(round(clock.get_fps())), 1, (255, 255, 255)), (0, 0))
    screen.blit(font.render("Balls:" + str(len(ballArray)) + "|" +str(settings.BALLSIZE)+"px|"+str(round(settings.BALLELASTICITY,2))+"e|"+"AngleCalc:"+str(settings.ANGLECALCULATIONS), 1, (255, 255, 255)), (0, 15))
    screen.blit(font.render("General Delta:" + str(round(generalDelta,100)), 1, (255, 255, 255)), (0, 30))
    screen.blit(font.render("Coll Time:" + str(round((et-st)*1000))+"ms", 1, (255, 255, 255)), (0, 45))
    screen.blit(font.render("Checks Num:" + str(collisionNum), 1, (255, 255, 255)), (0, 60))
    screen.blit(font.render("Gravity" + str(round(settings.GRAVITYVEC,1).position), 1, (255, 255, 255)), (0, 75))
    # screen.blit(font.render("Total Energy:" + str(round(total_energy)), 1, (255, 255, 255)), (0, 60))

    clock.tick(60)


    pygame.display.flip()

























