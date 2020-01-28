from objects import *
import pygame


class Game:
    def __init__(self, screen_width=1000, screen_height=1000):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.running = True

        pygame.init()
        pygame.display.set_caption("hello world")
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.font = pygame.font.SysFont('calibri', 24)


    def draw(self):
        for x in range(grid.width):
            for y in range(grid.height):
                obj = grid.grid[x][y]
                sym = obj.symbol if obj is not None else "."
                col = obj.color if obj is not None else (255, 100, 0)
                char = self.font.render(sym, True, col)
                char_rect = char.get_rect()
                char_rect.center = (x*grid.field_width+grid.MARGIN_LEFT, y*grid.field_height+grid.MARGIN_TOP)
                self.window.blit(char, char_rect)


    def tick(self, delay):
        pygame.time.delay(delay)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                p = grid.get_player()
                p.behavior(event.key)

        self.window.fill((0, 0, 0))
        self.draw()

        pygame.display.update()


    @staticmethod
    def clear_grid():
        for x in range(grid.width):
            for y in range(grid.height):
                grid.place_object(x, y, Empty())


    def level1(self):
        self.clear_grid()
        for i in range(1, grid.width-1):
            grid.place_object(i, 1, Wall())
            grid.place_object(i, grid.height - 2, Wall())
        for i in range(2, grid.height-2):
            grid.place_object(1, i, Wall())
            grid.place_object(grid.width - 2, i, Wall())

        grid.place_object(4, 4, Player())
        grid.place_object(8, 12, KeyDoor("small_key"))
        grid.place_object(10, 7, SmallKey())



if __name__ == "__main__":
    game = Game()
    game.level1()
    while game.running:
        game.tick(30)
