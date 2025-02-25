from pygame import image, display, event, font, transform, Rect

class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.main_menu_image = image.load('assets/menus/main_menu.png')
        self.character_select_image = image.load('assets/menus/character_select.png')
        self.font = font.Font(None, 74)
        self.title_text = self.font.render('2D Fighting Game', True, (255, 255, 255))
        self.start_text = self.font.render('Press Enter to Start', True, (255, 255, 255))
        self.quit_text = self.font.render('Press Q to Quit', True, (255, 255, 255))

    def show_main_menu(self):
        self.screen.blit(self.main_menu_image, (0, 0))
        self.screen.blit(self.title_text, (100, 50))
        self.screen.blit(self.start_text, (100, 200))
        self.screen.blit(self.quit_text, (100, 300))
        display.flip()

        while True:
            for e in event.get():
                if e.type == event.QUIT:
                    return 'quit'
                if e.type == event.KEYDOWN:
                    if e.key == event.K_RETURN:
                        return 'start'
                    if e.key == event.K_q:
                        return 'quit'

    def show_character_select(self):
        self.screen.blit(self.character_select_image, (0, 0))
        display.flip()

        while True:
            for e in event.get():
                if e.type == event.QUIT:
                    return 'quit'
                if e.type == event.KEYDOWN:
                    if e.key == event.K_ESCAPE:
                        return 'main_menu'