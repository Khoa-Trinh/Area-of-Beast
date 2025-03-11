class Scene:
    def handle_events(self, events):
        raise NotImplementedError

    def update(self, dt):
        raise NotImplementedError

    def render(self):
        raise NotImplementedError

    def next_scene(self):
        self
