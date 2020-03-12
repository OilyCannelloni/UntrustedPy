from objects import *
from constants import CONSOLE_CONFIG
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
        self.taskbar_top_surf.fill((20, 20, 20))

        self.game_surf = pygame.Surface((600, 600))
        self.game_surf.fill((30, 30, 30))

        self.code_surf = pygame.Surface((600, 600))
        self.code_surf.fill((0, 0, 0))

        self.window.blit(self.game_surf, (0, self.top_taskbar_h))
        self.window.blit(self.code_surf, (600, self.top_taskbar_h))

        self.inv_box = pygame.Surface((250, 70))
        self.inv_box.fill((255, 255, 255))
        self.item_boxes = [pygame.Surface((50, 50)) for _ in range(4)]

        self.display_inventory([None for _ in range(len(self.item_boxes))])

        self.taskbar_top_surf.blit(self.inv_box, (30, 70))
        inv_text = self.font.render("self.inventory", True, (255, 255, 255))
        self.taskbar_top_surf.blit(inv_text, (30, 30))

        self.window.blit(self.taskbar_top_surf, (0, 0))

        self.level = None

        self.console = Console(grid, 600, CONSOLE_CONFIG)
        self.console.toggle()

    def display_inventory(self, inv_):
        inv = inv_ + [None for _ in range(len(self.item_boxes) - len(inv_))]
        self.font = pygame.font.SysFont('couriernew', 30)
        self.inv_box.fill((255, 255, 255))
        for i in range(len(self.item_boxes)):
            s = inv[i].symbol if inv[i] is not None else "-"
            c = inv[i].color if inv[i] is not None else (255, 255, 255)
            sym = self.font.render(s, True, c)
            self.item_boxes[i].fill((10, 10, 10))
            self.item_boxes[i].blit(sym, (15, 10))
            self.inv_box.blit(self.item_boxes[i], (10 + 60 * i, 10))
        self.taskbar_top_surf.blit(self.inv_box, (30, 70))
        self.window.blit(self.taskbar_top_surf, (0, 0))

    def draw(self):
        self.font = pygame.font.SysFont('cambriacambriamath', 20)
        for x in range(grid.width):
            for y in range(grid.height):
                obj = grid.grid[x][y]
                sym = obj.symbol if obj is not None else "."
                col = obj.color if obj is not None else (255, 100, 0)
                char = self.font.render(sym, True, col)
                char_rect = char.get_rect()
                char_rect.center = (x*grid.field_width+grid.MARGIN_LEFT, y*grid.field_height+grid.MARGIN_TOP)
                self.game_surf.blit(char, char_rect)

        self.window.blit(self.game_surf, (0, self.top_taskbar_h))

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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F1:
                    self.console.toggle()

        self.game_surf.fill((0, 0, 0))
        self.draw()

        self.console.update(events)
        self.console.show(self.code_surf)
        self.window.blit(self.code_surf, (600, self.top_taskbar_h))
        pygame.display.update()


    @staticmethod
    def clear_grid():
        for x in range(grid.width):
            for y in range(grid.height):
                grid.place_object(x, y, Empty())


    def level1(self):
        self.clear_grid()
        grid.place_from_map(("....................",
                             ".##################.",
                             ".#................#.",
                             ".#................#.",
                             ".#....p......k....#.",
                             ".#................#.",
                             ".########d#########.",
                             ".#................#.",
                             ".#................#.",
                             ".#................#.",
                             ".#................#.",
                             ".#................#.",
                             ".#................#.",
                             ".#................#.",
                             ".#................#.",
                             ".#................#.",
                             ".#................#.",
                             ".#................#.",
                             ".##################.",
                             "...................."
                             ), {
            ".": Empty(),
            "#": Wall(),
            "p": Player(),
            "k": SmallKey(),
            "d": KeyDoor("small_key")
        })


if __name__ == "__main__":
    game = Game()
    game.level1()
    while game.running:
        game.tick(30)
