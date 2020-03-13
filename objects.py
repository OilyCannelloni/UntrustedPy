from constants import *
from grid import Grid
import pygame.event

grid = Grid(30, 30)


class Object:
    def __init__(self):
        self.id = grid.id_counter
        grid.id_counter += 1
        self.coords = (None, None)
        self.name = None
        self.stacked = None
        self.replacable = False

    def behavior(self, keys_down):
        pass

    def get_coords(self):
        for x in range(grid.width):
            for y in range(grid.height):
                obj = grid.grid[x][y]
                if obj is None:
                    continue
                if obj.id == self.id:
                    return x, y

    def get_adjacent(self):
        self.coords = self.get_coords()
        return {
            'right': (self.coords[0]+1, self.coords[1]),
            'left': (self.coords[0]-1, self.coords[1]),
            'down': (self.coords[0], self.coords[1]+1),
            'up': (self.coords[0], self.coords[1]-1)
        }

    def move(self, d):
        dest = grid.get(self.get_adjacent()[d])
        dest.on_collision_with(self)
        if dest.passable_for == 'all' or self.name in dest.passable_for:
            grid.move(*self.coords, d)

    def has(self, item):
        pass

    def on_collision_with(self, collider):
        pass


class Empty(Object):
    def __init__(self):
        super().__init__()
        self.name = 'empty'
        self.type = Type.STATIC
        self.passable_for = 'all'
        self.symbol = " "
        self.color = (255, 255, 255)
        self.replacable = True


class Player(Object):
    def __init__(self, inv=None):
        super().__init__()
        self.name = 'player'
        self.type = Type.PLAYER
        self.symbol = '▲'
        self.color = (0, 255, 100)
        self.inventory = inv if inv is not None else []
        self.max_inventory_size = 3
        self.stacked = Empty()

    def push_inventory(self, item):
        if len(self.inventory) < self.max_inventory_size:
            self.inventory.append(item)
            return True
        else:
            print("inventory full!")
            return False

    def has(self, item):
        return item in [it.name for it in self.inventory]

    def behavior(self, key):
        if key == keys.LEFT:
            self.move("right")
            self.symbol = "▶"
        elif key == keys.RIGHT:
            self.move("left")
            self.symbol = "◀"
        elif key == keys.DOWN:
            self.move("down")
            self.symbol = "▼"
        elif key == keys.UP:
            self.move("up")
            self.symbol = "▲"


class Wall(Object):
    def __init__(self):
        super().__init__()
        self.name = 'wall'
        self.type = Type.STATIC
        self.symbol = '#'
        self.color = (255, 255, 255)
        self.passable_for = []


class FluxBarrier(Object):
    def __init__(self, *items_removed):
        super().__init__()
        self.name = "flux_barrier"
        self.type = Type.DYNAMIC
        self.symbol = "⍂"
        self.color = (200, 100, 255)
        self.passable_for = "all"
        self.items_removed = items_removed

    def on_collision_with(self, collider):
        collider.inventory = [item for item in collider.inventory if item not in self.items_removed]


class Exit(Object):
    def __init__(self, target_level):
        super().__init__()
        self.name = "exit"
        self.type = Type.DYNAMIC
        self.symbol = "⌼"
        self.color = (100, 100, 255)
        self.passable_for = ["player"]
        self.target_level = target_level

    def on_collision_with(self, collider):
        if collider.name == "player":
            pygame.event.post(pygame.event.Event(Events.LEVEL, {"target": self.target_level}))


class KeyDoor(Object):
    def __init__(self, key_name):
        super().__init__()
        self.name = "key_door"
        self.type = Type.DYNAMIC
        self.symbol = "⌻"
        self.color = (255, 200, 100)
        self.passable_for = []
        self.required_key_name = key_name

    def on_collision_with(self, collider):
        if collider.name == "player" and collider.has(self.required_key_name):
            self.passable_for.append("player")
        else:
            self.passable_for = []


class ColoredDoor(Object):
    def __init__(self, color=(255, 0, 0), key_name="small_key"):
        super().__init__()
        self.name = "colored_door"
        self.type = Type.DYNAMIC
        self.symbol = "⌻"
        self.color = color
        self.passable_for = set()
        self.required_key_name = key_name

    def on_collision_with(self, collider):
        for item in collider.inventory:
            if item.name == self.required_key_name and item.color == self.color:
                self.passable_for.add(collider.name)
            else:
                self.passable_for.discard(collider.name)


class ChangingColoredDoor(ColoredDoor):
    def __init__(self, color_queue):
        super().__init__()
        self.color_queue = color_queue
        self.color_index = 0

    def behavior(self, keys_down):
        self.color_index = (self.color_index + 1) % len(self.color_queue)
        self.color = self.color_queue[self.color_index]


class SmallKey(Object):
    def __init__(self, color=(255, 0, 0)):
        super().__init__()
        self.name = "small_key"
        self.type = Type.STATIC
        self.symbol = 'k'
        self.color = color
        self.passable_for = "all"

    def on_collision_with(self, collider):
        if collider.name == "player":
            if grid.get_player().push_inventory(self):
                grid.place_object_f(*self.get_coords(), Empty())


class AllyDrone(Object):
    def __init__(self, inv=None):
        super().__init__()
        self.name = "ally_drone"
        self.type = Type.DYNAMIC
        self.symbol = "⌘"
        self.color = Colors.GREEN

    def move_towards(self, dest_coords):
        coords = self.get_coords()
        dx = coords[0] - dest_coords[0]
        dy = coords[1] - dest_coords[1]
        if abs(dx) > abs(dy):
            if coords[0] > dest_coords[0]:
                self.move("left")
            else:
                self.move("right")
        else:
            if coords[1] > dest_coords[1]:
                self.move("up")
            else:
                self.move("down")

    def behavior(self, keys_down):
        self.move_towards(grid.)