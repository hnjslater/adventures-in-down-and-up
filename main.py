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
    return image

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
    def __init__(self, img_path, x, y, **kwargs):
        pygame.sprite.Sprite.__init__(self)
        if isinstance(img_path, basestring):
            self.image = load_image(img_path)
        else:
            self.image = img_path
        self.rect = self.image.get_rect()

        self.rect.topleft = (x, y)
        self.dx = 0
        self.ddx = 0
        self.dy = 0
        self.ddy = 0

    def draw(self,win):
        pass
    def tick(self):
        self.rect.x += self.dx
        self.dx += self.ddx
        self.dy += self.ddy

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
        self.imageleft = pygame.transform.flip(self.image, True, False)
        self.imageright = self.image
        self.hops = 0
        self.falling = False
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
    def __init__(self, x, y, ** kwargs):
        if "img" in kwargs:
            Thing.__init__(self, kwargs["img"], x, y) 
        else:
            Thing.__init__(self, "platform.png", x, y)
    def draw(self, win):
        pass
    def bang(self, player):
        player.rect.bottom = self.rect.y-1
        player.dy = 0
        player.hops = 0
        player.falling = False

class LoosePlatform(Platform):
    def __init__(self, x, y, ** kwargs):
        Platform.__init__(self, x, y, ** kwargs)
    def tick(self):
        Platform.tick(self);
        if self.rect.y > 1000:
            self.kill()
            constants.STARTED = True
    def bang(self, player):
        self.ddy = 2.5
        player.dx = 0
        player.ddx = 0
        player.falling = True

class MovingPlatform(Platform):
    def __init__(self, x1, y1, x2, y2, speed, ** kwargs):
        self.max_x = max(x1,x2)
        self.max_y = max(y1,y2)
        self.min_x = min(x1,x2)
        self.min_y = min(y1,y2)
        self.speed = speed

        Platform.__init__(self, self.min_x, self.min_y, ** kwargs)

        self.dx = 0
        self.dy = 0
        if not x1 == x2:
            self.dx = self.speed
        if not y1 == y2:
            self.dy = self.speed

    def tick(self):
        Platform.tick(self);
        if not self.max_x == self.min_x:
            if self.rect.x > self.max_x:
                self.dx = -self.speed
            if self.rect.x < self.min_x:
                self.dx = self.speed

        if not self.max_y == self.min_y:
            if self.rect.y > self.max_y:
                self.dy = -self.speed
            if self.rect.y < self.min_y:
                self.dy = self.speed

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
            self.sprites.add(MovingPlatform(200, y, 400, y, 20))
            y += 100


        top = load_image("sky.png")
        self.sky = Thing(top.subsurface(0,0,top.get_rect().width,300),0,0)
        self.sky_color = top.get_at((0,0))
        self.sprites.add(self.sky, layer = SKY_LAYER)
        
        first_line = 50
        second_line = 150
        width = top.get_rect().width

        self.won = False


        ground1st = top.subsurface(0,300,first_line,50)
        self.ground = Platform(0,300, img = ground1st)
        self.sprites.add(self.ground, layer = PLATFORM_LAYER)

        ground2nd = top.subsurface(first_line,300,second_line - first_line,50)
        self.sprites.add(LoosePlatform(first_line, 300, img = ground2nd), layer = PLATFORM_LAYER)

        ground3rd = top.subsurface(second_line,300,width - second_line,50)
        self.sprites.add(Platform(second_line, 300, img = ground3rd), layer = PLATFORM_LAYER)

        self.sprites.add(Platform(200, 900))
        self.sprites.add(Platform(200, 1000))
        self.goal = Platform(400, -500)
        self.sprites.add(self.goal)

    def keypress(self, key):
        if not self.player.falling:
            if key == K_RIGHT:
                self.player.ddx = WALKING_SPEED
            elif key == K_LEFT:
                self.player.ddx = -WALKING_SPEED
            elif key == K_SPACE:
                self.player.jump()
        
    def keyup(self, key):
        if not self.player.falling:
            if key == K_RIGHT and self.player.ddx == WALKING_SPEED:
                self.player.ddx = 0
                self.player.dx = 0
            elif key == K_LEFT and self.player.ddx == -WALKING_SPEED:
                self.player.ddx = 0
                self.player.dx = 0
            
    def tick(self, win):
        self.sprites.tick();
        
        feet = pygame.sprite.Sprite()
        feet.rect = pygame.Rect(self.player.rect.x + self.player.rect.width /2, self.player.rect.bottom - 2, 2, 2)

        if self.player.dy > 0:
            for platform in self.sprites:
                if pygame.sprite.collide_rect(feet, platform) and hasattr(platform, "bang"):
                    platform.bang(self.player)


        y = self.player.rect.y
        if y < 100:
            for sprite in self.sprites:
                sprite.rect.y += 100 - y
        elif y > SCREEN_SIZE - 100:
            for sprite in self.sprites:
                sprite.rect.y += (SCREEN_SIZE - 100) - y

        if self.player.rect.bottom <= self.ground.rect.y and constants.STARTED and not self.won:
            self.sprites.add(Thing("win.png",0,self.sky.rect.y), layer = SKY_LAYER)
            self.won = True
            self.player.falling = True
            self.player.dx = 0
            self.player.ddx = 0
            
            

    def draw(self, win):
        win.fill((0,0,0), (0,0,SCREEN_SIZE,SCREEN_SIZE)) 
        if self.sky.rect.top > 0:
            win.fill(self.sky_color, (0,0,SCREEN_SIZE,self.sky.rect.top + 1)) 
            

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
