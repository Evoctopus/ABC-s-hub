import pygame
import math
from random import randint, uniform

from NPCs import *
from Settings import *
from Attributes import *
from Weapon import *

class Monster(NPC):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths, NeedDetect = False):
        super().__init__(x, y, name, window, player, bgm, paths)

        self.difficulty = difficulty
        self.original = self.images
        self.attacking = False
        self.hasattacked = False
        self.startattack = False
        self.check = False
        self.cooling = False
        self.completelydead = False
        self.disappear = False
        self.weapon = None
        self.attacking_method = None
        self.burning = False
        self.location = None
        self.NeedDetect = NeedDetect
        self.difficulty = difficulty
        self.tag = 'monster'
        self.attackrange = MonsterSettings.AttackingRange
        self.can_draw_weapon = True
        self.buff = []
        self.debuff = []
        self.previous_state = State.ALIVE
        self.clock = 0
        self.proportion = 1
    
    def set_attr(self, hp, defence, speed, atk, fps, cd):
        self.fps = fps
        self.cd = cd
        self.defence = defence
        self.speed = speed
        self.atk = atk * self.difficulty
        self.hp = hp* self.difficulty
        self.coord = 60 / self.hp

    def attack(self):
        pass    

    def image_update(self):
        if self.state == State.DEAD:
            self.set_dead()
        if not self.completelydead and self.state != State.FROZEN:
            self.index = (self.index + self.fps) % self.len 
            self.image = self.images[math.floor(self.index)]
        self.flip_image()

    def flip_image(self):
        if self.state != State.FROZEN and self.can_flip():
            self.image = pygame.transform.flip(self.image, True, False)
    
    def can_flip(self):
        return self.dir == -1

    def set_dead(self):
        self.completelydead = True

    def set_target(self, target=None):
        if target == None:
            self.target = self.get_player_rect()
        else:
            self.target = target

    def get_player_rect(self):
        return self.player.rect.center

    def attackimage(self):
        return [self.images[0]]

    def stillimage(self):
        return [self.images[0]]

    def moveimage(self):
        return self.original

    def hitimage(self):
        return [self.images[0]]
    
    def coolimage(self):
        return self.stillimage()

    def deadimage(self):
        self.image = pygame.transform.scale(pygame.image.load(f'assets/npc/{self.name}/dead.png'), self.size)
        return [self.image]

    def breathimage(self):
        return [self.images[0]]
    
    def state_update(self):
      
        if self.attacking_method == AttackMethod.WEAPON:
            self.attacking = self.weapon.attacking
        if self.check and not self.player.weapon.startattack and not self.player.weapon.cooling:
            self.check = False

        if self.state == State.ATTACKING:
            if self.is_attack_over():
                self.ChangeActionTo(State.COOLING)
                self.cooling = True  
                self.clock = self.cd
            if self.index in self.attackingindex:
                self.attacking_music()
                self.attacking = True
                self.hasattacked = False

        elif self.state == State.HIT and self.is_hit_over():
            self.ChangeActionTo(self.previous_state)
        
        elif self.state == State.APPEAR and self.is_appear_over():
            self.ChangeActionTo(State.ALIVE)
        else:
            self.extra_state_update()
            
    def extra_state_update(self):

        if self.state == State.COOLING:
            if self.is_cool_over():
                self.ChangeActionTo(State.ALIVE)
        elif self.state == State.ALIVE and self.can_attack():
            self.ChangeActionTo(State.ATTACKING)

    def ChangeActionTo(self, state):
        if state == State.ATTACKING:
            self.attack()
            self.images = self.attackimage()
        elif state == State.COOLING or self.state == State.TALKING:
            self.images = self.coolimage()
        elif state == State.STILL:
            if self.state != State.FROZEN and self.state != State.HIT:
                self.previous_state = self.state
            self.images = self.stillimage()
        elif state == State.HIT:
            self.images = self.hitimage()
            self.previous_state = self.state
        elif state == State.ALIVE:
            self.images = self.moveimage()
        elif state == State.DEAD:
            self.images = self.deadimage()
        else:
            self.extra_state_change(state)
                
        self.state = state
        self.index = 0
        self.image = self.images[self.index]
        self.len = len(self.images)

    def extra_state_change(self, state):
        pass
            
    def is_attack_over(self):
        return True
    
    def is_appear_over(self):
        return True
    
    def is_cool_over(self):
        if self.clock > 0:
            self.clock -= 1
            return False
        else:
            return True
    
    def is_hit_over(self):
        return True

    def can_attack(self):
        return self.dis <= self.attackrange

    def set_to_still(self):
        pass

    def beingattacked(self, atk, buff):
        self.hp -= atk * self.defence
        if self.hp <= 0 :
            self.ChangeActionTo(State.DEAD)
        elif self.state != State.SUMMON and self.state != State.SPELL:
            if self.state != State.STILL and self.state != State.FROZEN and self.state != State.ATTACKING and self.state != State.HIT: 
                self.ChangeActionTo(State.HIT)
            for debuff in buff:
                if not debuff in self.debuff:
                    if not(debuff == Debuff.REPELL and self.state == State.ATTACKING):
                        self.debuff.append(debuff)
                    if debuff == Debuff.BURNING:
                        self.burning = True
                        self.effect.add(Flame(self, self.window, self.bgm, BuffSettings.flame, 60, self.proportion))
                        if self.state == State.FROZEN:
                            self.ChangeActionTo(self.previous_state)
                            self.debuff.remove(Debuff.FROZEN)
                            for effect in self.effect:
                                if isinstance(effect, Frozen):
                                    self.effect.remove(effect)
                                    break
                    elif debuff == Debuff.FROZEN and not self.burning:
                        self.effect.add(Frozen(self, self.window, self.bgm, BuffSettings.frozen, 50, self.proportion))
                        if self.state != State.STILL and self.state != State.HIT:
                            self.previous_state = self.state
                        self.state = State.FROZEN
                        if self.dir == -1:
                            self.image = pygame.transform.flip(self.image, True, False)
                    elif debuff == Debuff.DIZZY and self.state != State.FROZEN:
                        self.effect.add(Dizzy(self, self.window, self.bgm, BuffSettings.dizzy, 30, self.proportion))
                        self.ChangeActionTo(State.STILL)

    def appear_music(self):
        pass

    def attack_music(self):
        pass   

    def attacking_music(self):
        pass

    def get_attack_pos(self):
        return self.rect.center
        
    def pos_update(self):
        
        if (not self.NeedDetect or (self.NeedDetect and self.dis <= MonsterSettings.DetectingRange)):
            if not self.startattack:
                self.appear_music()
                self.startattack = True
          
        if self.startattack:
            if self.dis == 0:
                self.dx, self.dy = 0, 0
            elif self.dis <= self.speed:
                self.dx, self.dy = self.dx + (self.target[0] - self.attack_pos[0]), self.dy + (self.target[1] - self.attack_pos[1])
            else:
                self.dx, self.dy = (self.dx + (self.target[0] - self.attack_pos[0]) / self.dis * self.speed, 
                                    self.dy + (self.target[1] - self.attack_pos[1]) / self.dis * self.speed)
             
        if self.target[0] < self.attack_pos[0]: 
            self.dir = -1
        elif self.target[0] > self.attack_pos[0]:
            self.dir = 1 
        
    def debuff_update(self):

        for debuff in self.debuff:
            if debuff == Debuff.BURNING:
                for effect in self.effect:
                    if isinstance(effect, Flame):
                        if effect.time % 20 == 0:
                            self.hp -=40
                            if self.hp <= 0:
                                self.ChangeActionTo(State.DEAD)
                                effect.bgm.burning.stop()
                        break
            elif debuff == Debuff.REPELL and self.state != State.ATTACKING:
                self.dx -= self.dir * 20
                self.clicktock(3)
                if not self.isclocking:
                    self.debuff.remove(Debuff.REPELL)

    def is_awake(self):
        return True
    
    def update(self):
        self.dx, self.dy = 0, 0
        if self.state != State.DEAD and self.is_awake():
            self.attack_pos = self.get_attack_pos()
            self.set_target(self.location)
            self.dis = math.hypot(self.target[0] - self.attack_pos[0], self.target[1] - self.attack_pos[1])
            self.state_update()
            self.debuff_update()
        self.image_update()
        if self.state == State.ALIVE or self.state == State.SPELL:
            self.pos_update()
        self.rect = self.rect.move(self.dx, self.dy)

    def draw(self, dx=0, dy=-10):
        self.window.blit(self.image, self.rect)
        if self.state != State.DEAD:
            pygame.draw.rect(self.window, Color.Red, [self.rect.centerx + dx - 30, self.rect.y + dy, self.hp*self.coord, 10], 0)
            if self.weapon != None and self.can_draw_weapon: 
                self.weapon.update()
                self.weapon.draw()    
            self.window.blit(self.namerender, (self.rect.centerx - self.namerender.get_width()/2, 
                                               self.rect.y - NPCSettings.Fontsize + dy))
        self.draw_effect()

    def draw_effect(self, dx=0, dy=0):      
        for effect in self.effect:
            if effect.isdisappear():
                if effect.debuff != None:
                    if effect.debuff == Debuff.DIZZY or effect.debuff == Debuff.FROZEN:
                        self.ChangeActionTo(self.previous_state)
                    if effect.debuff == Debuff.BURNING:
                        self.burning = False
                    self.debuff.remove(effect.debuff)
                self.effect.remove(effect)
                continue
            effect.update()
            if isinstance(effect, Explode) or self.state != State.DEAD:
                effect.draw(dx, dy)
            elif self.state == State.DEAD:
                self.effect.remove(effect)
                if isinstance(effect, Flame):
                    effect.bgm.burning.stop()
            if effect.debuff == Debuff.DIZZY or effect.debuff == Debuff.FROZEN:
                self.set_to_still() 

