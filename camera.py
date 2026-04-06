import pygame.sprite

import utilities

class Camera():
    def __init__(self, target, screensize,levelsize,speed = 1):
        self.offset = (0, 0)
        self.realoffest = target.rect.center
        self.target = target
        self. speed = speed
        self.screensize = screensize
        self.levelsize = levelsize
    def update(self):
        self.realoffset = utilities.sub_pos((self.screensize[0] / 2, self.screensize[1] / 2), self.target.rect.center)
        if self.offset[0] < self.realoffset[0]:
            self.offset = utilities.add_pos(self.offset,(self.speed,0))
        if self.offset[0] > self.realoffset[0]:
            self.offset = utilities.add_pos(self.offset,(-self.speed,0))
        if self.offset[1] < self.realoffset[1]:
            self.offset = utilities.add_pos(self.offset,(0,self.speed))
        if self.offset[1] > self.realoffset[1]:
            self.offset = utilities.add_pos(self.offset,(0,-self.speed))
        if self.offset[0] > 0:
            self.offset = utilities.setx(self.offset, 0)
        if self.offset[0] < -self.levelsize[0] + self.screensize[0] + 8:
            self.offset = utilities.setx(self.offset, -self.levelsize[0] + self.screensize[0] + 8)
        if self.offset[1]  > 28 :
            self.offset = utilities.sety(self.offset, 28)
        if self.offset[1] < self.screensize[1] - self.levelsize[1]:
            self.offset = utilities.sety(self.offset, self.screensize[1] - self.levelsize[1])

        print("offset" + str(self.offset))
        print(self.screensize[1] - self.levelsize[1])

    def get_offset(self):
        return self.offset
    def draw_sprite(self,screen,sprite):
        if sprite.rect.colliderect(pygame.rect.Rect(utilities.sub_pos(screen.get_rect().topleft, self.offset),(screen.get_width(),screen.get_height()))):
            screen.blit(sprite.image,utilities.add_pos(sprite.rect.topleft,self.offset))
