import os.path

import pygame
import state
import random

import utilities


class SpashScreen(state.State):
    def __init__(self, game):
        state.State.__init__(self, game)
        self.countdown = 75
        self.spashtext1 = self.game.large_font.render("A CheezeSoft Game", True, (255,255,255))
        self.spashtext1rect = self.spashtext1.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / self.countdown + 100))
        self.sound = utilities.loadSound(os.path.join("data","sounds"),"depressurize.wav")


    def update(self):
        if pygame.mixer.music.get_pos() > 0:
            pygame.mixer.music.unload()
        if self.countdown == 75:
            self.sound.play()
        self.countdown -= .4
        self.spashtext1rect = self.spashtext1.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / self.countdown * self.game.delta_time + 100))
        if self.countdown < -10:
            self.exit()
            self.game.start.enter()
    def render(self):
        tempsurf = pygame.Surface((self.game.screen_width,self.game.screen_height))
        tempsurf.blit(self.spashtext1,self.spashtext1rect)
        tempsurf.set_colorkey((0,0,0))
        tempsurf.set_alpha(random.randint(1,50))
        self.game.screen.blit(tempsurf,(0,0))

