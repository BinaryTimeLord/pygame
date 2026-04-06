
import os
import pygame


def loadImage(dir, filename, alpha=0):
    try:
        imgdir = os.path.join(dir, filename)
        print(imgdir)
        image = pygame.image.load(imgdir)
        if image == None:
            image = pygame.Surface(64,64)
            image.fill((255,0,0))
        if alpha == 1:
            image.set_colorkey(image.get_at((0,0)))
            image.convert_alpha()
        else:
            image.convert()
            #image.set_colorkey(image.get_at((0,0)))
        return image
    except:
        print("couldn't load image" + filename)


def loadSound(dir, filename):
    try:
        sound = pygame.mixer.Sound(os.path.join(dir, filename))
        return sound
    except:
        print("couldn't load sound " + filename)


def changeVolumes(los, vol):
    try:
        for i in los:
            i.set_volume(vol)
    except:
        print("could not adjust volume")


def getImageAt(image, loc, size):
    try:
        a = pygame.Surface(size).convert_alpha()
        a.blit(image, (0, 0), pygame.Rect((loc), (size)))
        a.set_colorkey((0,0,0))
        return a
    except:
        print("couldnt retreive image at " + loc)


def loadSpriteSheet(image, tilesize):
    try:
        ssw = image.get_width() // tilesize[0]
        ssh = image.get_height() // tilesize[1]
        print(ssw)
        print(ssh)
        x, y = 0, 0
        loloi = []
        for i in range(ssh):
            loi = []
            for n in range(ssw):
                loi.append(getImageAt(image, (x, y), tilesize))
                x += tilesize[0]
            loloi.append(loi)
            y += tilesize[1]
            x = 0
        return loloi
    except:
        print("error occured while trying to load sprite sheet")

def get_key(adict,val):
    for key, value in adict.items():
        if val == value:
            return key

    return None
import random


def sub_pos(pos1, pos2):
    x = pos1[0] - pos2[0]
    y = pos1[1] - pos2[1]
    return (x, y)


def add_pos(pos1, pos2):
    x = pos1[0] + pos2[0]
    y = pos1[1] + pos2[1]
    return (x, y)
def setx(pos,num):
    x = num
    y = pos[1]
    return (x,y)
def sety(pos,num):
    x = pos[0]
    y = num
    return (x,y)


def randpos(pos1, pos2):
    x = random.randint(pos1[0], pos2[0])
    y = random.randint(pos1[1], pos2[1])
    return (x, y)

def flipimages(loi):
    nloi = []
    for i in loi:
        nloi.append(pygame.transform.flip(i,True,False).convert_alpha())
    return nloi