"""
This file contains the Game class, which manipulates elements
of the grid. Run this file to initialize the game.
"""

import pygame
import objects
from objects import grid
from constants import Colors, Events
from config import CONSOLE_CONFIG
from libs.pygame_console.game_console import Console


class Game:
    """
    Main class which manipulates all game events
    """

    def __init__(self, level=1, screen_width=1200, screen_height=900):
        """
        :param screen_width: Screen width in pixels
        :param screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.top_taskbar_h = 180
        self.running = True

        pygame.init()
        pygame.display.set_caption("Pytrusted")
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont('couriernew', 30)

        self.taskbar_top_surf = pygame.Surface((self.screen_width, self.top_taskbar_h))
        self.taskbar_top_surf.fill(Colors.MD_GRAY)
        self.game_surf = pygame.Surface((600, 600))
        self.game_surf.fill(Colors.MD_GRAY)
        self.code_surf = pygame.Surface((600, 600))
        self.code_surf.fill(Colors.BLACK)

        self.window.blit(self.game_surf, (0, self.top_taskbar_h))
        self.window.blit(self.code_surf, (600, self.top_taskbar_h))

        self.inv_box = pygame.Surface((250, 70))
        self.inv_box.fill(Colors.WHITE)
        self.item_boxes = [pygame.Surface((50, 50)) for _ in range(4)]

        self.display_inventory([None for _ in range(len(self.item_boxes))])

        self.taskbar_top_surf.blit(self.inv_box, (30, 70))
        inv_text = self.font.render("self.inventory", True, Colors.WHITE)
        self.taskbar_top_surf.blit(inv_text, (30, 30))
        self.window.blit(self.taskbar_top_surf, (0, 0))

        self.console = Console(grid, 600, CONSOLE_CONFIG)
        # self.console.toggle()

        self.level = level

    def draw(self):
        """
        Draws the object symbols and blits them onto the window
        :return: None
        """
        self.font = pygame.font.SysFont('cambria', 30)
        for x in range(grid.width):
            for y in range(grid.height):
                obj = grid.grid[x][y]
                sym = obj.symbol if obj is not None else "."
                col = obj.color if obj is not None else Colors.ORANGE
                char = self.font.render(sym, True, col)
                char_rect = char.get_rect()
                char_rect.center = (x * grid.field_width + grid.margin_left,
                                    y * grid.field_height + grid.margin_top)
                self.game_surf.blit(char, char_rect)

        self.window.blit(self.game_surf, (0, self.top_taskbar_h))

    @staticmethod
    def disable_console():
        """
        Closes the console
        :return: None
        """
        e = pygame.event.Event(Events.CONSOLE_TOGGLE, on=False)
        e.dict['on'] = False
        pygame.event.post(e)

    @staticmethod
    def clear_grid():
        """
        Places an Empty() object on each square
        :return: None
        """
        for x in range(grid.width):
            for y in range(grid.height):
                grid.place_object_f((x, y), objects.Empty())

    def display_inventory(self, inv_):
        """
        Displays symbols of items from the player's inventory on the
        top of the screen
        :param inv_: Inventory of the player
        :type inv_: list
        :return: None
        """
        inv = inv_ + [None for _ in range(len(self.item_boxes) - len(inv_))]
        self.font = pygame.font.SysFont('couriernew', 30)
        self.inv_box.fill(Colors.WHITE)
        for i, box in enumerate(self.item_boxes):
            s = inv[i].symbol if inv[i] is not None else "-"
            c = inv[i].color if inv[i] is not None else Colors.WHITE
            sym = self.font.render(s, True, c)
            box.fill(Colors.D_GRAY)
            box.blit(sym, (15, 10))
            self.inv_box.blit(box, (10 + 60 * i, 10))
        self.taskbar_top_surf.blit(self.inv_box, (30, 70))
        self.window.blit(self.taskbar_top_surf, (0, 0))

    @staticmethod
    def place_from_map(_map, code):
        """
        Places objects onto the grid using a string pattern
        :param _map: A tuple of strings of equal length. Each character represents
        an object, each string represents a row.
        :type _map: tuple
        :param code: A dictionary of {char: Object()}, {char: prototype} or {char: name} pairs, which
        defines the meaning of the characters in _map strings. If {char: Object()}
        is passed, the char should only be used once. {char: name} places an object
        with a given name. {char: prototype} places a new default instance of an object
        :type code: dict
        :return: None
        """
        for y, row in enumerate(_map):
            for x, char in enumerate(row):
                ref = code[char]
                obj = None
                if isinstance(ref, str):
                    obj = objects.__dict__[ref]()
                elif isinstance(ref, type):
                    obj = ref()
                else:
                    obj = ref
                grid.place_object((x, y), obj)

    def tick(self, delay):
        """
        Main loop function which handles PyGame Events, processes objects on the
        grid, and displays the symbols on the screen.
        :param delay: Duration of one tick
        :return: None
        """
        pygame.time.delay(delay)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                print(event.key)
                p = grid.get_player()
                p.behavior(event.key)
                self.display_inventory(p.inventory)

                for obj_coords in grid.get_dynamic_objects():
                    grid.get(obj_coords).behavior(event.key)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F1:
                    self.console.toggle()

                if event.key == pygame.K_q:
                    getattr(self, "level" + str(self.level))()

            if event.type == Events.LEVEL:
                getattr(self, event.dict['target'])()

            if event.type == Events.CONSOLE_TOGGLE:
                if event.dict['on']:
                    self.console.enabled = True
                else:
                    self.disable_console()

        self.game_surf.fill(Colors.BLACK)
        self.draw()

        self.console.update(events)
        self.console.show(self.code_surf)
        self.window.blit(self.code_surf, (600, self.top_taskbar_h))
        pygame.display.update()

    def level1(self):
        """
        Level 1
        :return: None
        """
        self.level = 1
        self.clear_grid()
        self.disable_console()
        self.place_from_map(("..........",
                             ".########.",
                             ".#p.....#.",
                             ".#.....k#.",
                             ".####d###.",
                             ".#......#.",
                             ".#.....e#.",
                             ".########.",
                             ".........."),
                            {
                                ".": 'Empty',
                                "#": 'Wall',
                                "p": objects.Player(),
                                "k": objects.SmallKey(),
                                "d": objects.KeyDoor(key_name="small_key"),
                                "e": objects.Exit(target_level="level2")
                            })

    def level2(self):
        """
        Level 2
        :return: None
        """
        self.level = 2
        self.clear_grid()
        self.place_from_map(("..........",
                             ".########.",
                             ".#.p....#.",
                             ".#....k.#.",
                             ".#....m.#.",
                             ".#....l.#.",
                             ".###d####.",
                             ".#......#.",
                             ".#....e.#.",
                             ".########.",
                             ".........."),
                            {
                                ".": 'Empty',
                                "#": 'Wall',
                                "p": 'Player',
                                "k": objects.SmallKey(color=(255, 0, 0)),
                                "l": objects.SmallKey(color=(0, 255, 0)),
                                "m": objects.SmallKey(color=(0, 0, 255)),
                                "d": objects.ColoredDoor(color=(0, 0, 255)),
                                "e": objects.Exit(target_level="level3")
                            })

    def level3(self):
        """
        Level 3
        :return: None
        """
        self.level = 3
        self.clear_grid()
        self.place_from_map(("..........",
                             ".########.",
                             ".#.p....#.",
                             ".#....k.#.",
                             ".#....m.#.",
                             ".#....l.#.",
                             ".###d####.",
                             ".#......#.",
                             ".#....e.#.",
                             ".########.",
                             ".........."),
                            {
                                ".": 'Empty',
                                "#": 'Wall',
                                "p": 'Player',
                                "k": objects.SmallKey(color=Colors.YELLOW),
                                "l": objects.SmallKey(color=Colors.SCARLET),
                                "m": objects.SmallKey(color=Colors.NAVY),
                                "d": objects.ChangingColoredDoor(
                                    color_queue=(Colors.RED, Colors.AQUA,
                                                 Colors.ORANGE, Colors.MAGENTA,
                                                 Colors.YELLOW, Colors.BLUE)),
                                "e": objects.Exit(target_level="level4")
                            })

    def level4(self):
        """
        Level 4
        :return: None
        """
        self.level = 4
        self.clear_grid()
        self.place_from_map(("....................",
                             ".##################.",
                             ".#.............x.e#.",
                             ".#.p...........#..#.",
                             ".#.............####.",
                             ".#...########.....#.",
                             ".#...D......#.....#.",
                             ".#.#######..#.....#.",
                             ".#.#.....#..#.....#.",
                             ".#.#..#..#..#.....#.",
                             ".#.#..#..#..#.....#.",
                             ".#.#..#..#..#.....#.",
                             ".#.#..#.....#.....#.",
                             ".#.#..#######.....#.",
                             ".###..#...........#.",
                             ".#.#..#############.",
                             ".#.#...........d..#.",
                             ".#.#..............#.",
                             ".##################.",
                             "...................."),
                            {
                                ".": "Empty",
                                "#": "Wall",
                                "p": "Player",
                                "x": objects.ColoredDoor(color=Colors.ORANGE),
                                "e": objects.Exit(target_level="level5"),
                                "d": objects.AllyDrone(inventory=[objects.SmallKey(
                                    color=Colors.ORANGE)]),
                                "D": objects.ColoredDoor(color=Colors.ORANGE)
                            })

    def level5(self):
        """
        Level 5
        :return: None
        """
        self.level = 5
        self.clear_grid()
        self.place_from_map(("..........",
                             ".########.",
                             ".#p.c...#.",
                             ".#.....k#.",
                             ".####d###.",
                             ".#......#.",
                             ".#.....e#.",
                             ".########.",
                             ".........."),
                            {
                                ".": 'Empty',
                                "#": 'Wall',
                                "p": objects.Player(),
                                "k": objects.SmallKey(color=Colors.AQUA, hackable=['color']),
                                "d": objects.ColoredDoor(color=Colors.GREEN),
                                "e": objects.Exit(target_level="level6"),
                                "c": objects.Computer()
                            })

    def level6(self):
        """
        Level 6
        :return: None
        """
        self.level = 6
        self.clear_grid()
        self.place_from_map(("..........",
                             ".########.",
                             ".#p.c...#.",
                             ".#.....k#.",
                             ".####d###.",
                             ".#......#.",
                             ".#......#.",
                             ".####D###.",
                             ".#......#.",
                             ".#.....e#.",
                             ".########.",
                             ".........."),
                            {
                                ".": 'Empty',
                                "#": 'Wall',
                                "p": objects.Player(),
                                "k": objects.SmallKey(color=Colors.AQUA, hackable=[]),
                                "d": objects.ColoredDoor(color=Colors.SCARLET, hackable=['color']),
                                "D": objects.ColoredDoor(color=Colors.AQUA,
                                                         required_key_name="big_key",
                                                         hackable=['required_key_name']),
                                "e": objects.Exit(target_level="level6"),
                                "c": objects.Computer(),
                            })

    def level7(self):
        """
        Level 7
        :return: None
        """
        self.level = 7
        self.clear_grid()
        self.place_from_map((".........................",
                             ".#######################.",
                             ".#p.c..................#.",
                             ".#....M................#.",
                             ".##.####################.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#.....................#.",
                             ".#....................e#.",
                             ".#######################.",
                             "........................."),
                            {
                                ".": 'Empty',
                                "#": 'Wall',
                                "p": objects.Player(),
                                "e": objects.Exit(target_level="level6"),
                                "c": objects.Computer(),
                                "M": objects.MazeGenerator(working_area=((2, 5), (23, 17)),
                                                           path_str=((3, 5), "ddrrrrrdrrrurr"),
                                                           density=0.8,
                                                           hackable=['path_str'])
                            })


if __name__ == "__main__":
    game = Game(5)
    getattr(game, "level"+str(game.level))()
    while game.running:
        game.tick(30)
