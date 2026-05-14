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
        
        self.titletext = self.game.large_font.render("Moes Adventure", True, (255, 255, 255))
        self.titletext2 = self.game.large_font.render("Moes Adventure", True, (25, 25, 25))
        self.titletextrect = self.titletext.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 4))
        
        self.modes = ["Normal", "Hard"]
        self.selected_mode = 0
        
        self.starttext = self.game.small_font.render("Press Enter to Start", True, (255,255,255))
        self.starttextrect = self.starttext.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 2 - 60))
        
        self.controls_text1 = self.game.small_font.render("Controls: WASD to Move", True, (255, 255, 255))
        self.controls_text2 = self.game.small_font.render("Space to Jump, Enter to Start/Pause", True, (255, 255, 255))
        self.controls_rect1 = self.controls_text1.get_rect(center=(self.game.screen_width / 2, self.game.screen_height - 80))
        self.controls_rect2 = self.controls_text2.get_rect(center=(self.game.screen_width / 2, self.game.screen_height - 40))
        
        self.musicstart = False
        self.input_delay = 0

    def update(self):
        if self.musicstart == False:
            pygame.mixer.music.load(os.path.join("data", "music", "moesstartscreen.ogg"))
            pygame.mixer.music.play(-1,0,10)
            self.musicstart = True
            
        if self.input_delay > 0:
            self.input_delay -= 1

        if self.game.actions["down"] and self.input_delay == 0:
            self.selected_mode = (self.selected_mode + 1) % len(self.modes)
            self.input_delay = 15
        elif self.game.actions["up"] and self.input_delay == 0:
            self.selected_mode = (self.selected_mode - 1) % len(self.modes)
            self.input_delay = 15

        if self.game.actions["start"] and self.input_delay == 0:
            self.game.mode = self.modes[self.selected_mode]
            # Guys ito yung nagse-set ng buhay: 1 life/health sa Hard, 3 lives/5 health sa Normal
            if self.game.mode == "Hard":
                self.game.platformer.health = 1
                self.game.platformer.lives = 1
            else:
                self.game.platformer.health = 5
                self.game.platformer.lives = 3
            self.exit()
            pygame.mixer.music.stop()
            self.musicstart = False
            self.game.levelselection.enter()

    def render(self):
        tempsurf = pygame.Surface((self.game.screen_width,self.game.screen_height))
        tempsurf.blit(pygame.transform.scale(self.background,(800,640)),(0,0))
        tempsurf.blit(pygame.transform.scale(self.grassshadow, (800, 640)), (random.randint(0,5 ), 50))
        tempsurf.blit(pygame.transform.scale(self.grassimage,(800,640)),(0,55))
        tempsurf.blit(pygame.transform.scale(pygame.transform.flip(self.grassshadow,True,False), (800, 640)), (random.randint(0, 5), 75))
        tempsurf.blit(pygame.transform.scale(pygame.transform.flip(self.grassimage,True,False), (800, 640)), (0, 80))
        
        tempsurf.blit(self.titletext2, utilities.add_pos(self.titletextrect.topleft,(random.randint(5,10),(random.randint(5,10)))))
        tempsurf.blit(self.titletext,self.titletextrect)
        
        self.starttext.set_alpha(random.randint(50,150))
        tempsurf.blit(self.starttext, self.starttextrect)
        
        for i, mode in enumerate(self.modes):
            color = (255, 255, 255) if i == self.selected_mode else (180, 180, 180)
            mode_text = self.game.small_font.render(mode, True, color)
            mode_rect = mode_text.get_rect(center=(self.game.screen_width / 2, self.game.screen_height / 2 + (i * 45)))
            tempsurf.blit(mode_text, mode_rect)
            
            if i == self.selected_mode:
                rcolor = random.randint(20,60)
                pygame.draw.rect(tempsurf, (rcolor,rcolor,rcolor), mode_rect.inflate(random.randint(10,20), random.randint(10,20)), 1)
        
        tempsurf.blit(self.controls_text1, self.controls_rect1)
        tempsurf.blit(self.controls_text2, self.controls_rect2)
        
        tempsurf.set_colorkey((0,0,0))
        self.game.screen.blit(tempsurf,(0,0))