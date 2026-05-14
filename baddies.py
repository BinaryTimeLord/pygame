import os.path
import random

import blocks
import utilities
import pygame
import player

class Crab(pygame.sprite.Sprite):
    def __init__(self,pos,collisiongroup):
        pygame.sprite.Sprite.__init__(self)
        self.images = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"crab.png",1),(8,8))[0]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.copy().inflate(-2,-2)
        self.collisiongroup = collisiongroup

        self.dir = True
        self.frame = 0

    def move(self,x,y,rfix = False):
        self.move_single_axis(round(x), 0)
        self.move_single_axis(0,round(y))


    def move_single_axis(self,x,y):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collisiongroup, False)
        for block in hit:
            if not block == self and not isinstance(block,blocks.collectable):
                if x > 0:
                    block.onhit(self,0)
                    self.dir = False
                if x < 0:
                    block.onhit(self,1)
                    self.dir = True
                if y > 0:
                    block.onhit(self,2)
                if y < 0:
                    block.onhit(self,3)
    def onhit(self,object,direction = 0):
        if isinstance(object,player.Player):
            if self.hitbox.colliderect(object.rect):
                object.baddiehit()
                self.dir = not self.dir


    def update(self):
        if self.dir:
            self.move(1,0)
        if not self.dir:
            self.move(-1,0)
        self.move(0,1)
        self.frame += 1
        self.image = self.images[int(self.frame / 8 % 2)]
        self.hitbox.center = self.rect.center
    def render(self,screen):
        screen.blit(self.image,self.rect)

class Dog(pygame.sprite.Sprite):
    def __init__(self,pos,collisiongroup):
        pygame.sprite.Sprite.__init__(self)
        self.rimages = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"dog.png",1),(8,8))[0]
        self.limages = utilities.flipimages(self.rimages)
        self.image = self.rimages[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.collisiongroup = collisiongroup
        self.hitbox = self.rect.copy().inflate(-2, -2)

        self.dir = True
        self.frame = 0

    def move(self,x,y,rfix = False):
        self.move_single_axis(round(x), 0)
        self.move_single_axis(0,round(y))


    def move_single_axis(self,x,y):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collisiongroup, False)
        for block in hit:
            if not block == self:
                if x > 0:
                    block.onhit(self,0)
                    self.dir = False
                if x < 0:
                    block.onhit(self,1)
                    self.dir = True
                if y > 0:
                    block.onhit(self,2)
                if y < 0:
                    block.onhit(self,3)
    def onhit(self,object,direction = 0):
        if isinstance(object,player.Player):
            if self.hitbox.colliderect(object.rect):
                object.baddiehit()
                self.dir = not self.dir


    def update(self):
        if self.dir:
            self.move(1,0)
        if not self.dir:
            self.move(-1,0)
        self.move(0,1)
        self.frame += 1
        if self.dir == True:
            self.image = self.rimages[int(self.frame / 8 % 3)]
        if self.dir == False:
            self.image = self.limages[int(self.frame / 8 % 3)]
        self.hitbox.center = self.rect.center

    def render(self,screen):
        screen.blit(self.image,self.rect)


