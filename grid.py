"""
This file contains the Grid class
"""

from constants import Type


class Grid:
    """
    This class resembles the game grid and stores objects on its squares.
    Also contains methods which manipulate those objects
    """
    def __init__(self, width=10, height=10):
        """
        :param width: Width of the grid in squares
        :param height: Height of the grid in squares
        """
        self.field_width = 20
        self.field_height = 20
        self.width = width
        self.height = height

        self.margin_left = int(self.field_width / 2 + 5)
        self.margin_top = int(self.field_height/2 + 5)

        self.grid = [[None] * self.height for _ in range(self.width)]
        self.id_counter = 0

        self.level = "level1"

    def get(self, coords):
        """
        Returns the object placed on given coordinates of grid
        :param coords: (x, y) coordinates of the square
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
                for key, value in kwargs.items():
                    if getattr(obj, key) == value:
                        ret.append((x, y))
        return ret

    def find(self, **kwargs):
        """
        Returns the first found object that matches search criteria
        :param kwargs: Search parameters in attribute=value pairs.
        :return: (x, y) coordinate tuple of matching object
        """
        return self.match(**kwargs)[0]

    def swap(self, coords_1, coords_2):
        """
        Swaps objects between two given squares
        :param coords_1: Coordinates of the first square
        :param coords_2: Coordinates of the second square
        :return: None
        """
        temp = self.get(coords_1)
        self.place_object_f(coords_1, self.get(coords_2))
        self.place_object_f(coords_2, temp)

    def push(self, coords_1, coords_2):
        """
        Moves object to a target square, while managing stacking
        :param coords_1: Coordinates of the moved object
        :param coords_2: Coordinates of the target square
        :return: None
        """
        new_stack = self.get(coords_2)
        self.place_object_f(coords_2, self.get(coords_1))
        self.place_object_f(coords_1, self.get(coords_1).stacked)
        self.get(coords_2).stacked = new_stack

    def move(self, crd, direction):
        """
        Moves object to one of its adjacent squares.
        :param crd: Coordinates of the moved object
        :param direction: Direction of movement: "up", "right", "left", "down"
        :type direction: str
        :return: False if movement exceeds the grid, True otherwise.
        """
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
        return True

    def place_object(self, crd, obj, **kwargs):
        """
        Places an object at a given square. Does not replace objects flagged with
        obj.replacable = False.
        :param crd: Coordinates of the square in format (x, y).
        :type crd: tuple
        :param obj: Object to be placed.
        :param kwargs: Object attributes if obj is a prototype
        :return: False if object cannot be placed, True otherwise.
        """
        if self.get(crd) is None or self.get(crd).replacable:
            self.place_object_f(crd, obj, **kwargs)
            return True
        return False

    def place_object_f(self, crd, obj, **kwargs):
        """
        Places an object on a given square. Forces replacement of objects flagged with
        obj.replacable = False. If the object is a class prototype, places a new instance
        with kwargs instead.
        :param crd: Coordinates of the square in format (x, y)
        :type crd: tuple
        :param obj: Object to be placed
        :param kwargs: Object attributes if obj is a prototype
        :return: None
        """
        if isinstance(obj, type):
            self.grid[crd[0]][crd[1]] = obj(**kwargs)
        else:
            self.grid[crd[0]][crd[1]] = obj

    @staticmethod
    def get_adjacent(crd):
        """
        Returns the coordinates of all neighboring cells
        :param crd: Coordinates of the point
        :return: A dict of 'dir': coordinate pairs
        """
        return {
            'right': (crd[0] + 1, crd[1]),
            'left': (crd[0] - 1, crd[1]),
            'down': (crd[0], crd[1] + 1),
            'up': (crd[0], crd[1] - 1)
        }

    def get_player(self):
        """
        Returns the player object.
        :return: Player object
        """
        for col in self.grid:
            for entity in col:
                if entity.type == Type.PLAYER:
                    return entity
        return None

    def get_dynamic_objects(self):
        """
        Returns a list of (x, y) coordinates of all dynamic objects
        on the grid
        :return: A list of (x, y) coordinates of all dynamic objects on the grid
        """
        for x, col in enumerate(self.grid):
            for y, obj in enumerate(col):
                if obj.type == Type.DYNAMIC:
                    yield x, y
