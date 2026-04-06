import os.path

import pygame
import utilities

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.images = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"moe.png",1),(8,8))
        self.game = game
        self.frame = 0

        self.idle_right = [self.images[0][0],self.images[0][1]]
        self.walk_right = [self.images[0][2],self.images[0][3]]
        self.right_jump = self.images[1][0]
        self.falling_right = self.images[2][1]
        self.land_right = self.images[1][1]
        self.hit_right = self.images[2][2]

        self.idle_left = utilities.flipimages(self.idle_right)
        self.walk_left = utilities.flipimages(self.walk_right)
        self.left_jump = pygame.transform.flip(self.right_jump,True, False).convert_alpha()
        self.falling_left = pygame.transform.flip(self.falling_right,True, False).convert_alpha()
        self.land_left = pygame.transform.flip(self.land_right, True, False).convert_alpha()
        self.hit_left = pygame.transform.flip(self.hit_right, True,False).convert_alpha()

        self.image = self.idle_right[0]
        self.rect = self.image.get_rect().inflate(-2,0)
        self.position = self.rect.topleft
        self.collision_group = pygame.sprite.Group()
        self.direction = 0
        self.actstate = {"walking":False,"idle":False,"jumping":False,"falling":False, "hit":False}
        self.currstate = "idle"
        self.jumptimer = 0
        self.groundcount = 3
        self.grounded = False
        self.hasjumped = False
        self.hitcooldown = 0

    def set_pos(self, pos):
        self.rect.topleft = pos
        self.jumptimer = 0
        self.actstate = {"walking": False, "idle": False, "jumping": False, "falling": False, "hit": False}
        self.grounded = False
        self.hasjumped = False
        self.hitcooldown = 0
        self.direction = 0


    def move(self,x,y, rfix = False):
        self.move_single_axis(round(x), 0,rfix)
        self.move_single_axis(0,round(y),rfix)

    def baddiehit(self):
        if self.hitcooldown <= 0:
            self.game.health -=1
            self.hitcooldown = 40
            self.game.hitsound.play()
    def move_single_axis(self,x,y,rfix = False):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collision_group, False)
        for block in hit:
            if rfix:
                block.onhit(self,-1)
            if x > 0:
                block.onhit(self,0)
            if x < 0:
                block.onhit(self,1)
            if y > 0:
                block.onhit(self,2)
            if y < 0:
                block.onhit(self,3)
    def update(self):
        if self.groundcount > -10:
            self.move(0,1)
        if self.groundcount <= -10:
            self.move(0,2)
        self.frame += 1
        if utilities.get_key(self.actstate,True) == None:
            self.actstate["idle"] = True
        if self.groundcount < 0:
            self.actstate["falling"] = True
            self.grounded = False
        if self.jumptimer > 20:
            self.move(0,-3)
            self.jumptimer -= 1
            self.actstate["jumping"] = True
        elif self.jumptimer > 5:
            self.move(0, -2)
            self.jumptimer -= 1
            self.actstate["jumping"] = True
        elif self.jumptimer > 0:
            self.move(0, -1)
            self.jumptimer -= 1
            self.actstate["jumping"] = True
        if not self.game.game.actions["a"] and self.jumptimer < 20:
            self.jumptimer = 0
        if self.direction == 0:
            if self.actstate["walking"]:
                self.image = self.walk_right[int(self.frame/8%2)]
            if self.actstate["idle"]:
                self.image = self.idle_right[int(self.frame / 8 % 2)]
            if self.actstate["falling"]:
                self.image = self.falling_right
            if self.groundcount == 3 and self.grounded == False:
                self.image = self.land_right
                self.grounded = True
            if self.actstate["jumping"]:
                self.image = self.right_jump
            if self.hitcooldown > 35:
                self.image = self.hit_right
                self.move(-1,-2)
                self.jumptimer = 0
        if self.direction == 1:
            if self.actstate["walking"]:
                self.image = self.walk_left[int(self.frame/8%2)]
            if self.actstate["idle"]:
                self.image = self.idle_left[int(self.frame / 8 % 2)]
            if self.actstate["falling"]:
                self.image = self.falling_left
            if self.groundcount == 3  and self.grounded == False:
                self.image = self.land_left
                self.grounded = True
            if self.actstate["jumping"]:
                self.image = self.left_jump
            if self.hitcooldown > 35:
                self.jumptimer = 0
                self.image = self.hit_left
                self.move(1,-2)
        self.groundcount -= 1
        if self.grounded and self.hasjumped and not self.game.game.actions["a"]:
            self.hasjumped = False
        self.hitcooldown -= 1


        for k in self.actstate.keys():
            self.actstate[k] = False

