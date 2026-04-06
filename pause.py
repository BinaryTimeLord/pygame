import pygame
import utilities
import state
import game

class pause(state.State):
    def __init__(self,game):
        state.State.__init__(self, game)
        self.pause_text = self.game.small_font.render("*pause*",False,(0,0,0))
        self.pause_text_rect = self.pause_text.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 2))
    def update(self):
        if self.game.actions["start"] and self.game.pausecooldown <= 0:
            self.game.pausecooldown = 20
            self.game.prev_state.enter()
            self.exit()
    def render(self):
        self.game.prev_state.render()
        self.game.screen.blit(self.pause_text,self.pause_text_rect)