class Bee(pygame.sprite.Sprite):
    def __init__(self,pos,collisiongroup):
        pygame.sprite.Sprite.__init__(self)
        self.rimages = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"Bee.png",1),(8,8))[0]
        self.limages = utilities.flipimages(self.rimages)
        self.image = self.rimages[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.collisiongroup = collisiongroup
        self.hitbox = self.rect.copy().inflate(-2, -2)

        self.dir = True
        self.frame = 0
        self.distance = 0
        self.wobble = random.randint(0, 10) * .1
        self.wdir = True

    def move(self,x,y,rfix = False):
        self.move_single_axis(round(x), 0)
        self.move_single_axis(0,round(y))


    def move_single_axis(self,x,y):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collisiongroup, False)
        for block in hit:
            if not block == self:
                if x > 0:
                    block.onhit(self,0)
                    self.dir = False
                    self.distance = 40 - self.distance
                if x < 0:
                    block.onhit(self,1)
                    self.dir = True
                    self.distance = 40 - self.distance
                if y > 0:
                    block.onhit(self,2)
                if y < 0:
                    block.onhit(self,3)
    def onhit(self,object,direction = 0):
        if isinstance(object,player.Player):
            if self.hitbox.colliderect(object.rect):
                object.baddiehit()
                self.dir = not self.dir
                self.distance = 40 - self.distance


    def update(self):
        if self.dir:
            self.move(1,0)
        if not self.dir:
            self.move(-1,0)
        self.frame += 1
        if self.dir == True:
            self.image = self.rimages[int(self.frame / 8 % 2)]
        if self.dir == False:
            self.image = self.limages[int(self.frame / 8 % 2)]
        self.distance += 1
        if self.distance > 40:
            self.distance = 0
            self.dir = not self.dir
        if self.wdir == True:
            self.wobble += .1
            self.rect.move_ip(0,-self.wobble)
            if self.wobble > 1:
                self.wobble = 0
                self.wdir = False
        else:
            self.wobble += .1
            self.rect.move_ip(0, self.wobble)
            if self.wobble > 1:
                self.wobble = 0
                self.wdir = True
        self.hitbox.center = self.rect.center

    def render(self,screen):
        screen.blit(self.image,self.rect)

class Penguin(pygame.sprite.Sprite):
    def __init__(self,pos,collisiongroup):
        pygame.sprite.Sprite.__init__(self)
        self.rimages = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"penguin.png",1),(8,8))[0]
        self.limages = utilities.flipimages(self.rimages)
        self.image = self.rimages[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.collisiongroup = collisiongroup
        self.hitbox = self.rect.copy().inflate(-2, -2)

        self.dir = True
        self.frame = 0

    def move(self,x,y,rfix = False):
        self.move_single_axis(round(x), 0)
        self.move_single_axis(0,round(y))


    def move_single_axis(self,x,y):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collisiongroup, False)
        for block in hit:
            if not block == self:
                if x > 0:
                    block.onhit(self,0)
                    self.dir = False
                if x < 0:
                    block.onhit(self,1)
                    self.dir = True
                if y > 0:
                    block.onhit(self,2)
                if y < 0:
                    block.onhit(self,3)
    def onhit(self,object,direction = 0):
        if isinstance(object,player.Player):
            if self.hitbox.colliderect(object.rect):
                object.baddiehit()
                self.dir = not self.dir


    def update(self):
        if self.dir:
            self.move(1,0)
        if not self.dir:
            self.move(-1,0)
        self.move(0,1)
        self.frame += 1
        if self.dir == True:
            self.image = self.rimages[int(self.frame / 8 % 3)]
        if self.dir == False:
            self.image = self.limages[int(self.frame / 8 % 3)]
        self.hitbox.center = self.rect.center
    def render(self,screen):
        screen.blit(self.image,self.rect)
class Spike(pygame.sprite.Sprite):
    def __init__(self,pos,collisiongroup,dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = utilities.loadImage(os.path.join("data","images"),"spike.png",1)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.collisiongroup = collisiongroup
        self.hitbox = self.rect.copy().inflate(-3, -3)

        self.dir = dir

        if self.dir == 1:
            self.image = pygame.transform.flip(self.image,True,True).convert_alpha()
        if self.dir == 2:
            self.image = pygame.transform.rotate(self.image,90).convert_alpha()
        if self.dir == 3:
            self.image = pygame.transform.rotate(self.image, -90).convert_alpha()


    def move(self,x,y,rfix = False):
        self.move_single_axis(round(x), 0)
        self.move_single_axis(0,round(y))


    def move_single_axis(self,x,y):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collisiongroup, False)
        for block in hit:
            if not block == self:
                if x > 0:
                    block.onhit(self,0)
                    self.dir = False
                if x < 0:
                    block.onhit(self,1)
                    self.dir = True
                if y > 0:
                    block.onhit(self,2)
                if y < 0:
                    block.onhit(self,3)
    def onhit(self,object,direction = 0):
        if isinstance(object,player.Player):
            if self.hitbox.colliderect(object.rect):
                object.baddiehit()


    def update(self):
        pass
    def render(self,screen):
        screen.blit(self.image,self.rect)

