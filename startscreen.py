import os.path

import pygame
import state
import random

import utilities


class StartScreen(state.State):
    def __init__(self, game):
        state.State.__init__(self, game)
        self.background = utilities.loadImage(os.path.join("data","images"),"skygrad.png")
        self.grassimage = utilities.loadImage(os.path.join("data","images"),"grass.png",1)
        self.grassshadow = utilities.loadImage(os.path.join("data","images"),"grasshadow.png" ,1)
        self.starttext = self.game.small_font.render("press Start", True, (255,255,255))
        self.starttextrect = self.starttext.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 2 - 30))
        self.titletext = self.game.large_font.render("Moes Adventure", True, (255, 255, 255))
        self.titletext2 = self.game.large_font.render("Moes Adventure", True, (25, 25, 25))
        self.titletextrect = self.titletext.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 4))
        self.musicstart = False

    def update(self):
        if self.musicstart == False:
            pygame.mixer.music.load(os.path.join("data", "music", "moesstartscreen.ogg"))
            pygame.mixer.music.play(-1,0,10)
            self.musicstart = True
        if self.game.actions["start"]:
            self.exit()
            pygame.mixer.music.stop()
            self.musicstart = False
            self.game.levelselection.enter()

    def render(self):
        rcolor = random.randint(20,60)
        tempsurf = pygame.Surface((self.game.screen_width,self.game.screen_height))
        tempsurf.blit(pygame.transform.scale(self.background,(800,640)),(0,0))
        tempsurf.blit(pygame.transform.scale(self.grassshadow, (800, 640)), (random.randint(0,5 ), 50))
        tempsurf.blit(pygame.transform.scale(self.grassimage,(800,640)),(0,55))
        tempsurf.blit(pygame.transform.scale(pygame.transform.flip(self.grassshadow,True,False), (800, 640)), (random.randint(0, 5), 75))
        tempsurf.blit(pygame.transform.scale(pygame.transform.flip(self.grassimage,True,False), (800, 640)), (0, 80))
        tempsurf.blit(self.titletext2, utilities.add_pos(self.titletextrect.topleft,(random.randint(5,10),(random.randint(5,10)))))
        tempsurf.blit(self.titletext,self.titletextrect)
        self.starttext.set_alpha(random.randint(50,150))
        tempsurf.blit(self.starttext,self.starttextrect)
        pygame.draw.rect(tempsurf,(rcolor,rcolor,rcolor),self.starttextrect.inflate(random.randint(3,10),random.randint(3,10)),1)
        tempsurf.set_colorkey((0,0,0))
        self.game.screen.blit(tempsurf,(0,0))