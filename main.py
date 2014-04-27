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

class SomeSprites(pygame.sprite.LayeredUpdates):
    def __init__(self):
        pygame.sprite.LayeredUpdates.__init__(self)
    def draw(self,win):
        pygame.sprite.LayeredUpdates.draw(self,win)
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
        self.dy = 0

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

        if self.dx < -10:
            self.dx = -10
        elif self.dx > 10:
            self.dx = 10

        self.rect.y += self.dy

        if self.dy > 20:
            self.dy = 20


class Player(Thing):
    def __init__(self):
        Thing.__init__(self, "dude.png", 0,0)
        self.imageleft, self.rectleft = load_image("dude2.png")
        self.imageright, self.rectright = self.image, self.rect
        self.hops = 0
    def tick(self):
        old_dx = self.dx
        self.dy += 2 
        Thing.tick(self)
        if self.dx > 0:
            self.image = self.imageright
        elif self.dx < 0:
            self.image = self.imageleft

    def jump(self):
        if not self.hops > 1:
            self.dy = -25
            self.hops += 1


class Platform(Thing):
    def __init__(self, x, y):
        Thing.__init__(self, "platform.png", x, y)
        self.solid = True
    def tick(self):
        pass
    def draw(self, win):
        pass

class Stage():
    def __init__(self):
        self.sprites = SomeSprites()

        self.player = Player()
        self.sprites.add(self.player, layer =1)

        x = 0
        while x < SCREEN_SIZE:
            platform = Platform(x, 0)
            platform.rect.bottom = LEVEL_HEIGHT
            x += platform.rect.width
            self.sprites.add (platform)

        y = 300
        while y < LEVEL_HEIGHT:
            self.sprites.add(Platform(400, y))
            y += 100


        self.sprites.add(Thing("sky.png",0,0), layer = 0)
        self.sprites.add(Platform(400, 700))

        self.sprites.add(Platform(200, 800))
        self.sprites.add(Platform(200, 0))
        self.sprites.add(Platform(200, 900))
        self.sprites.add(Platform(200, 1000))
        self.goal = Platform(400, -500)
        self.sprites.add(self.goal)


    def keypress(self, key):
        if key == K_RIGHT:
            self.player.ddx = WALKING_SPEED
        elif key == K_LEFT:
            self.player.ddx = -WALKING_SPEED
        elif key == K_SPACE:
            self.player.jump()
        
    def keyup(self, key):
        if key == K_RIGHT and self.player.ddx == WALKING_SPEED:
            self.player.ddx = 0
            self.player.dx = 0
        elif key == K_LEFT and self.player.ddx == -WALKING_SPEED:
            self.player.ddx = 0
            self.player.dx = 0
            
    def tick(self, win):
        self.sprites.tick();
        
        feet = pygame.sprite.Sprite()
        feet.rect = pygame.Rect(self.player.rect.x, self.player.rect.bottom - 2, self.player.rect.width, 2)

        if self.player.dy > 0:
            for platform in self.sprites:
                if pygame.sprite.collide_rect(feet, platform) and hasattr(platform, "solid") and platform.solid:
                    self.player.rect.bottom = platform.rect.y-1
                    self.player.dy = 0
                    self.player.airbourne = False
                    self.player.hops = 0

        y = self.player.rect.y
        if y < 100:
            for sprite in self.sprites:
                sprite.rect.y += 100 - y
        elif y > SCREEN_SIZE - 100:
            for sprite in self.sprites:
                sprite.rect.y += (SCREEN_SIZE - 100) - y

        if self.player.rect.y < self.goal.rect.y:
            print "you win"
            

    def draw(self, win):
        win.fill((0,0,0), (0,0,SCREEN_SIZE,SCREEN_SIZE)) 
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
            elif event.type == KEYUP:
                stage.keyup(event.key)
        
        stage.tick(win)
        stage.draw(win)
        
        pygame.display.update()
        fpsClock.tick(60)

main()
