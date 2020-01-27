from constants import keys
from grid import Grid

grid = Grid(40, 40)


class Object:
    def __init__(self):
        self.id = grid.id_counter
        grid.id_counter += 1
        self.coords = (None, None)
        self.name = None


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
        if dest.passable_for == 'all' or self.name in dest.passable_for:
            grid.move(*self.coords, d)
        else:
            print("cant move")


class Empty(Object):
    def __init__(self):
        super().__init__()
        self.name = 'empty'
        self.type = 'static'
        self.passable_for = 'all'
        self.symbol = " "
        self.color = (255, 255, 255)

    def behavior(self, keys_down):
        pass


class Player(Object):
    def __init__(self):
        super().__init__()
        self.name = 'player'
        self.type = 'player'
        self.symbol = '@'
        self.color = (0, 255, 100)

    def behavior(self, key):
        if key == keys.LEFT:
            self.move("right")
        if key == keys.RIGHT:
            self.move("left")
        if key == keys.DOWN:
            self.move("down")
        if key == keys.UP:
            self.move("up")


class Wall(Object):
    def __init__(self):
        super().__init__()
        self.name = 'wall'
        self.type = 'static'
        self.symbol = '#'
        self.color = (255, 255, 255)
        self.passable_for = []