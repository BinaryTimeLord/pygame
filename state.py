class State():
    def __init__(self, game):
        self.game = game

    def update(self):
        pass

    def render(self):
        pass

    def enter(self):
        self.game.curr_state = self

    def exit(self):
        self.game.prev_state = self