class Knight(Monster):
    
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__( x, y, name, window, difficulty, player, bgm, paths)
        self.weapon = Sword(self.window, self, GamePath.Sword, 65, 55, self.bgm)
        self.attacking_method = AttackMethod.WEAPON
        self.money = (2, 1)
        self.attackingindex = [0]
        self.skill = None
        self.set_attr(100, 0.9, 3, 10, 0.3, 30,)

    def attack(self):
        self.skill = 'cut'
        
    def is_attack_over(self):
        if not self.weapon.startattack:
            self.skill = None
            return True
        else:
            return False
    
    def appear_music(self):
        self.bgm.addsound('roar')

    def set_to_still(self):
        self.skill = None

class Tauren(Knight):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths)
        self.money = (4, 3)
        self.set_attr(700, 0.5, 3, 20, 0.3, 50)

class Ghour(Knight):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths)
        self.money = (3, 2)
        self.set_attr(550, 0.65, 3, 15, 0.3, 35)

class Zombie(Knight):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths)
        self.set_attr(300, 0.9, 3, 13, 0.5, 40)
        self.money = (2, 2)
        self.weapon = Claw(self.window, self, GamePath.Claw, 75, 65, self.bgm)
        self.can_draw_weapon = False
    
    def attack(self):
        self.skill = 'cut'
        self.can_draw_weapon = True
        
    def is_attack_over(self):
        if not self.weapon.startattack:
            self.skill = None
            self.can_draw_weapon = False
            return True
        else:
            return False

