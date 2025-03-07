import pygame
from game import Game
from ui.menu import Menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((320, 180))  # Sử dụng kích thước màn hình từ constants.py
    menu = Menu(screen)
    menu.display_menu()  # Hiển thị menu trước khi bắt đầu trò chơi

    game = Game()
    game.run()

    pygame.quit()


if __name__ == "__main__":
    main()