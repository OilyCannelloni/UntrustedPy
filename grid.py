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
        """
        Returns the object placed on given coordinates of grid
        :param coords: (x, y) coordinates of the field
        :type coords: tuple
        :return: Object on (x, y) coordinates
        """
        return self.grid[coords[0]][coords[1]]

    def match(self, **kwargs):
        """
        Returns coordinates of all objects, that match search conditions.
        A matching object must have all properties equal to those
        specified in search conditions.
        :param kwargs: Search parameters in attribute=value pairs.
        :return: A list of (x, y) coordinate tuples of matching objects
        """
        ret = []
        for x, col in enumerate(self.grid):
            for y, obj in enumerate(col):
                for k, v in kwargs.items():
                    if getattr(obj, k) == v:
                        ret.append((x, y))
        return ret

    def find(self, **kwargs):
        """
        Returns the first found object that matches search criteria
        :param kwargs: Search parameters in attribute=value pairs.
        :return: (x, y) coordinate tuple of matching object
        """
        return self.match(**kwargs)[0]

    def swap(self, c1, c2):
        temp = self.get(c1)
        self.place_object_f(c1, self.get(c2))
        self.place_object_f(c2, temp)

    def push(self, c1, c2):
        new_stack = self.get(c2)
        self.place_object_f(c2, self.get(c1))
        self.place_object_f(c1, self.get(c1).stacked)
        self.get(c2).stacked = new_stack

    def move(self, crd, direction):
        x, y = crd
        if direction == "right":
            if x+1 > self.width:
                return False
            self.push((x, y), (x+1, y))
        elif direction == "up":
            if y-1 < 0:
                return False
            self.push((x, y), (x, y-1))
        elif direction == "down":
            if y+1 > self.height:
                return False
            self.push((x, y), (x, y+1))
        elif direction == "left":
            if x-1 < 0:
                return False
            self.push((x, y), (x-1, y))

    def place_object(self, crd, obj):
        if self.get(crd) is None or self.get(crd).replacable:
            self.grid[crd[0]][crd[1]] = obj

    def place_object_f(self, crd, obj):
        self.grid[crd[0]][crd[1]] = obj

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