class Miner(Zombie):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths)
        self.set_attr(400, 0.7, 3, 20, 0.5, 80)
        self.money = (3, 2)
        self.buff = [Debuff.REPELL]

class FireWorm(Monster):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__( x, y, name, window, difficulty, player, bgm, paths)
        self.attacking_method = AttackMethod.SACRIFICE
        self.money = (1, 0)
        self.attackingindex = [0]
        self.set_attr(150, 1, 8, 75, 0.3, 0)

    def attack(self):
        self.ChangeActionTo(State.COOLING)
        self.clock = 5

    def is_cool_over(self):
        if self.clock > 0:
            self.clock -= 1
        else:
            self.attacking = True
            self.ChangeActionTo(State.DEAD)
            self.effect.add(Explode(self, self.window, self.bgm, BuffSettings.fire_explode))
            self.bgm.addsound('explode')
        return False
    
    def set_dead(self):
        for effect in self.effect:
            if isinstance(effect, Explode) and effect.isdisappear():
                self.completelydead = True
        if not self.effect and self.state == State.DEAD:
            self.completelydead = True

class Iceworm(FireWorm):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths)
        self.money = (2, 0)
        self.set_attr(150, 1, 7, 65, 0.3, 0)
        self.buff = [Debuff.FROZEN]
    
    def is_cool_over(self):
        if self.clock > 0:
            self.clock -= 1
        else:
            self.attacking = True
            self.ChangeActionTo(State.DEAD)
            self.effect.add(Explode(self, self.window, self.bgm, BuffSettings.ice_explode))
        return False

