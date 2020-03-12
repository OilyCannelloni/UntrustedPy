from constants import keys
from grid import Grid

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
        else:
            print("cant move")

    def has(self, item):
        pass

    def on_collision_with(self, collider):
        pass


class Empty(Object):
    def __init__(self):
        super().__init__()
        self.name = 'empty'
        self.type = 'static'
        self.passable_for = 'all'
        self.symbol = " "
        self.color = (255, 255, 255)
        self.replacable = True


class Player(Object):
    def __init__(self):
        super().__init__()
        self.name = 'player'
        self.type = 'player'
        self.symbol = '@'
        self.color = (0, 255, 100)
        self.inventory = []
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
        elif key == keys.RIGHT:
            self.move("left")
        elif key == keys.DOWN:
            self.move("down")
        elif key == keys.UP:
            self.move("up")


class Wall(Object):
    def __init__(self):
        super().__init__()
        self.name = 'wall'
        self.type = 'static'
        self.symbol = '#'
        self.color = (255, 255, 255)
        self.passable_for = []


class KeyDoor(Object):
    def __init__(self, key_name):
        super().__init__()
        self.name = "key_door"
        self.type = "dynamic"
        self.symbol = "⌻"
        self.color = (255, 200, 100)
        self.passable_for = []
        self.required_key_name = key_name

    def on_collision_with(self, collider):
        if collider.name == "player" and collider.has(self.required_key_name):
            self.passable_for.append("player")
        else:
            self.passable_for = []


class SmallKey(Object):
    def __init__(self):
        super().__init__()
        self.name = "small_key"
        self.type = "item"
        self.symbol = 'k'
        self.color = (255, 50, 50)
        self.passable_for = "all"

    def on_collision_with(self, collider):
        if collider.name == "player":
            if grid.get_player().push_inventory(self):
                grid.place_object_f(*self.get_coords(), Empty())





