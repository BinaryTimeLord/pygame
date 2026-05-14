import pygame

class Camera():
    def __init__(self, target, screensize, levelsize, speed=0.1):
        self.offset = (0, 0)
        self.realoffset = target.rect.center
        self.target = target
        self.speed = speed  
        self.screensize = screensize
        self.levelsize = levelsize

    def update(self):
        self.realoffset = (
            (self.screensize[0] / 2) - self.target.rect.centerx,
            (self.screensize[1] / 2) - self.target.rect.centery
        )

        dx = self.realoffset[0] - self.offset[0]
        dy = self.realoffset[1] - self.offset[1]

        self.offset = (
            self.offset[0] + dx * self.speed,
            self.offset[1] + dy * self.speed
        )

        if self.offset[0] > 0:
            self.offset = (0, self.offset[1])
        if self.offset[0] < -self.levelsize[0] + self.screensize[0] + 8:
            self.offset = (-self.levelsize[0] + self.screensize[0] + 8, self.offset[1])
        if self.offset[1] > 28:
            self.offset = (self.offset[0], 28)
        if self.offset[1] < self.screensize[1] - self.levelsize[1]:
            self.offset = (self.offset[0], self.screensize[1] - self.levelsize[1])

        print("offset:", self.offset)

    def get_offset(self):
        return self.offset

    def draw_sprite(self, screen, sprite):
        cam_rect = pygame.Rect(
            (screen.get_rect().topleft[0] - self.offset[0],
             screen.get_rect().topleft[1] - self.offset[1]),
            (screen.get_width(), screen.get_height())
        )
        if sprite.rect.colliderect(cam_rect):
            screen.blit(sprite.image, (sprite.rect.topleft[0] + self.offset[0],
                                       sprite.rect.topleft[1] + self.offset[1]))