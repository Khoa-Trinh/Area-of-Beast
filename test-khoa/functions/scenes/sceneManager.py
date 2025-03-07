class SceneManager:
    def __init__(self, game):
        self.game = game
        self.current_scene = None

    def set_scene(self, scene):
        self.current_scene = scene

    def process_events(self, events):
        if self.current_scene:
            self.current_scene.process_events(events)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def render(self, screen):
        if self.current_scene:
            self.current_scene.render(screen)
