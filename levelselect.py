import os.path
import pygame

import level
import utilities
import state

class LevelSelect(state.State):
    def __init__(self,game):
        state.State.__init__(self,game)
        self.mapimage = utilities.loadImage(os.path.join("data","images"),"mapselect.png")
        self.points = [(622,622),(650,506),(738,379),(688,234),(520,365),(345,365),(333,250),(469,232),(496,102),(383,134),(246,109),(81,135)]
        self.current_sel = 0
        self.pressedonce = False
        self.musicplaying = False
        self.movesound = utilities.loadSound(os.path.join("data","sounds"),"selmove.wav")
        self.levellock = level.levellocks

    def update(self):
        if pygame.mouse.get_pressed()[0]:
            pass
        if self.game.actions["up"] and self.current_sel < 11 and self.pressedonce == False:
            self.current_sel +=1
            self.pressedonce = True
            self.movesound.play()
        if self.game.actions["down"] and self.current_sel > 0 and self.pressedonce == False:
            self.current_sel -= 1
            self.pressedonce = True
            self.movesound.play()
        if not self.game.actions["up"] and not self.game.actions["down"] :
            self.pressedonce = False
        if not self.musicplaying:
            pygame.mixer.music.load(os.path.join("data", "music", "levelsel.ogg"))
            pygame.mixer.music.play(-1)
            self.musicplaying = True
        if self.game.actions["a"]:
            if self.levellock[self.current_sel] == 0 or self.levellock[self.current_sel] == 2:
                self.exit()
                self.musicplaying = False
                self.game.platformer.enter()
                if self.current_sel == 0:
                    self.game.platformer.levelparse(self.game.platformer.level1)
                if self.current_sel == 1:
                    self.game.platformer.levelparse(self.game.platformer.level2)
                if self.current_sel == 2:
                    self.game.platformer.levelparse(self.game.platformer.level3)
                if self.current_sel == 3:
                    self.game.platformer.levelparse(self.game.platformer.level4)
                if self.current_sel == 4:
                    self.game.platformer.levelparse(self.game.platformer.level5)
                if self.current_sel == 5:
                    self.game.platformer.levelparse(self.game.platformer.level6)
                if self.current_sel == 6:
                    self.game.platformer.levelparse(self.game.platformer.level7)
                if self.current_sel == 7:
                    self.game.platformer.levelparse(self.game.platformer.level8)
                if self.current_sel == 8:
                    self.game.platformer.levelparse(self.game.platformer.level9)
                if self.current_sel == 9:
                    self.game.platformer.levelparse(self.game.platformer.level10)
                if self.current_sel == 10:
                    self.game.platformer.levelparse(self.game.platformer.level11)
                if self.current_sel == 11:
                    self.game.platformer.levelparse(self.game.platformer.level12)

    def render(self):
        self.game.screen.blit(pygame.transform.scale(self.mapimage,(self.game.screen_width,self.game.screen_height)),(0,0))
        pygame.draw.lines(self.game.screen, (25, 25, 25), False, self.points, 6)
        pygame.draw.lines(self.game.screen,(255,255,255),False,self.points,3)
        at = 0
        for i in self.points:
            pygame.draw.circle(self.game.screen, (25, 25, 25), i, 14)
            pygame.draw.circle(self.game.screen,(255,255,255),i,10)
            if self.levellock[at] == 1:
                pygame.draw.circle(self.game.screen, (255, 25, 25), i, 8)
            if self.levellock[at] == 2:
                pygame.draw.circle(self.game.screen, (25, 255, 25), i, 8)
            at += 1
        pygame.draw.circle(self.game.screen, (2, 2, 255), self.points[self.current_sel], 9)