import math

class Vec2():
    def __init__(self,pos):
        self.x = pos[0]
        self.y = pos[1]
        self.position = pos
        self.mag = self.get_len()

    def get_len(self):
        len = math.sqrt(self.x**2+self.y**2)

        if len == 0:
            return 0.1

        return len

    def normalise_self(self):
        self.x, self.y = self.x / self.mag, self.y / self.mag

    def normalise(self):
        return Vec2((self.x / self.mag, self.y / self.mag))

    def update(self,x,y):
        self.x = x
        self.y = y
        self.position = (x,y)
        self.mag = self.get_len()

    def __add__(self, vec2_2):
        return Vec2((self.x + vec2_2.x, self.y+vec2_2.y))

    def __sub__(self, vec2_2):
        return Vec2((self.x - vec2_2.x, self.y-vec2_2.y))

    def __mul__(self, n):
        return Vec2((self.x*n, self.y*n))

    def __neg__(self):
        return Vec2((-self.x, -self.y))

    def __round__(self, n=0):
        return Vec2((round(self.x,n), round(self.y, n)))

    def int(self):
        return Vec2((int(self.x), int(self.y)))


    def increment(self,vec):
        self.update(self.x + vec.x, self.y + vec.y)

    def decrement(self,vec):
        self.update(self.x - vec.x, self.y - vec.y)

    def perpendicular_norm(self):
        return Vec2((-self.y, self.x)).normalise()

    def dot(self, vector):
        return self.x*vector.x+self.y*vector.y

    def overlap(self, vector):
        return self.dot(vector)/vector.mag