class Dragon(Monster):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__( x, y, name, window, difficulty, player, bgm, paths)
        self.bullettype = BulletType.FireBall
        self.money = (4, 3)
        self.attackingindex = [2.1]
        self.attackrange = MonsterSettings.BulletRange
        self.attacking_method = AttackMethod.BULLET
        self.set_attr(250, 0.6, 5, 0, 0.3, 100)
    
    def attackimage(self):
        return [pygame.transform.scale(pygame.image.load(f'assets/npc/{self.name}/attack/{index}.png'), self.size) for index in range(1, 6)]

    def is_attack_over(self):
        if self.index >= self.len - 1:
            self.hasattacked = False
            self.attacking = False
            return True
        else:
            return False

    def coolimage(self):
        return self.stillimage()

    def stillimage(self):
        return self.original
    
    def moveimage(self):
        return self.original
    
    def hitimage(self):
        return self.original

    def attack(self):
        self.angle = [((self.target[0]-self.rect.centerx)/self.dis, (self.target[1]-self.rect.centery)/self.dis)]
    
class Shaman(Dragon):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths)
        self.money = (3, 1)
        self.bullettype = BulletType.Fire_Yellow
        self.attackingindex = [0]
        self.set_attr(50, 1, 5, 0, 0.3, 90)
    
    def attackimage(self):
        return [pygame.transform.scale(pygame.image.load(f'assets/npc/{self.name}/attack/{index}.png'), self.size) for index in range(1, 2)]

    def stillimage(self):
        return [self.original[0]]

class Wizard(Shaman):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths)
        self.bullettype = BulletType.Fire_Pink
        self.set_attr(550, 0.5, 4, 0, 0.2, 70)

    def attack(self):
        self.angle = []
        for _ in range(3):
            target = (self.target[0], self.target[1] + uniform(-350, 350))
            dis = math.hypot(target[0]-self.rect.centerx, target[1]-self.rect.centery)
            self.angle.append(((target[0]-self.rect.centerx)/dis, (target[1]-self.rect.centery)/dis))

    def coolimage(self):
        return self.attackimage()

class Simian(Dragon):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths)
        self.money = (2, 1)
        self.bullettype = BulletType.Mini_Blue
        self.attackingindex = [2.1]
        self.set_attr(300, 0.8, 5, 0, 0.3, 80)
    
    def attackimage(self):
        return [pygame.transform.scale(pygame.image.load(f'assets/npc/{self.name}/attack/{index}.png'), self.size) for index in range(1, 6)]

    def stillimage(self):
        return [self.original[0]]

class Mummy(Dragon):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths)
        self.money = (2, 3)
        self.bullettype = BulletType.Mini_Black
        self.attackingindex = [0]
        self.set_attr(650, 0.6, 3, 0, 0.3, 70)
    
    def attackimage(self):
        return [self.original[0]]

    def stillimage(self):
        return [self.original[0]]
   
class Elite(Monster):

    def __init__(self, x, y, name, window, difficulty, player, bgm, paths, index_msg):
        super().__init__( x, y, name, window, difficulty, player, bgm, paths)
        self.tag = 'elite'
        self.index_msg = index_msg
        self.attackrange = MonsterSettings.EliteRange
        self.proportion = 1.5
    
    def attacking_music(self):
        self.bgm.addsound(f'{self.name}attack')
        
    def attackimage(self):
        return [pygame.transform.scale(pygame.image.load(f'./assets/npc/{self.name}/attack/{index}.png'), self.size) 
                for index in range(1, self.index_msg['attack'])] 
    
    def hitimage(self):
        return [pygame.transform.scale(pygame.image.load(f'./assets/npc/{self.name}/hit/{index}.png'), self.size) 
                for index in range(1, self.index_msg['hit'])] 
    
    def stillimage(self):
        return [pygame.transform.scale(pygame.image.load(f'./assets/npc/{self.name}/idle/{index}.png'), self.size) 
                for index in range(1, self.index_msg['idle'])] 
    
    def coolimage(self):
        return self.stillimage()
    
    def deadimage(self):
        return [pygame.transform.scale(pygame.image.load(f'./assets/npc/{self.name}/dead/{index}.png'), self.size) 
                for index in range(1, self.index_msg['dead'])] 
    
    def moveimage(self):
        return [pygame.transform.scale(pygame.image.load(f'./assets/npc/{self.name}/run/{index}.png'), self.size) 
                for index in range(1, self.index_msg['run'])]

    def is_attack_over(self):
        return math.floor(self.index) == self.len - 1
     
    def is_hit_over(self):
        return math.floor(self.index) == self.len - 1

    def set_dead(self):
        if self.index == self.len - 1:
            self.completelydead = True
    
    def draw(self):
        self.window.blit(self.image, self.rect)
        if self.state != State.DEAD:
            pygame.draw.rect(self.window, (255, 0, 0), [self.rect.centerx - 50 , self.rect.y + 60, self.hp*self.coord, 10], 0)  
            self.window.blit(self.namerender, (self.rect.centerx - self.namerender.get_width()/2, 
                                               self.rect.y - NPCSettings.Fontsize + 60))
        self.draw_effect(0, 30)