class Snowman(pygame.sprite.Sprite):
    def __init__(self,pos,collison_group):
        pygame.sprite.Sprite.__init__(self)
        self.images = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"snowman.png", 1),(8,8))
        self.left_walking = self.images[0]
        self.left_throwing = self.images[1]
        self.right_walking = utilities.flipimages(self.left_walking)
        self.right_throwing = utilities.flipimages(self.left_throwing)
        self.image = self.left_walking[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.copy()
        self.dir = False
        self.throwing = False
        self.distance = 0
        self.frame = 0
        self.collisiongroup = collison_group
        self.halfmove = True

    def move(self,x,y,rfix = False):
        self.move_single_axis(round(x), 0)
        self.move_single_axis(0,round(y))

    def move_single_axis(self,x,y):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collisiongroup, False)
        for block in hit:
            if not block == self:
                if x > 0:
                    block.onhit(self,0)
                    self.dir = False
                if x < 0:
                    block.onhit(self,1)
                    self.dir = True
                if y > 0:
                    block.onhit(self,2)
                if y < 0:
                    block.onhit(self,3)
    def onhit(self,object,direction = 0):
        if isinstance(object,player.Player):
            if self.hitbox.colliderect(object.rect):
                object.baddiehit()
    def update(self):
        if self.throwing == False:
            if self.halfmove == True:
                if self.dir == True:
                    self.move(1,0)
                    self.image = self.right_walking[int(self.frame / 8 % 3)]
                if self.dir == False:
                    self.move(-1,0)
                    self.image = self.left_walking[int(self.frame / 8 % 3)]
            self.distance += 1
            if self.distance > 30:
                self.throwing = True
                self.distance = 0
            self.halfmove = not self.halfmove
        self.frame += 1
        self.hitbox.center = self.rect.center
        if self.throwing == True:
            a = int(self.frame / 20 % 4) - 1
            if self.dir == True:
                self.image = self.right_throwing[a]
            if self.dir == False:
                self.image = self.left_throwing[a]
            if a >= 2:
                self.collisiongroup.add(Snowball(self.dir,self.rect.center,self.collisiongroup))
                self.dir = not self.dir
                self.throwing = False
                self.halfmove = True
