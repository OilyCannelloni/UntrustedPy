import objects
from objects import grid
from constants import *
from config import CONSOLE_CONFIG
from libs.pygame_console.game_console import Console
import pygame


class Game:
    def __init__(self, screen_width=1200, screen_height=900):
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
        self.console.toggle()


    def draw(self):
        self.font = pygame.font.SysFont('cambriacambriamath', 20)
        for x in range(grid.width):
            for y in range(grid.height):
                obj = grid.grid[x][y]
                sym = obj.symbol if obj is not None else "."
                col = obj.color if obj is not None else Colors.ORANGE
                char = self.font.render(sym, True, col)
                char_rect = char.get_rect()
                char_rect.center = (x*grid.field_width+grid.MARGIN_LEFT, y*grid.field_height+grid.MARGIN_TOP)
                self.game_surf.blit(char, char_rect)

        self.window.blit(self.game_surf, (0, self.top_taskbar_h))

    @staticmethod
    def clear_grid():
        for x in range(grid.width):
            for y in range(grid.height):
                grid.place_object_f(x, y, objects.Empty())

    def display_inventory(self, inv_):
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
        for y, row in enumerate(_map):
            for x, char in enumerate(row):
                ref = code[char]
                obj = objects.__dict__[ref]() if type(ref) == str else ref
                grid.place_object(x, y, obj)

    def tick(self, delay):
        pygame.time.delay(delay)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                p = grid.get_player()
                p.behavior(event.key)
                self.display_inventory(p.inventory)

                for obj_coords in grid.get_dynamic_objects():
                    grid.get(obj_coords).behavior(event.key)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F1:
                    self.console.toggle()

            if event.type == Events.LEVEL:
                getattr(self, event.target)()

        self.game_surf.fill(Colors.BLACK)
        self.draw()

        self.console.update(events)
        self.console.show(self.code_surf)
        self.window.blit(self.code_surf, (600, self.top_taskbar_h))
        pygame.display.update()

    def level1(self):
        self.clear_grid()
        self.place_from_map(("..........",
                             ".########.",
                             ".#p.....#.",
                             ".#.....k#.",
                             ".####d###.",
                             ".#......#.",
                             ".#.....e#.",
                             ".########.",
                             ".........."), {
            ".": 'Empty',
            "#": 'Wall',
            "p": objects.Player(),
            "k": objects.SmallKey(),
            "d": objects.KeyDoor("small_key"),
            "e": objects.Exit("level2")
        })

    def level2(self):
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
                             ".........."), {
            ".": 'Empty',
            "#": 'Wall',
            "p": 'Player',
            "k": objects.SmallKey(color=(255, 0, 0)),
            "l": objects.SmallKey(color=(0, 255, 0)),
            "m": objects.SmallKey(color=(0, 0, 255)),
            "d": objects.ColoredDoor(color=(0, 0, 255)),
            "e": objects.Exit("level3")
        })

    def level3(self):
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
                             ".........."), {
                                ".": 'Empty',
                                "#": 'Wall',
                                "p": 'Player',
                                "k": objects.SmallKey(color=Colors.YELLOW),
                                "l": objects.SmallKey(color=Colors.SCARLET),
                                "m": objects.SmallKey(color=Colors.NAVY),
                                "d": objects.ChangingColoredDoor((Colors.RED, Colors.AQUA, Colors.ORANGE,
                                                                  Colors.MAGENTA, Colors.YELLOW, Colors.BLUE)),
                                "e": objects.Exit("level4")
                            })

    def level4(self):
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
                             "...................."), {
            ".": "Empty",
            "#": "Wall",
            "p": "Player",
            "x": objects.ColoredDoor(Colors.ORANGE),
            "e": objects.Exit("level1"),
            "d": objects.AllyDrone(inv=[objects.SmallKey(Colors.ORANGE)]),
            "D": objects.ColoredDoor(Colors.ORANGE)
        })


if __name__ == "__main__":
    game = Game()
    game.level4()
    while game.running:
        game.tick(30)
