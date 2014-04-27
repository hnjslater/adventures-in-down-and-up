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
    def tick(self):
        for thing in self:
            thing.tick()

class Thing(pygame.sprite.Sprite):
    def __init__(self, img_path, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image(img_path)
        self.rect.center = (x, y)
        self.dx = 0
        self.ddx = 0
    def draw(self,win):
        pass
    def tick(self):
        self.rect.x += self.dx
        self.dx += self.ddx

        if self.rect.x < 0:
            self.rect.x = 0
            if self.dx < 0:
                self.dx == 0

        if self.rect.right > SCREEN_SIZE:
            self.rect.right = SCREEN_SIZE
            if self.dx > 0:
                self.dx == 0

        if self.dx < -5:
            self.dx = -5
        elif self.dx > 5:
            self.dx = 5

    

class Stage():
    def __init__(self):
        self.sprites = SomeSprites()
        self.player = Thing("dude.png", 400, 400);
        self.sprites.add(self.player);
    def keypress(self, key):
        if key == K_RIGHT:
            self.player.ddx = 1;
        if key == K_LEFT:
            self.player.ddx = -1;
            
    def tick(self, win):
        self.sprites.tick();
        self.sprites.draw(win);
        

def main():
    pygame.init()

    fpsClock = pygame.time.Clock()

    win = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE))
    pygame.display.set_caption('game')
    font = pygame.font.Font(None, 20)

    stage = Stage()

    frame_count = 0

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                stage.keypress(event.key)
        
        stage.tick(win)
        
        pygame.display.update()
        fpsClock.tick(60)

main()
