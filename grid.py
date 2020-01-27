import pygame


class Grid:
    def __init__(self, grid_width=10, grid_height=10, screen_width=1000, screen_height=1000):
        self.running = True

        self.field_width = 24
        self.field_height = 24

        self.width = grid_width
        self.height = grid_height

        self.MARGIN_LEFT = int(self.field_width/2 + 10)
        self.MARGIN_TOP = int(self.field_height/2 + 10)

        self.grid = [[None] * self.height for _ in range(self.width)]

        self.id_counter = 0


    def get(self, coords):
        return self.grid[coords[0]][coords[1]]


    def swap(self, x1, y1, x2, y2):
        temp = self.grid[x2][y2]
        self.grid[x2][y2] = self.grid[x1][y1]
        self.grid[x1][y1] = temp


    def move(self, x, y, d):
        if d == "right":
            if x+1 > self.width:
                return False
            self.swap(x, y, x+1, y)
        elif d == "up":
            if y-1 < 0:
                return False
            self.swap(x, y, x, y-1)
        elif d == "down":
            if y+1 > self.height:
                return False
            self.swap(x, y, x, y+1)
        elif d == "left":
            if x-1 < 0:
                return False
            self.swap(x, y, x-1, y)


    def place_object(self, x, y, obj=None):
        if obj is not None:
            self.grid[x][y] = obj


    def get_player(self):
        for col in self.grid:
            for entity in col:
                if entity.type == 'player':
                    return entity

