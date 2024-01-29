# -*- coding:utf-8 -*-

import pygame

from Settings import *
from Attributes import *
from Weapon import *
from Special import *

class Player(pygame.sprite.Sprite, Collidable):
    def __init__(self, window, bgm, x, y):
        # Must initialize everything one by one here
        pygame.sprite.Sprite.__init__(self)
        Collidable.__init__(self, window, bgm)
        self.images = [pygame.transform.scale(pygame.image.load(path), 
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for path in GamePath.player]
        
        self.dead = pygame.transform.scale(pygame.image.load(r'assets\player\dead.png'), 
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight))
        self.index = 0
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.dx, self.dy = 0, 0
        self.hp = 1000
        self.hp_limit = 1000
      
        self.tag = 'player'
    
        self.speed = PlayerSettings.playerSpeed
        self.original_speed = PlayerSettings.playerSpeed
        self.defence = 0.8
        self.atk = 20000000
        self.state = State.ALIVE
        self.money = 500

        self.shieldlevel = 1
        self.shield = pygame.transform.scale(pygame.image.load(f"./assets/shield/1.png"), (60, 60))
        self.shield_hp_limit = ShieldSettings.hp[0]
        self.shield_hp_coord = 60 / self.shield_hp_limit
        self.shield_hp = self.shield_hp_limit

        self.namefont = pygame.font.Font(None, PlayerSettings.FontSize)
        
        self.vert = 10
        self.acceleration = -2   #跳跃的相关变量

        self.dir = 1
        self.dodge = False
        self.dodge_cd = 0
        self.sword_cd = 0
        self.is_talking = False
        self.is_jumping = False
        self.defending = False
        self.skill = None
        self.peace = True

        self.ability = {'longcut': False, 'spin' : False, 'disappear' : False}
        self.buff_get = {'REPELL' : True, 'DIZZY' : False, 'FROZEN': False, 'BURNING': False}
        self.weapon = Sword(self.window, self, GamePath.Sword, 65, 55, self.bgm)
        
    def attr_update(self, addCoins = 0, addHP = 0, addAttack = 0, addDefence = 0, addShield = 0, addHP_limit = 0, islottery=False, ability=None, buff=None):
        if self.money + addCoins < 0 :
            if self.state == State.DEAD:
                self.money = 0
            return
        elif self.defence - addDefence < 0.2 or self.shieldlevel +addShield > 6 or (self.atk + addAttack> 10) or self.atk +addAttack < 1 or \
            self.defence - addDefence > 1 or self.hp_limit + addHP_limit > 5000 or self.hp_limit + addHP_limit < 300:
            if islottery:
                self.money += addCoins
                self.bgm.addsound('shopping')
            return    
        elif addCoins < 0 and self.state != State.DEAD:
            self.bgm.addsound('shopping') 

        self.money += addCoins
        self.hp += addHP
        self.atk += addAttack
        self.defence -= addDefence

        if ability != None:
            self.ability[ability] = True
        elif buff != None:
            self.buff_get[buff] = True

        if addDefence > 0 and self.defence <= 0.5:
            self.images = [pygame.transform.scale(pygame.image.load(path), 
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for path in GamePath.player2]
            self.dead = pygame.transform.scale(pygame.image.load(r'assets\player2\dead.png'), 
                                (PlayerSettings.playerWidth, PlayerSettings.playerHeight))
        elif addDefence < 0 and self.defence > 0.5:
            self.images = [pygame.transform.scale(pygame.image.load(path), 
                            (PlayerSettings.playerWidth, PlayerSettings.playerHeight)) for path in GamePath.player]
        
            self.dead = pygame.transform.scale(pygame.image.load(r'assets\player\dead.png'), 
                                (PlayerSettings.playerWidth, PlayerSettings.playerHeight))
            
        self.hp_limit += addHP_limit
        if addShield > 0:
            self.shieldlevel += addShield
            self.shield = pygame.transform.scale(pygame.image.load(f"./assets/shield/{self.shieldlevel}.png"), (60, 60))
            self.shield_hp_limit = ShieldSettings.hp[self.shieldlevel - 1]
            self.shield_hp_coord = 60 / self.shield_hp_limit
            self.shield_hp = self.shield_hp_limit

    def reset_pos(self, scene, x=WindowSettings.width // 2, y=WindowSettings.height // 2):
        self.bgm.stopwalking()
        if scene == SceneType.CITY:
            self.peace = True
            self.rect.topleft = WindowSettings.width // 2 - PlayerSettings.playerWidth//2, WindowSettings.height//2 - PlayerSettings.playerHeight//2
        if scene == SceneType.ICE:
            self.peace = False
            self.rect.topleft = WindowSettings.width // 2 - PlayerSettings.playerWidth//2, 45
        if scene == SceneType.LAVA:
            self.peace = False
            self.rect.topleft = 45, WindowSettings.height//2
        if scene == SceneType.WILD:
            self.peace = False
            self.rect.topleft = WindowSettings.width - PlayerSettings.playerWidth//2, WindowSettings.height//2
        if scene == SceneType.BOSS:
            self.peace = False
            self.rect.topleft = WindowSettings.width // 2 - PlayerSettings.playerWidth//2, WindowSettings.height - PlayerSettings.playerHeight
            self.weapon.update()

    def try_move(self, key):
        
        if key[pygame.K_l]:
            self.is_jumping = True
        if self.is_jumping:
            self.image = self.images[0]
            self.dy -= self.vert
            self.vert += self.acceleration
            if self.vert < -10:
                self.vert = 10
                self.is_jumping = False

        if key[pygame.K_SPACE] and self.dodge_cd == 0: 
            self.dodge = True
            self.dodge_cd = 5
            self.speed = 30
        

        if key[pygame.K_d] or key[pygame.K_w] or key[pygame.K_a] or key[pygame.K_s]:

            if self.is_jumping:
                self.image = self.images[0]
                self.bgm.stopwalking()
            else:
                self.index = (self.index + 0.5) % len(self.images)
                self.image = self.images[math.floor(self.index)]
                self.bgm.startwalking()

            if key[pygame.K_w] and self.rect.top > 0 :
                self.dy -= self.speed
            if key[pygame.K_s] and self.rect.bottom < WindowSettings.height:
                self.dy += self.speed
            if key[pygame.K_a] and self.rect.left > 0:
                self.dx -= self.speed
                self.dir = -1
            if key[pygame.K_d] and self.rect.right < WindowSettings.width:
                self.dx += self.speed
                self.dir = 1   
        else:
            self.image = self.images[0]
            self.bgm.stopwalking()

        self.rect = self.rect.move(self.dx, self.dy)

    def dodge_update(self):

        if self.dodge:
            self.dodge_cd -= 1
            if self.dodge_cd == 0:
                self.dodge = False
                self.speed = self.original_speed
                self.dodge_cd = 10
        elif self.dodge_cd > 0:
            self.dodge_cd -= 1

    def try_attack(self, key):
        
        if key[pygame.K_k] and self.shield_hp > 0:
            self.defending = True
        else: 
            self.defending = False

        if not self.weapon.startattack and not self.defending:
            if key[pygame.K_h]:
                self.skill = 'cut'
            elif key[pygame.K_j]:
                self.skill = 'stab'
            elif key[pygame.K_u] and self.ability['longcut']:
                self.skill = 'longcut'
            elif key[pygame.K_i] and self.ability['spin']:
                self.skill = 'spin'
            elif key[pygame.K_o] and self.ability['disappear'] and self.sword_cd == 0:
                self.skill = 'disappear'   
            else:
                self.skill = None   
        else:
            self.skill = None
        
    def update(self, key, slow_key):
        self.state_update()
        self.dodge_update()
        if self.state != State.DEAD:
            if self.state == State.TALKING or self.state == State.STILL:
                self.bgm.stopwalking()
                self.index = 0
                self.image = self.images[self.index]
            else:
                self.dx, self.dy = 0, 0
                if not self.peace:
                    self.try_attack(key)
                    self.weapon.update() 
                self.try_move(key)

            if self.dir == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            self.debuff_update()
            self.effect_update()
        
        self.weapon.get_hanpos()
        self.weapon.pos_update() 
    
    def effect_update(self):
        for effect in self.effect:
            effect.update()
            
    def state_update(self):
        if self.hp <= 0 and self.state != State.DEAD:
            self.hp = 0
            self.state = State.DEAD
            self.effect = pygame.sprite.Group()
            self.debuff = []
            self.image = self.dead
            if self.dir == -1:
                self.image = pygame.transform.flip(self.image, True, False)
            pygame.event.post(pygame.event.Event(Event.PlayerDead))
            
        if self.sword_cd > 0:
            self.sword_cd -= 1
            
    def debuff_update(self):

        for debuff in self.debuff:
            if debuff == Debuff.CURSE:
                self.effect.add(Curse(self, self.window, self.bgm, BuffSettings.curse))
                self.original_speed = 3
                self.speed = 3
                self.atk *= 0.8
                self.defence *= 1.8
                self.debuff.remove(Debuff.CURSE)

            elif debuff == Debuff.BURNING:
                for effect in self.effect:
                    if isinstance(effect, Flame):
                        if effect.time % 20 == 0:
                            self.hp = max(self.hp - 40, 0)
                        break

            elif debuff == Debuff.FROZEN or debuff == Debuff.DIZZY:
                self.state = State.STILL
            
            elif debuff == Debuff.REPELL:
                
                self.dx -= self.dir * 20
                self.rect = self.rect.move(self.dx, self.dy)
                self.clicktock(3)
                if not self.isclocking:
                    self.debuff.remove(Debuff.REPELL)

    def beingattacked(self, atk, buff):
        
        if (not self.dodge or self.dodge_cd > 5) and self.state != State.DEAD:
            if self.defending:
                self.hp -= max(atk * self.defence - self.shield_hp, 0)
                self.shield_hp = self.shield_hp - atk * self.defence
            else:
                self.hp -= atk * self.defence
                self.bgm.addsound('hurt')
                for debuff in buff:
                    if not debuff in self.debuff:
                        self.debuff.append(debuff)
                        if debuff == Debuff.BURNING:
                            self.effect.add(Flame(self, self.window, self.bgm, BuffSettings.flame, 60))
                        elif debuff == Debuff.FROZEN:
                            self.effect.add(Frozen(self, self.window, self.bgm, BuffSettings.frozen, 50))
                        elif debuff == Debuff.DIZZY:
                            self.effect.add(Dizzy(self, self.window, self.bgm, BuffSettings.dizzy, 30))

    def draw(self):
        
        if not self.defending and self.state != State.DEAD and self.shield_hp > 0:
            self.window.blit(self.shield, self.rect)
        self.window.blit(self.image, self.rect)
        if self.state != State.DEAD:
            if self.defending:
                pygame.draw.rect(self.window, (230, 230, 230), [self.rect.x, self.rect.y - 20, self.shield_hp*self.shield_hp_coord, 10], 0)
            if not self.peace:
                self.weapon.draw()
            if self.defending and self.shield_hp > 0:
                self.window.blit(self.shield, self.rect)
        
            for effect in self.effect:
                if effect.isdisappear():
                    if effect.debuff != None:
                        self.debuff.remove(effect.debuff)
                    self.effect.remove(effect)
                else:
                    effect.draw()

        self.render_attr()
    
    def render_attr(self):
        self.window.blit(pygame.transform.scale(pygame.image.load(r'assets\icon\purse.png'), (60, 60)), (10, 10))
        self.window.blit(self.namefont.render(str(self.money), False, Color.Golden), (95, 20))  #money

        hp_msg = str(math.floor(self.hp)) +' / ' + str(math.floor(self.hp_limit))
        self.window.blit(pygame.transform.scale(pygame.image.load(r'assets\icon\health.png'), (50, 50)), (15, 75))
        self.window.blit(self.namefont.render(hp_msg, False, Color.Red), (95, 85)) #hp

        if self.ability['disappear']:
            self.window.blit(pygame.transform.scale(pygame.image.load(r'assets\icon\sandglass.png'), (50, 50)), (15, 130))
            if self.sword_cd == 0:
                color = Color.Blue
            else:
                color = Color.Greyish
            self.window.blit(self.namefont.render(str(self.sword_cd), False, color), (95, 140)) #cd

        