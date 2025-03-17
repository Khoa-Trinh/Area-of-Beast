import pygame
from game import Game
from ui.menu import Menu
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.NOFRAME)
    menu = Menu(screen)
    menu.display_menu()  # Hiển thị menu trước khi bắt đầu trò chơi

    game = Game(screen)  # Truyền màn hình đã khởi tạo vào Game
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()