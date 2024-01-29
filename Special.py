import pygame
import math

from BgmPlayer import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, window, difficulty, angle, bgm, paths, canhit=True):
        
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.transform.scale(pygame.image.load(path), paths['size'])
                       for path in paths['move']]
        self.size = paths['size']
        self.angle = angle
        if canhit:
            self.hit = paths['hit']
        else:
            self.hit = None
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.sound = paths['sound']
        
        self.index = 0
        self.len = len(self.images)

        self.AS = paths['as'] 
        self.atk = paths['atk'] * difficulty
        self.speed = paths['speed']

        self.window = window
        self.buff = paths['debuff']

        self.explode = False
        self.disappear = False

        self.bgm = bgm
        self.dx = 0
        self.dy = 0
        self.bgm.addsound(self.sound[0])
    
    def image_update(self):

        if self.explode and self.index == self.len - 1:
            self.disappear = True
        else:
            self.index = (self.index + self.AS) % self.len
            self.image = self.images[math.floor(self.index)]
        
    def attack(self):
        if self.hit != None:
            self.images = [pygame.transform.scale(pygame.image.load(path), self.size)
                                for path in self.hit]
            self.bgm.addsound(self.sound[1])
            self.index = 0
            self.AS = 1
            self.len = len(self.hit)
            self.explode = True
        else:
            self.disappear = True
            self.bgm.addsound(self.sound[1])
    
    def pos_update(self):
        self.dx += self.angle[0] * self.speed
        self.dy += self.angle[1] * self.speed
        self.rect = self.rect.move(self.dx, self.dy)

    def update(self):
        self.image_update()
        if not self.explode:
            self.pos_update()
    
    def draw(self):
        self.window.blit(self.image, self.rect)


class Buff(pygame.sprite.Sprite):
    def __init__(self, owner, window, bgm, paths, proportion=1):
        pygame.sprite.Sprite.__init__(self)
        self.owner = owner
        self.window = window
        self.bgm = bgm
        self.proportion = proportion
        self.images = [pygame.transform.scale(pygame.image.load(path), (paths['size'][0]*self.proportion, paths['size'][1]*self.proportion))
                       for path in paths['path']]
        self.image = self.images[0]
        self.fps = paths['fps']
        self.rect = self.image.get_rect()
        self.index = 0
        self.len = len(self.images)
        self.debuff = None

    def update(self):
        self.pos_update()
        self.image_update()
    
    def pos_update(self):
        self.rect.center = self.owner.rect.center
    
    def image_update(self):
        self.index = (self.index + self.fps) % self.len
        self.image = self.images[math.floor(self.index)]
    
    def isdisappear(self):
        return self.index >= self.len - 1
        
    def draw(self, x=0, y=0):
        self.window.blit(self.image, (self.rect[0]+x, self.rect[1]+y))
    

class Curse(Buff):
    def __init__(self, owner, window, bgm, paths, proportion=1):
        super().__init__(owner, window, bgm, paths, proportion)
    
    def pos_update(self):
        self.rect.center = (self.owner.rect.centerx+50, self.owner.rect.centery-30)

class SwordPlay(Buff):
    def __init__(self, owner, window, bgm, paths, proportion=1):
        super().__init__(owner, window, bgm, paths, proportion)
        self.again = False

    def isdisappear(self):
        if math.floor(self.index) >= self.len - 1:
            if self.again:
                return True
            else:
                self.again = True
                self.index = 0
    
class Flame(Buff):
    def __init__(self, owner, window, bgm, paths, time, proportion=1):
        super().__init__(owner, window, bgm, paths, proportion)
        self.time = time
        self.debuff = Debuff.BURNING
        self.bgm.burning.play(-1)

    def isdisappear(self):
        self.time -= 1
        if self.time == 0:
            self.bgm.burning.stop()
            return True
        else:
            return False


class Frozen(Buff):
    def __init__(self, owner, window, bgm, paths, time, proportion=1):
        super().__init__(owner, window, bgm, paths, proportion)
        self.time = time
        self.debuff = Debuff.FROZEN
        self.bgm.addsound('frozen')
    
    def isdisappear(self):
        self.time -= 1
        self.image.set_alpha(200)
        if self.time == 0:
            self.owner.state = State.ALIVE
            return True
        else:
            return False

class Dizzy(Buff):
    def __init__(self, owner, window, bgm, paths, time, proportion=1):
        super().__init__(owner, window, bgm, paths, proportion)
        self.time = time
        self.debuff = Debuff.DIZZY
    
    def pos_update(self):
        self.rect.center = (self.owner.rect.centerx, self.owner.rect.centery-30)

    def isdisappear(self):
        self.time -= 1
        if self.time == 0:
            self.owner.state = State.ALIVE
            return True
        else:
            return False

class Explode(Buff):
    def __init__(self, owner, window, bgm, paths, proportion=1):
        super().__init__(owner, window, bgm, paths, proportion)
    
    def draw(self, x=0, y=0):
        self.window.blit(self.image, (self.rect[0]+x, self.rect[1]+y-10))