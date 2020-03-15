"""
This file contains definitions of all objects used in the game
"""
import pygame.event
from constants import *
from grid import Grid


grid = Grid(30, 30)


class Object:
    """
    This class contains methods characteristic for every object
    """
    def __init__(self):
        self.id = grid.id_counter  # A unique id for each object
        grid.id_counter += 1
        self.coords = (None, None)
        self.stacked = None
        self.replacable = False
        self.hackable = []
        self.name = None

    def set(self, **kwargs):
        """
        Sets given atributes to given values
        :param kwargs: Attribute=value pairs
        :return: None
        """
        for arg, val in kwargs.items():
            setattr(self, arg, val)

    def behavior(self, key):
        """
        This function is executed each game tick for each dynamic object
        :param key: Pressed keys detected by PyGame
        :return:
        """

    def get_coords(self):
        """
        Returns coordinates of the object
        :return: (x, y) coordinates of the object
        """
        return grid.find(id=self.id)

    def get_adjacent(self):
        """
        Returns a dictionary of coordinates of adjacent squares
        :return: dictionary of coordinates of adjacent squares
        """
        self.coords = self.get_coords()
        return {
            'right': (self.coords[0]+1, self.coords[1]),
            'left': (self.coords[0]-1, self.coords[1]),
            'down': (self.coords[0], self.coords[1]+1),
            'up': (self.coords[0], self.coords[1]-1)
        }

    def move(self, direction):
        """
        Moves the object in target direction
        :param direction: Direction "up", "right", "down", "left"
        :return: True if movement was successful, False otherwise
        """
        dest = grid.get(self.get_adjacent()[direction])
        self.on_collision_with(dest)
        dest.on_collision_with(self)
        if dest.passable_for == 'all' or self.name in dest.passable_for:
            return grid.move(self.coords, direction)
        return False

    def has(self, item):
        """
        Checks if an item is in the object's inventory
        :param item: Item to be checked
        :return: True if the object has the item, False othewise
        """

    def on_collision_with(self, collider):
        """
        Triggers when the object is moved into another, or when
        another object is moved into this object
        :param collider: Colliding object
        :return: None
        """


class Item(Object):
    """
    This class defines methods for pickable items
    """
    def __init__(self, **kwargs):
        super().__init__()
        super().set(**kwargs)

    def on_collision_with(self, collider):
        if collider.name == "player":
            if grid.get_player().push_inventory(self):
                grid.place_object_f(self.get_coords(), Empty())


class Empty(Object):
    """
    Idle object passable for everything
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'empty'
        self.type = Type.STATIC
        self.passable_for = 'all'
        self.symbol = " "
        self.color = (255, 255, 255)
        self.replacable = True
        super().set(**kwargs)


class Player(Object):
    """
    The object which is controlled by the player
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'player'
        self.type = Type.PLAYER
        self.symbol = '▲'
        self.looking_at = None
        self.color = (0, 255, 100)
        self.inventory = []
        self.max_inventory_size = 3
        self.stacked = Empty()
        self.passable_for = []
        super().set(**kwargs)

    def push_inventory(self, item):
        """
        Places an object in player's inventory
        :param item: Object to be placed
        :return: True if successful, False otherwise
        """
        if len(self.inventory) < self.max_inventory_size:
            self.inventory.append(item)
            return True
        print("inventory full!")
        return False

    def has(self, item):
        return item in [it.name for it in self.inventory]

    def behavior(self, key):
        dirs = {
            Keys.LEFT: ("left", "◀"),
            Keys.RIGHT: ("right", "▶"),
            Keys.UP: ("up", "▲"),
            Keys.DOWN: ("down", "▼")
        }
        if key in dirs.keys():
            self.move(dirs[key][0])
            self.symbol = dirs[key][1]
            self.looking_at = self.get_adjacent()[dirs[key][0]]


class Wall(Object):
    """
    Basic impassable object
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'wall'
        self.type = Type.STATIC
        self.symbol = '#'
        self.color = (255, 255, 255)
        self.passable_for = []
        super().set(**kwargs)


class FluxBarrier(Object):
    """
    Object which removes given items from all entities
    which pass through it
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "flux_barrier"
        self.type = Type.DYNAMIC
        self.symbol = "⍂"
        self.color = (200, 100, 255)
        self.passable_for = "all"
        self.items_removed = []
        super().set(**kwargs)

    def on_collision_with(self, collider):
        collider.inventory = [item for item in collider.inventory if item not in self.items_removed]


