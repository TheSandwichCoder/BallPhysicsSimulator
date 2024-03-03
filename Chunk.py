import pygame

import settings


def get_TransRect(hitbox,alpha, color, screen):
    s = pygame.Surface((hitbox[2], hitbox[3]))
    s.set_alpha(alpha)
    s.fill(color)
    screen.blit(s, (hitbox[0], hitbox[1]))

class Chunks():
    def __init__(self):
        self.x = 1280
        self.y = 720
        self.intervals = settings.BALLSIZE
        self.offset = 2  # this refers to the offset in each direction
        self.x2 = (self.x // self.intervals) + 1
        self.y2 = (self.y // self.intervals) + 1
        self.total_x = self.x2+self.offset*2
        self.total_y = self.y2+self.offset*2


        self.chunks = self.initiateChunks()

    def initiateChunks(self):

        chunk = []
        for x in range(self.x2 + self.offset * 2):
            for y in range(self.y2 + self.offset * 2):
                chunk.append([])
        return chunk

    def draw(self, screen):
        for x in range(self.x2 + self.offset * 2):
            x_value = ((x - self.offset) * self.intervals)
            pygame.draw.line(screen, (255, 255, 255), *((x_value, 0), (x_value, self.y)))


        for y in range(self.y2 + self.offset * 2):
            y_value = ((y-self.offset)*self.intervals)
            pygame.draw.line(screen,(255,255,255),*((0,y_value), (self.x, y_value)))

    def clear(self):
        for list in self.chunks:
            list.clear()

    def highlightChunk(self, color, index, screen):
        y_index = index//self.total_x - self.offset
        x_index = index%self.total_x - self.offset


        get_TransRect(pygame.Rect((x_index)*self.intervals, (y_index)*self.intervals, self.intervals, self.intervals),200,color,screen)


    def seeOccupiedChunks(self,screen):
        for index in range(len(self.chunks)):
            if len(self.chunks[index]) != 0:
                self.highlightChunk((0,255,0), index, screen)

    def get_chunkIndex(self, pos):
        x_index = pos.x//self.intervals + self.offset
        y_index = pos.y//self.intervals + self.offset

        return y_index*(self.total_x)+x_index

    def is_indexWithinBoundary(self, index):
        y_index = index // self.total_x - self.offset
        x_index = index % self.total_x - self.offset
        if self.isnot_withinBoundary_x(x_index) and self.isnot_withinBoundary_y(y_index):
            return True
        return False


    def isnot_withinBoundary_x(self, x):
        if x < 0 or x >= self.total_x:
            return True
        return False

    def isnot_withinBoundary_y(self, y):
        if y < 0 or y >= self.total_y:
            return True
        return False

    def draw_surroundingObjects(self, pos, screen):
        x_index = pos.x // self.intervals + self.offset
        y_index = pos.y // self.intervals + self.offset
        for x in range(-1, 2):
            x_index1 = x_index + x
            if self.isnot_withinBoundary_x(x_index1):
                continue
            for y in range(-1, 2):
                y_index1 = y_index + y
                if self.isnot_withinBoundary_y(y_index1):
                    continue

                global_coords = int(y_index1 * (self.total_x) + x_index1)
                self.highlightChunk((0, 255, 255), global_coords, screen)


    def get_surroundingObjects(self, pos):
        x_index = pos.x // self.intervals + self.offset
        y_index = pos.y // self.intervals + self.offset
        mainlist = []
        for x in range(-1,2):
            x_index1 = x_index+x
            if self.isnot_withinBoundary_x(x_index1):
                continue
            for y in range(-1,2):
                y_index1 = y_index + y
                if self.isnot_withinBoundary_y(y_index1):
                    continue

                global_coords = int(y_index1*(self.total_x)+x_index1)

                for ball in self.chunks[global_coords]:
                    mainlist.append(ball)

        return mainlist




    def append(self, item, index):

        self.chunks[int(index)].append(item)

    def addBalls(self, ballArray):
        for ball in ballArray:
            if ball.pos.y < 0-self.offset*self.intervals*2:
                continue

            index = self.get_chunkIndex(ball.pos)


            self.append(ball, index)
        # print("Adding Successful")



