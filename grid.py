from constants import *


class Grid:
    """
    This class resembles the game grid and stores objects on its fields.
    Also contains methods which manipulate those objects
    """
    def __init__(self, width=10, height=10):
        """
        :param width: Width of the grid in fields
        :param height: Height of the grid in fields
        """
        # TODO add config file for those
        self.field_width = 20
        self.field_height = 20
        self.width = width
        self.height = height

        self.MARGIN_LEFT = int(self.field_width/2 + 5)
        self.MARGIN_TOP = int(self.field_height/2 + 5)

        self.grid = [[None] * self.height for _ in range(self.width)]
        self.id_counter = 0

        self.level = "level1"

    def get(self, coords):
        return self.grid[coords[0]][coords[1]]


    def swap(self, x1, y1, x2, y2):
        temp = self.grid[x2][y2]
        self.grid[x2][y2] = self.grid[x1][y1]
        self.grid[x1][y1] = temp

    def push(self, x1, y1, x2, y2):
        new_stack = self.grid[x2][y2]
        self.grid[x2][y2] = self.grid[x1][y1]
        self.grid[x1][y1] = self.grid[x1][y1].stacked
        self.grid[x2][y2].stacked = new_stack

    def move(self, x, y, d):
        if d == "right":
            if x+1 > self.width:
                return False
            self.push(x, y, x+1, y)
        elif d == "up":
            if y-1 < 0:
                return False
            self.push(x, y, x, y-1)
        elif d == "down":
            if y+1 > self.height:
                return False
            self.push(x, y, x, y+1)
        elif d == "left":
            if x-1 < 0:
                return False
            self.push(x, y, x-1, y)

    def place_object(self, x, y, obj):
        if self.grid[x][y] is None or self.grid[x][y].replacable:
            self.grid[x][y] = obj

    def place_object_f(self, x, y, obj):
        self.grid[x][y] = obj

    def get_player(self):
        for col in self.grid:
            for entity in col:
                if entity.type == Type.PLAYER:
                    return entity

    def get_dynamic_objects(self):
        for x, col in enumerate(self.grid):
            for y, obj in enumerate(col):
                if obj.type == Type.DYNAMIC:
                    yield x, y



