import pygame, sys, math, random, os
from pygame.locals import *
import random
from constants import *
import constants
from random import randint


def load_image(name):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert_alpha()
    colorkey = image.get_at((0,0))
    image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

class SomeSprites(pygame.sprite.Group):
    def __init__(self):
        pygame.sprite.Group.__init__(self)
    def draw(self,win):
        pygame.sprite.Group.draw(self, win)
        for thing in self:
            thing.draw(win)

class Thing(pygame.sprite.Sprite):
    def __init__(self, img_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(img_path)
        self.rect.center = (x, y)
    def draw(self,win):
        pass

def main():
    pygame.init()

    fpsClock = pygame.time.Clock()

    win = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
    pygame.display.set_caption('game')
    font = pygame.font.Font(None, 20)

    sprites = SomeSprites()
    sprites.add(Thing("dude.png", 400, 400));

    frame_count = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        sprites.draw(win);

        pygame.display.update()
        fpsClock.tick(60)
        print(fpsClock.get_fps())



main()