class Monk(Elite):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths, index_msg):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths, index_msg)
        self.set_attr(600, 0.6, 6, 35, 0.5, 40)
        self.money = (6, 6)
        self.attackingindex = [5, 13]
        self.attacking_method = AttackMethod.FIST
        self.coord = 100 / self.hp
        self.buff = [Debuff.REPELL]

class Melee(Elite):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths, index_msg):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths, index_msg)
        self.set_attr(1400, 0.7, 6, 50, 0.5, 90)
        self.money = (10, 10)
        self.attackingindex = [7]
        self.attacking_method = AttackMethod.FIST
        self.coord = 100 / self.hp
        self.buff = [Debuff.BURNING]

class Ninja(Elite):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths, index_msg):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths, index_msg)
        self.set_attr(1100, 0.5, 6, 40, 0.5, 40)
        self.money = (8, 8)
        self.attackingindex = [14, 21]
        self.attacking_method = AttackMethod.FIST
        self.coord = 100 / self.hp
        self.buff = [Debuff.FROZEN]

class Ghost(Elite):
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths, index_msg):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths, index_msg)
        self.state = State.APPEAR
        self.set_attr(2000, 0.4, 5, 200, 0.5, 90)
        self.hp_coord = 100 / self.hp
        self.attacking_method = AttackMethod.FIST
        self.money = (0, 0)
        self.attackingindex = [6]
        self.proportion = 1
        self.tag = 'ghost'
        self.buff = [Debuff.DIZZY]
    
    def is_appear_over(self):
        return math.floor(self.index) == self.len - 1

    def get_attack_pos(self):
        return (self.rect.centerx, self.rect.centery + 100) 
    
    def can_flip(self):
        return self.dir == 1
    
    def attack(self):
        self.bgm.addsound('scream')
    
    def attacking_music(self):
        pass

    def draw(self):
        self.window.blit(self.image, self.rect)
        if self.state != State.DEAD:

            pygame.draw.rect(self.window, (255, 0, 0), [self.rect.centerx - 50 , self.rect.centery, self.hp*self.coord, 10], 0)  
            self.window.blit(self.namerender, (self.rect.centerx - self.namerender.get_width()/2, 
                                               self.rect.y - NPCSettings.Fontsize + 200))
        
        self.draw_effect(0, 60)

class Fort(Elite):
     
    def __init__(self, x, y, name, window, difficulty, player, bgm, paths, index_msg):
        super().__init__(x, y, name, window, difficulty, player, bgm, paths, index_msg)
        self.attacking_method = AttackMethod.BULLET
        self.bullettype = BulletType.Fire_Red
        self.attackrange = MonsterSettings.WholeRange
        self.tag = 'fort'
        self.can_fire = False
        self.attackingindex =  [11]
        self.money = (0, 0)
        self.set_attr(1700, 0.3, 0, 0, 0.5, 45)
        self.coord = 100 / self.hp
    
    def pos_update(self):
        pass
    
    def is_awake(self):
        return self.can_fire
    
    def attacking_music(self):
        pass
    
    def beingattacked(self, atk, buff):
        if self.can_fire:
            self.hp -= atk * self.defence
            if self.hp <= 0:
                self.ChangeActionTo(State.DEAD)
        
    def moveimage(self):
        return self.stillimage()
    
    def attack(self):
        self.angle = [((self.player.rect.centerx-self.rect.centerx)/self.dis, (self.player.rect.centery-self.rect.centery)/self.dis)]
        
    def draw(self):
        self.window.blit(self.image, self.rect)
        if self.state != State.DEAD and self.can_fire:
            pygame.draw.rect(self.window, Color.Grey, [self.rect.centerx - 50 , self.rect.centery - 50, self.hp*self.coord, 10], 0)  