class Snowball(pygame.sprite.Sprite):
    def __init__(self,direction,startpos, colgro):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((2,2))
        self.image.fill((255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = startpos
        self.dir = direction
        self.collisiongroup = colgro
        self.distance = 0
        self.slowmove = 0

    def move(self,x,y,rfix = False):
        self.move_single_axis(round(x), 0)
        self.move_single_axis(0,round(y))

    def move_single_axis(self,x,y):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collisiongroup, False)
        for block in hit:
            if not block == self and self.distance > 5:
                if x > 0:
                    block.onhit(self,0)
                    self.kill()
                if x < 0:
                    block.onhit(self,1)
                    self.kill()
                if y > 0:
                    block.onhit(self,2)
                    self.kill()
                if y < 0:
                    block.onhit(self,3)
                    self.kill()
    def onhit(self,object,direction = 0):
        if isinstance(object,player.Player):
            object.baddiehit()
            self.kill()
    def update(self):
        if self.dir:
            self.move(1,0)
        if not self.dir:
            self.move(-1,0)
        self.distance += 1
        self.slowmove += .33
        if self.distance < 20:
            self.move(0,-self.slowmove)
        if self.distance > 30:
            self.move(0,self.slowmove)
        if self.slowmove > 1:
            self.slowmove = 0

class Bat(pygame.sprite.Sprite):
    def __init__(self,pos,collison_group):
        pygame.sprite.Sprite.__init__(self)
        self.images = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"bat.png",1),(8,8))[0]
        self.rest_image = self.images[0]
        self.flying_image = [self.images[1],self.images[2]]
        self.image = self.rest_image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.copy().inflate(-2,-2)
        self.state = "resting"
        self.rest_time = random.randint(1,100)
        self.fly_time = 0
        self.dir = True
        self.collisiongroup = collison_group
        self.frame = 0
    def move(self,x,y,rfix = False):
        self.move_single_axis(round(x), 0)
        self.move_single_axis(0,round(y))

    def move_single_axis(self,x,y):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collisiongroup, False)
        for block in hit:
            if not block == self and (isinstance(block,blocks.wall) or isinstance(block,blocks.bridge)):
                if x > 0:
                    block.onhit(self,0)
                if x < 0:
                    block.onhit(self,1)
                if y > 0:
                    block.onhit(self,2)
                if y < 0:
                    block.onhit(self,3)
                    self.state = "resting"
                    self.rest_time = random.randint(50,100)
    def onhit(self,object,direction = 0):
        if isinstance(object,player.Player):
            object.baddiehit()
    def update(self):
        self.frame += 1
        print(self.state)
        if self.state == "resting":
            self.image = self.rest_image
            self.rest_time -= 1
            if self.rest_time <= 0 :
                self.state = "flying"
                self.fly_time = 50
                self.dir = not self.dir
        if self.state == "flying":
            if self.dir == True:
                self.image = self.flying_image[int(self.frame / 8 % 2)]
                if self.fly_time > 25:
                    self.move(1,1)
                elif self.fly_time < 0:
                    self.move(1,-1)
                else:
                    self.move(1,0)
            if self.dir == False:
                self.image = self.flying_image[int(self.frame / 8 % 2)]
                if self.fly_time > 25:
                    self.move(-1,1)
                elif self.fly_time < 0:
                    self.move(-1,-1)
                else:
                    self.move(-1,0)
            self.fly_time -= 1

class Wolf(Dog):
    def __init__(self,pos,collisiongroup):
        Dog.__init__(self, pos, collisiongroup)
        self.rimages = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"wolves.png",1),(8,8))[0]
        self.limages = utilities.flipimages(self.rimages)


class Jelly(pygame.sprite.Sprite):
    def __init__(self,pos,colgroup):
        pygame.sprite.Sprite.__init__(self)
        self.images = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"jellyfish.png",1),(8,8))[0]
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.hitbox = self.rect.copy().inflate(-2,-2)
        self.ydir = True
        self.xdir = True
        self.ytime = random.randint(1,40)
        self.xtime = random.randint(1,40)
        self.frame = 0
        self.collisiongroup = colgroup
        self.slowdown = 0
    def move(self,x,y,rfix = False):
        self.move_single_axis(round(x), 0)
        self.move_single_axis(0,round(y))

    def move_single_axis(self,x,y):
        self.rect.move_ip(x,y)
        hit = pygame.sprite.spritecollide(self, self.collisiongroup, False)
        for block in hit:
            if not block == self:
                if x > 0:
                    block.onhit(self,0)
                if x < 0:
                    block.onhit(self,1)
                if y > 0:
                    block.onhit(self,2)
                if y < 0:
                    block.onhit(self,3)
            if isinstance(block,blocks.bridge):
                self.ydir = True
    def onhit(self,object,direction = 0):
        if isinstance(object,player.Player):
            object.baddiehit()
    def update(self):
        if self.slowdown == 3:
            self.xtime -= 1
            self.ytime -= 1
            self.frame += 1
            self.image = self.images[int(self.frame / 8 % 4)]
            if self.xdir == True:
                self.move(1,0)
            if self.xdir == False:
                self.move(-1,0)
            if self.ydir == True:
                self.move(0,1)
            if self.ydir == False:
                self.move(0,-1)
            if self.xtime < 0:
                self.xdir = random.choice([True,False])
                self.xtime = random.randint(1,40)
            if self.ytime < 0:
                self.ydir = random.choice([True,False])
                self.ytime = random.randint(1,40)
            self.slowdown = 0
        self.slowdown += 1