class Exit(Object):
    """
    Object which generates another map (level) after
    collision with player
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "exit"
        self.type = Type.DYNAMIC
        self.symbol = "⌼"
        self.color = (100, 100, 255)
        self.passable_for = ["player"]
        self.target_level = "level1"
        super().set(**kwargs)

    def on_collision_with(self, collider):
        if collider.name == "player":
            pygame.event.post(pygame.event.Event(Events.LEVEL, {"target": self.target_level}))


class KeyDoor(Object):
    """
    Object passable for all entities having an item
    with a given name in their inventory
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "key_door"
        self.type = Type.DYNAMIC
        self.symbol = "⌻"
        self.color = (255, 200, 100)
        self.passable_for = []
        self.key_name = "small_key"
        super().set(**kwargs)

    def on_collision_with(self, collider):
        if collider.name == "player" and collider.has(self.key_name):
            self.passable_for.append("player")
        else:
            self.passable_for = []


class ColoredDoor(Object):
    """
    Object passsable for all entities that have an item with given
    name and color in their inventory
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "colored_door"
        self.type = Type.DYNAMIC
        self.symbol = "⌻"
        self.color = (255, 0, 0)
        self.passable_for = set()
        self.required_key_name = "small_key"
        super().set(**kwargs)

    def on_collision_with(self, collider):
        for item in collider.inventory:
            if item.name == self.required_key_name and item.color == self.color:
                self.passable_for.add(collider.name)
                return
        self.passable_for.discard(collider.name)


class ChangingColoredDoor(ColoredDoor):
    """
    ColoredDoor which change color every tick along
    a given queue
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.color_queue = [Colors.WHITE, Colors.GREEN, Colors.RED]
        self.color_index = 0
        super().set(**kwargs)

    def behavior(self, key):
        self.color_index = (self.color_index + 1) % len(self.color_queue)
        self.color = self.color_queue[self.color_index]


class SmallKey(Object):
    """
    A key used to open doors
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "small_key"
        self.type = Type.STATIC
        self.symbol = 'k'
        self.passable_for = "all"
        self.color = Colors.WHITE
        super().set(**kwargs)

    def on_collision_with(self, collider):
        if collider.name == "player":
            if grid.get_player().push_inventory(self):
                grid.place_object_f(self.get_coords(), Empty())


class BigKey(Object):
    """
    A key used to open doors
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "big_key"
        self.type = Type.STATIC
        self.symbol = 'K'
        self.passable_for = "all"
        self.color = Colors.WHITE
        super().set(**kwargs)

    def on_collision_with(self, collider):
        if collider.name == "player":
            if grid.get_player().push_inventory(self):
                grid.place_object_f(self.get_coords(), Empty())


class AllyDrone(Object):
    """
    An object which moves towards the player on each tick
    and has an inventory for items. It drops the items upon
    collision with player
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "ally_drone"
        self.type = Type.DYNAMIC
        self.symbol = "⌘"
        self.color = Colors.GREEN
        self.stacked = Empty()
        self.inventory = []
        self.passable_for = ["player"]
        super().set(**kwargs)

    def move_towards(self, dest_coords):
        """
        Moves in the direction, which makes the object travel the most distance
        towards the target
        :param dest_coords: Target (x, y) coordinates
        :return:
        """
        coordinates = self.get_coords()
        delta_x = coordinates[0] - dest_coords[0]
        delta_y = coordinates[1] - dest_coords[1]
        if abs(delta_x) > abs(delta_y):
            if coordinates[0] > dest_coords[0]:
                return self.move("left")
            return self.move("right")
        if coordinates[1] > dest_coords[1]:
            return self.move("up")
        return self.move("down")

    def behavior(self, key):
        self.move_towards(grid.match(name="player")[0])

    def on_collision_with(self, collider):
        if collider.name == "player":
            coords = self.get_coords()
            if len(self.inventory) > 0:
                grid.place_object_f(coords, self.inventory[0])
            else:
                grid.place_object_f(coords, Empty)


class Computer(Object):
    """
    Object which, after being picked up, enables
    the player to use the console
    """
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "computer"
        self.type = Type.STATIC
        self.symbol = "@"
        self.color = Colors.WHITE
        self.passable_for = ["player"]
        super().set(**kwargs)

        # Close the console on spawn, as the player has no computer
        # pygame.event.post(pygame.event.Event(Events.CONSOLE_TOGGLE, {"on": False}))

    def on_collision_with(self, collider):
        if collider.name == "player":
            if grid.get_player().push_inventory(self):
                self.on_pickup()
                grid.place_object_f(self.get_coords(), Empty())

    @staticmethod
    def on_pickup():
        """
        Triggers when the item is picked up by the player
        :return: None
        """
        pygame.event.post(pygame.event.Event(Events.CONSOLE_TOGGLE, {"on": True}))


class MazeGenerator(Object):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "maze_generator"
        self.type = Type.DYNAMIC
        self.symbol = "&"
        self.color = Colors.ORANGE
        self.passable_for = []
        self.working_area = None
        self.maze_block_name = "Wall"
        super().set(**kwargs)

    def behavior(self, key):
        for x in range(self.working_area[0][0], self.working_area[1][0]):
            for y in range(self.working_area[0][1], self.working_area[1][1]):
                obj = grid.get((x, y))
                if obj.name == "player":
                    continue
                grid.place_object_f((x, y), Wall)