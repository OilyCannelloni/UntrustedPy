from constants import *
from grid import Grid
import pygame.event

grid = Grid(30, 30)


class Object:
    def __init__(self):
        self.id = grid.id_counter  # A unique id for each object
        grid.id_counter += 1
        self.coords = (None, None)
        self.stacked = None
        self.replacable = False
        self.hackable = []

    def set(self, **kwargs):
        for arg, val in kwargs.items():
            setattr(self, arg, val)

    def behavior(self, keys_down):
        """
        This function is executed each game tick for each dynamic object
        :param keys_down: Pressed keys detected by PyGame
        :return:
        """
        pass

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

    def move(self, d):
        """
        Moves the object in target direction
        :param d: Direction "up", "right", "down", "left"
        :return: True if movement was successful, False otherwise
        """
        dest = grid.get(self.get_adjacent()[d])
        self.on_collision_with(dest)
        dest.on_collision_with(self)
        if dest.passable_for == 'all' or self.name in dest.passable_for:
            return grid.move(self.coords, d)
        return False

    def has(self, item):
        """
        Checks if an item is in the object's inventory
        :param item: Item to be checked
        :return: True if the object has the item, False othewise
        """
        pass

    def on_collision_with(self, collider):
        """
        Triggers when the object is moved into another, or when
        another object is moved into this object
        :param collider: Colliding object
        :return: None
        """
        pass


class Item(Object):
    def __init__(self, **kwargs):
        super().__init__()
        super().set(**kwargs)

        def on_collision_with(self, collider):
        if collider.name == "player":
            if grid.get_player().push_inventory(self):
                grid.place_object_f(self.get_coords(), Empty())


class Empty(Object):
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
        else:
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
    def __init__(self, **kwargs):
        super().__init__()
        self.name = 'wall'
        self.type = Type.STATIC
        self.symbol = '#'
        self.color = (255, 255, 255)
        self.passable_for = []
        super().set(**kwargs)


class FluxBarrier(Object):
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
    def __init__(self, **kwargs):
        super().__init__()
        self.color_queue = [Colors.WHITE, Colors.GREEN, Colors.RED]
        self.color_index = 0
        super().set(**kwargs)

    def behavior(self, keys_down):
        self.color_index = (self.color_index + 1) % len(self.color_queue)
        self.color = self.color_queue[self.color_index]


class SmallKey(Object):
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


class AllyDrone(Object):
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
        coords = self.get_coords()
        dx = coords[0] - dest_coords[0]
        dy = coords[1] - dest_coords[1]
        if abs(dx) > abs(dy):
            if coords[0] > dest_coords[0]:
                return self.move("left")
            else:
                return self.move("right")
        else:
            if coords[1] > dest_coords[1]:
                return self.move("up")
            else:
                return self.move("down")

    def behavior(self, keys_down):
        self.move_towards(grid.match(name="player")[0])

    def on_collision_with(self, collider):
        if collider.name == "player":
            coords = self.get_coords()
            if len(self.inventory) > 0:
                grid.place_object_f(coords, self.inventory[0])
            else:
                grid.place_object_f(coords, Empty)


class Computer(Object):
    def __init__(self, **kwargs):
        super().__init__()
        self.name = "computer"
        self.type = Type.STATIC
        self.symbol = "@"
        self.color = Colors.WHITE
        self.passable_for = ["player"]
        super().set(**kwargs)

        # Close the console on spawn, as the player has no computer
        pygame.event.post(pygame.event.Event(Events.CONSOLE_TOGGLE, {"on": False}))

    def on_collision_with(self, collider):
        if collider.name == "player":
            if grid.get_player().push_inventory(self):
                self.on_pickup()
                grid.place_object_f(self.get_coords(), Empty())

    @staticmethod
    def on_pickup():
        pygame.event.post(pygame.event.Event(Events.CONSOLE_TOGGLE, {"on": True}))
