import os.path

import baddies
import camera
import pygame

import hud
import state
import player
import blocks
import level
import utilities
import fuckit

class Platformer(state.State):
    def __init__(self, game):
        state.State.__init__(self,game)
        self.tempsurf = pygame.Surface((200,160))
        self.player = player.Player(self)
        self.collidables = pygame.sprite.Group()
        self.decor = pygame.sprite.Group()

        self.level1 = level.level1
        self.level2 = level.level2
        self.level3 = level.level3
        self.level4 = level.level4
        self.level5 = level.level5
        self.level6 = level.level6
        self.level7 = level.level7
        self.level8 = level.level8
        self.level9 = level.level9
        self.level10 = level.level10
        self.level11 = level.level11
        self.level12 = level.level12
        self.currentlvl = 0
        self.backgroundimage = None
        self.coinimage = utilities.loadImage(os.path.join("data","images"),"coin.png",1)
        self.heartimage = utilities.loadImage(os.path.join("data","images"), "heart.png", 1)
        self.bridgeimages = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),"bridge.png", 1),(8,8))
        self.treeimage = utilities.loadImage(os.path.join("data","images"),"palmtree1.png" , 1)
        self.player.collision_group = self.collidables
        self.camera = camera.Camera(self.player,(self.tempsurf.get_width(),self.tempsurf.get_height()),(len(self.level1["map"][0] * 8),len(self.level1["map"] * 8)))

        self.coins = 0
        self.lives = 3
        self.health = 3

        self.jumpsound = utilities.loadSound(os.path.join("data", "sounds"),"jump.wav")
        self.oneupsound = utilities.loadSound(os.path.join("data", "sounds"), "1up.wav")
        self.jumpsound.set_volume(.5)
        self.hitsound = utilities.loadSound(os.path.join("data", "sounds"), "hit.wav")
        self.healthsound = utilities.loadSound(os.path.join("data", "sounds"), "health.wav")
        self.hud = hud.hud(self)


    def action_update(self):
        if self.game.actions["right"] and self.player.hitcooldown < 10:
            self.player.move(1 * self.game.delta_time,0)
            self.player.direction = 0
            self.player.actstate["walking"] = True
        if self.game.actions["left"]  and self.player.hitcooldown < 10:
            self.player.move(-(1 * self.game.delta_time), 0)
            self.player.direction = 1
            self.player.actstate["walking"] = True
        if self.game.actions["up"]:
            pass
        if self.game.actions["down"]:
            pass
        if self.game.actions["a"] and not self.player.hasjumped:
            if self.player.jumptimer <= 0  and self.player.groundcount > 0 :
                self.player.jumptimer = 25
                self.jumpsound.play()
                self.player.actstate["jumping"] = True
                self.player.hasjumped = True

        if self.game.actions["b"]:
            pass
        if self.game.actions["select"]:
            pass
        if self.game.actions["start"] and self.game.pausecooldown <= 0:
            self.game.pausecooldown = 20
            self.exit()
            self.game.pause.enter()
    def win(self):
        self.exit()
        self.game.winscreen.enter()
    def vic(self):
        self.exit()
        pygame.mixer.music.unload()
        self.game.victory.enter()
    def die(self):
        self.exit()
        self.lives -= 1
        if self.lives <= 0:
            self.game.curr_state.exit()
            self.game.gameover.enter()
        else:
            self.game.deathscreen.enter()

    def update(self):
        self.action_update()
        self.player.update()
        self.collidables.update()
        self.camera.update()
        self.hud.update()
        if self.health <= 0:
            self.die()
        if self.coins > 100:
            self.lives += 1
            self.oneupsound.play()
            self.coins -= 100


    def render(self):
        self.tempsurf.fill((0,0,0))
        self.tempsurf.blit(self.backgroundimage,(0,0))
        for i in self.decor:
            self.camera.draw_sprite(self.tempsurf,i)
        for i in self.collidables.sprites():
            self.camera.draw_sprite(self.tempsurf,i)
            #it = i.rect.copy()
            #it.topleft = utilities.add_pos(i.rect.topleft,self.camera.offset)
            #pygame.draw.rect(self.tempsurf,(90,90,90),it,1)

        self.camera.draw_sprite(self.tempsurf, self.player)
        self.hud.render(self.tempsurf)
        self.game.screen.blit(pygame.transform.scale(self.tempsurf,(800,640)),(0,0))

    def getsurroundings(self,letter, map,x,y):
        loh = [0, 0, 0, 0]
        try:
            if map[y // 8 + 1][x // 8] == letter:
                loh[0] = 1
        except:
            loh[0] = 0
        try:
            if map[y // 8 - 1][x // 8] == letter:
                loh[1] = 1
        except:
            loh[1] = 0
        try:
            if map[y // 8][x // 8 + 1] == letter:
                loh[2] = 1
        except:
            loh[2] = 0
        try:
            if map[y // 8][x // 8 - 1] == letter:
                loh[3] = 1
        except:
            loh[3] = 0
        return loh

    def lvlclear(self):
        for i in self.collidables:
            i.kill()
        for i in self.decor:
            i.kill()
    
    def levelparse(self,level):

        self.lvlclear()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(os.path.join("data","music",level["music"]))
        pygame.mixer.music.play(-1)
        pygame.mixer.music.set_volume(.5)
        map = level["map"]
        self.currentlvl = level["num"]
        self.backgroundimage = utilities.loadImage(os.path.join("data","images"),level["background image"])
        groundimages = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"),level["ground image"],1),(8,8))
        miscblocks = utilities.loadSpriteSheet(utilities.loadImage(os.path.join("data","images"), "miscblocks.png",1),(8,8))
        dimages = []
        for i in level["decor"]:
            dimages.append(utilities.loadImage(os.path.join("data","images"),i,1))
        self.camera = camera.Camera(self.player, (self.tempsurf.get_width(), self.tempsurf.get_height()),
                                    (len(level["map"][0] * 8), len(level["map"] * 8)))
        x = 0
        y = 0
        for i in map:
            for k in i:
                if k == "g":
                    loh = self.getsurroundings("g",map,x,y)
                    lor = self.getsurroundings("r",map,x,y)
                    lol = self.getsurroundings("l",map,x,y)
                    if loh == [1,0,1,0]:
                        self.collidables.add(blocks.wall(groundimages[0][0],(x,y),self))
                    elif loh == [1,0,1,1]:
                        self.collidables.add(blocks.wall(groundimages[0][1],(x,y),self))
                    elif loh == [1,0,0,1] and not lor == [ 0,1,0,1] and not lol == [ 0,1,1,0]:
                        self.collidables.add(blocks.wall(groundimages[0][2],(x,y),self))
                    elif loh == [1,1,1,0]:
                        self.collidables.add(blocks.wall(groundimages[1][0],(x,y),self))
                    elif loh == [1,1,1,1]:
                        self.collidables.add(blocks.wall(groundimages[1][1],(x,y),self))
                    elif loh == [1,1,0,1]:
                        self.collidables.add(blocks.wall(groundimages[1][2],(x,y),self))
                    elif loh == [0,1,1,0]:
                        self.collidables.add(blocks.wall(groundimages[2][0],(x,y),self))
                    elif loh == [0,1,1,1]:
                        self.collidables.add(blocks.wall(groundimages[2][1],(x,y),self))
                    elif loh == [0,1,0,1]:
                        self.collidables.add(blocks.wall(groundimages[2][2],(x,y),self))
                    elif loh == [0,0,1,0]:
                        self.collidables.add(blocks.wall(groundimages[3][0],(x,y),self))
                    elif loh == [0,0,1,1]:
                        self.collidables.add(blocks.wall(groundimages[3][1],(x,y),self))
                    elif loh == [0,0,0,1]:
                        self.collidables.add(blocks.wall(groundimages[3][2],(x,y),self))
                    elif loh == [0,0,0,0]:
                        self.collidables.add(blocks.wall(groundimages[3][3],(x,y),self))
                    elif loh == [1,0,0,0]:
                        self.collidables.add(blocks.wall(groundimages[3][4],(x,y),self))
                    elif loh == [1,1,0,0]:
                        self.collidables.add(blocks.wall(groundimages[3][5],(x,y),self))
                    if lor ==[0,1, 0, 0]:
                        self.collidables.add(blocks.wall(groundimages[2][4], (x, y),self))
                    elif lol == [0, 1, 0, 0]:
                        self.collidables.add(blocks.wall(groundimages[2][3], (x, y),self))
                    elif lor ==[0,0, 0, 1] and loh[1] == 0:
                        self.collidables.add(blocks.wall(groundimages[0][1], (x, y),self))
                    elif lol ==[0,0, 1, 0] and loh[1] == 0:
                        self.collidables.add(blocks.wall(groundimages[0][1], (x, y),self))
                    elif  lor == [ 0,1,0,1]:
                        self.collidables.add(blocks.wall(groundimages[2][4], (x, y),self))
                    elif  lol == [ 0,1,1,0]:
                        self.collidables.add(blocks.wall(groundimages[2][3], (x, y),self))
                if k == "r":
                    self.collidables.add(blocks.Ramp(groundimages[0][3],self,(x,y),True))
                if k == "l":
                    self.collidables.add(blocks.Ramp(groundimages[0][4],self,(x,y),False))
                if k == "t":
                    self.decor.add(blocks.decor(dimages[0],(x,y)))
                if k == "T":
                    self.decor.add(blocks.decor(dimages[1],(x,y)))
                if k == "a":
                    self.decor.add(blocks.decor(dimages[2],(x,y)))
                if k == "b":
                    log = self.getsurroundings("g",map,x,y)
                    if log[2]:
                        self.collidables.add(blocks.bridge(self.bridgeimages[0][2],self, (x, y)))
                    elif log[3]:
                        self.collidables.add(blocks.bridge(self.bridgeimages[0][0],self, (x, y)))
                    else:
                        self.collidables.add(blocks.bridge(self.bridgeimages[0][1],self,(x,y)))
                if k == "c":
                    self.collidables.add(blocks.collectable(self.coinimage,self,"coin",(x,y)))
                if k == "h":
                    self.collidables.add(blocks.collectable(self.heartimage,self,"heart",(x,y)))
                if k == "p":
                    self.collidables.add(blocks.PushBlock(miscblocks[0][4],(x,y),self.collidables,self)   )
                if k == "P":
                    self.player.set_pos((x,y))
                if k == "C":
                    self.collidables.add(baddies.Crab((x,y),self.collidables))
                if k == "f":
                    self.collidables.add(blocks.finish((x,y)))
                if k == "E":
                    self.collidables.add(blocks.Finalfinish((x,y)))
                if k == "D":
                    self.collidables.add(baddies.Dog((x,y),self.collidables))
                if k == "B":
                    self.collidables.add(baddies.Bee((x,y),self.collidables))
                if k =="M":
                    self.collidables.add(baddies.Bat((x,y),self.collidables))
                if k == "W":
                    self.collidables.add(baddies.Wolf((x,y),self.collidables))
                if k == "Q":
                    self.collidables.add(baddies.Penguin((x,y),self.collidables))
                if k == "J":
                    self.collidables.add(baddies.Jelly((x,y),self.collidables))
                if k == "8":
                    self.collidables.add(baddies.Snowman((x,y),self.collidables))
                if k == "S":
                    log = self.getsurroundings("g",map,x,y)
                    try:
                        if log[0]:
                            self.collidables.add(baddies.Spike((x,y),self.collidables, 0))
                        elif log[1]:
                            self.collidables.add(baddies.Spike((x,y),self.collidables, 1))
                        elif log[2]:
                            self.collidables.add(baddies.Spike((x,y),self.collidables, 2))
                        elif log[3]:
                            self.collidables.add(baddies.Spike((x,y),self.collidables, 3))
                    except:
                        pass
                x += 8
            y += 8
            x = 0
