import level
import state

class Gameover(state.State):
    def __init__(self,game):
        state.State.__init__(self,game)
        self.game = game
        self.gameover_text = self.game.large_font.render("Game over",False,(255,255,255))
        self.gameover_text_rect = self.gameover_text.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 3))
    def update(self):
        if self.game.actions["start"] and self.game.pausecooldown <= 0:
            self.game.pausecooldown = 20
            self.exit()
            self.game.spash.enter()
            self.game.spash.countdown = 75
            self.game.platformer.lives = 3
            self.game.levelselection.levellock = [0,1,1,1,1,1,1,1,1,1,1,1]
            self.game.platformer.coins = 0
            self.game.levelselection.current_sel = 0
            self.game.platformer.health = 3
            self.exit()
    def render(self):
        self.game.prev_state.render()
        self.game.screen.blit(self.gameover_text, self.gameover_text_rect)