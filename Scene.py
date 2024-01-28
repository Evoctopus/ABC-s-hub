# -*- coding:utf-8 -*-

import pygame
import Maps
from random import randint

from enum import Enum
from Settings import *
from NPCs import *
from Boss import *
from PopUpBox import *
from Portal import *
from BgmPlayer import *
from Monster import *
from Special import *

class Scene():
    def __init__(self, window, player, bgm):
        self.bgm = bgm
        self.player = player
        self.playerweapon = player.weapon
        self.type = None
        self.map = None
        self.obstacles = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.box = None
        self.can_renderbox = False
        self.battling = False
        self.Coin = pygame.sprite.Group()
        self.dead = pygame.sprite.Group()
        self.house = pygame.sprite.Group()
        self.special_block = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.window = window
        self.difficulty = 1
        self.width = WindowSettings.width
        self.height = WindowSettings.height
        self.buddha = None
        self.cherry_tree = None
        self.can_buy = False

    def trigger_dialog(self, npc):
        self.box = DialogBox(self.window, npc)

    def end_dialog(self):
        self.box = None

    def trigger_shop(self, npc):
        self.box = ShoppingBox(self.window,npc,self.player)

    def end_shop(self):
        self.box = None

    def trigger_battle(self):
        self.battling = True
        for _ in range(self.difficulty * 3):
            rand_num = randint(1, 3)
            if rand_num == 1:
                self.gen_monsters(randint(0, 1280), -40)
            elif rand_num == 2:
                self.gen_monsters(randint(0, 1280), 760)
            elif rand_num == 3:
                self.gen_monsters(-40, randint(0, 720))

        self.gen_elite()
        self.difficulty += 1
        # 生成许多怪物
    
    def detectnpc(self):
        for npc in self.npcs:
            if pygame.sprite.collide_rect_ratio(1.5)(self.player, npc):
                npc.can_talk = True
                self.can_talk = True
                if self.box == None:
                    if npc.type == NPCType.DIALOG:
                        self.trigger_dialog(npc)
                    if npc.type == NPCType.SHOP:
                        self.trigger_shop(npc)
            else:
                npc.can_talk = False

        if not self.can_talk: 
            self.box = None
    
    def detectmonster(self):
        if self.playerweapon.skill != 'disappear':
            object = pygame.sprite.spritecollide(self.playerweapon, self.monsters, False)
            if object and self.playerweapon.attacking:
                for monster in object:
                    if not monster.check and monster.state != State.DEAD:
                        if monster.tag != 'ghost' or pygame.sprite.collide_mask(self.playerweapon, monster):
                            monster.check = True
                            monster.beingattacked(self.playerweapon.atk, self.playerweapon.buff)
        elif self.playerweapon.swordplay != None:
            object = pygame.sprite.spritecollide(self.playerweapon.swordplay, self.monsters, False)
            if object and self.playerweapon.swordplay.index in self.playerweapon.playing_index:
                for monster in object:
                    monster.beingattacked(self.playerweapon.atk, self.playerweapon.buff)
    
    def detectplayer(self):
        for each in self.monsters:
            if each.attacking_method == AttackMethod.WEAPON:
                if each.weapon.attacking and pygame.sprite.collide_rect(self.player, each.weapon):
                    if not each.weapon.hasattacked:
                        self.player.beingattacked(each.atk, each.buff)
                        each.weapon.hasattacked = True
            elif each.attacking_method == AttackMethod.FIST or each.attacking_method == AttackMethod.SACRIFICE:
                if each.attacking and pygame.sprite.collide_rect(self.player, each):
                    if not each.hasattacked:
                        self.player.beingattacked(each.atk, each.buff)
                        each.hasattacked = True
            elif each.attacking_method == AttackMethod.BULLET:
                #print(each.attacking, each.hasattacked)
                if each.attacking and not each.hasattacked:
                    each.hasattacked = True
                    for angle in each.angle:
                        if each.bullettype == BulletType.FireBall:
                            self.bullets.add(Bullet(each.rect.centerx, each.rect.centery, self.window, 
                                                    self.difficulty, angle=angle, bgm=self.bgm, paths=BulletSettings.fireball))
                        elif each.bullettype == BulletType.Fire_Red:
                            self.bullets.add(Bullet(each.rect.centerx, each.rect.centery, self.window, 
                                                    self.difficulty, angle=angle, bgm=self.bgm, paths=BulletSettings.redfire, canhit=False))
                        elif each.bullettype == BulletType.Fire_Yellow:
                            self.bullets.add(Bullet(each.rect.centerx, each.rect.centery, self.window, 
                                                    self.difficulty, angle=angle, bgm=self.bgm, paths=BulletSettings.yellowfire, canhit=False))
                        elif each.bullettype == BulletType.Fire_Pink:
                            self.bullets.add(Bullet(each.rect.centerx, each.rect.centery, self.window, 
                                                    self.difficulty, angle=angle, bgm=self.bgm, paths=BulletSettings.pinkfire, canhit=False))
                        elif each.bullettype == BulletType.Mini_Blue:
                            self.bullets.add(Bullet(each.rect.centerx, each.rect.centery, self.window, 
                                                    self.difficulty, angle=angle, bgm=self.bgm, paths=BulletSettings.miniblue, canhit=False))
                        elif each.bullettype == BulletType.Mini_Black:
                            self.bullets.add(Bullet(each.rect.centerx, each.rect.centery, self.window, 
                                                    self.difficulty, angle=angle, bgm=self.bgm, paths=BulletSettings.miniblack, canhit=False))
                        
        for each in self.bullets:
            if pygame.sprite.collide_mask(self.playerweapon, each) and self.playerweapon.attacking:
                each.disappear = True
            elif pygame.sprite.collide_mask(self.player, each) and not each.explode:
                each.attack()
                self.player.beingattacked(each.atk, each.buff)
            
    def detectportal(self):
        if not self.battling: 
            for portal in self.portals:
                if pygame.sprite.collide_rect(self.player, portal):
                    portal.blink = True
                    self.can_flush = True
                    self.goto = portal.goto
                else:
                    portal.blink = False
    
    def detectbuddha(self):
        if pygame.sprite.collide_rect_ratio(2)(self.player, self.buddha) and not self.battling:
            self.buddha.blink = True
            self.can_start_battle = True
        else:
            self.buddha.blink = False

    def detectcollide(self):

        if ((self.buddha != None and pygame.sprite.collide_mask(self.player, self.buddha)) or 
        (self.cherry_tree != None and pygame.sprite.collide_rect(self.player,self.cherry_tree))):
            self.player.rect = self.player.rect.move(-self.player.dx, -self.player.dy)
        else:
            for each in self.obstacles:
                if pygame.sprite.collide_mask(self.player, each):
                    self.player.rect = self.player.rect.move(-self.player.dx, -self.player.dy)
            
    def gen_npcs(self):
        pass

    def gen_monsters(self):
        pass

    def update_camera(self, player):
        pass

    def choose_item(self, item_num, slow_key):
        if slow_key['W'] :
                self.box.selectedID = max(0,self.box.selectedID-1)
        elif slow_key['S']:
            self.box.selectedID = min(item_num,self.box.selectedID + 1)
        elif slow_key['E']:
            if self.box.selectedID == item_num:
                self.box.npc.state = State.ALIVE
                self.end_shop()
                self.player.state = State.ALIVE
                self.can_renderbox = False
                self.can_buy = False
            elif self.can_buy:
                self.box.buy()
            else:
                self.can_buy = True

    def update(self, key, slow_key):
        self.can_talk = False
        self.can_start_battle = False
        self.can_flush = False
        self.detectmonster()
        self.detectnpc()
        self.detectplayer()
        self.detectportal()
        self.detectcollide()
        if self.buddha != None:
            self.detectbuddha()
        self.update_camera(self.player)
        self.can_flush &= not self.battling
        if slow_key['E']:
            if self.can_talk:
                self.can_renderbox = True
                self.box.npc.state = State.TALKING
                self.player.state = State.TALKING
                if self.box.npc.type == NPCType.DIALOG:
                    self.box.index += 1
                    if self.box.index == self.box.len:
                        self.box.npc.state = State.ALIVE
                        self.end_dialog()
                        self.player.state = State.ALIVE
                        self.can_renderbox = False
            elif self.can_flush:
                event = pygame.event.Event(Event.FlushScene, {'GOTO': self.goto})
                pygame.event.post(event)
            elif self.can_start_battle:
                self.bgm.addsound('bell')
                self.trigger_battle()
        
        if self.can_renderbox and self.box.npc.type == NPCType.SHOP:
            if self.box.npc.name != 'blacksmith':
                self.choose_item(3, slow_key)
            else:
                self.choose_item(4, slow_key)

        for each in self.npcs:
            each.update()
        
        if self.monsters:
            for each in self.monsters:
                if not each.completelydead:
                    each.update()
                else:
                    self.dead.add(each)
                    self.monsters.remove(each)
                    for _ in range(each.money[0]):
                        self.Coin.add(Coin(self.window, self.player, 'goldcoin', randint(1, 360)*math.pi/180, self.bgm, each.rect.center))
                    for _ in range(each.money[1]):
                        self.Coin.add(Coin(self.window, self.player, 'silvercoin', randint(1, 360)*math.pi/180, self.bgm, each.rect.center)) 
        else:
            self.battling = False
            self.player.shield_hp = self.player.shield_hp_limit

        for each in self.Coin:
            if not each.disappear:
                each.update()
            else:
                self.Coin.remove(each)

        for each in self.bullets:
            each.update()
            if each.disappear or not each.rect.centerx in range(0, 1280) or not each.rect.centery in range(0, 720):
                self.bullets.remove(each)
             
    def render(self):
        
        self.map_render()
        self.obstacles.draw(self.window)

        for each in self.dead:
            if each.disappear:
                self.dead.remove(each)
            else:
                each.draw()
        for each in self.portals:
            each.draw()

        if self.buddha != None:
            self.buddha.draw()

        for each in self.npcs:
            each.draw()
        for each in self.bullets:
            each.draw()
        for each in self.monsters:
            each.draw()
        for each in self.Coin:
            each.draw()

    def map_render(self):
        pass
    
class StartMenu(Scene):
    def __init__(self, window,player,bgm):
        ##### Your Code Here ↓ #####
        super().__init__(window, player, bgm)
        
        self.type = SceneType.MENU
        self.bg = pygame.image.load(GamePath.menu)
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))

        self.font = pygame.font.Font(None,MenuSetting.textSize)
        self.text = self.font.render("Genshen Start ! (press E)",True,(255,255,255))

        self.textRect = self.text.get_rect(center = (WindowSettings.width//2,WindowSettings.height - 50))
        self.blinkTimer = 0
    
    def render(self):
        ##### Your Code Here ↓ #####
        self.window.blit(self.bg,(0,0))

        self.blinkTimer += 1 
        if self.blinkTimer >= MenuSetting.blinkInterval:
            self.window.blit(self.text,self.textRect)
            if self.blinkTimer >= MenuSetting.blinkInterval*2:
                self.blinkTimer = 0
        
class Introduction(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(window, player, bgm)
        self.type = SceneType.INTRODUCTION

        self.bg = pygame.image.load(GamePath.introudction)
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width,WindowSettings.height))

        self.font =pygame.font.Font(None,MenuSetting.textSize)

        self.text = self.font.render("please press E to continue",True,(0,0,0))

        self.textRect = self.text.get_rect(center = (WindowSettings.width//2,WindowSettings.height - 50))
        self.blinkTimer = 0

        a = pygame.font.SysFont('alibabapuhuiti245light',70)
        b = pygame.font.SysFont('alibabapuhuiti245light',40)
        self.words = []
        self.words.append(a.render('Background Introduction',True,(0,0,0)))
        self.words.append(b.render("        This is a world full of monsters, which are divided into levels.",True,(0,0,0)))
        self.words.append(b.render("        You need to defeat the monster in the following three scencs",True,(0,0,0)))
        self.words.append(b.render("        ' Emerald Wood ', ' Thundering Ice Peaks ' and ' Infernal Isle '",True,(0,0,0)))
        self.words.append(b.render("        Then, you'll get coin from the monster so that you can improve your own attributes",True,(0,0,0)))
        self.words.append(b.render('        When all your attributes are elevated to a certain value',True,(0,0,0)))
        self.words.append(b.render('        You can chanllenge the Demon King',True,(0,0,0)))
        self.words.append(b.render('        When you defeat the Demon King , you win the game and the game ends',True,(0,0,0)))

    def render(self):
        self.window.blit(self.bg,(0,0))
        self.blinkTimer += 1 
        if self.blinkTimer >= MenuSetting.blinkInterval:
            self.window.blit(self.text,self.textRect)
            if self.blinkTimer >= MenuSetting.blinkInterval*2:
                self.blinkTimer = 0
        self.window.blit(self.words[0],(WindowSettings.width//4 + 50,1))
        for i in range(1,len(self.words)):
            self.window.blit(self.words[i],(10,40 + 75*i))

class CityScene(Scene):

    def __init__(self, window, player, bgm):
        super().__init__(window, player, bgm)
        self.type = SceneType.CITY
        self.cameraX = 360
        self.cameraY = 160

    def gen_Map(self):

        self.map = Maps.gen_city_map()
        self.gen_npcs()
        self.obstacles = Maps.gen_city_obstacle()
        self.cherry_tree = Maps.Cherry_blossom_tree(self.window)
        self.portals.add(Portal(965, 1000, 'dangerous', self.window, 'Thundering Ice Peaks', SceneType.ICE, True))
        self.portals.add(Portal(965, 45, 'boss', self.window, 'Shadowrealm Castle', SceneType.BOSS, True))
        self.portals.add(Portal(45, 525, 'dangerous', self.window, 'Emerald Woods', SceneType.WILD, True))
        self.portals.add(Portal(1825, 525, 'dangerous', self.window, 'Infernal Isle', SceneType.LAVA, True))
           
    def get_width(self):
        return WindowSettings.width * WindowSettings.outdoorScale

    def get_height(self):
        return WindowSettings.height * WindowSettings.outdoorScale
    
    def update_camera(self, player):
        if player.rect.x > WindowSettings.width / 4 * 3:
            self.cameraX += player.speed
            if self.cameraX < self.get_width() - WindowSettings.width:
                player.rect = player.rect.move(-player.dx,0)
            else:
                self.cameraX = self.get_width() - WindowSettings.width
        elif player.rect.x < WindowSettings.width / 4:
            self.cameraX -= player.speed
            if self.cameraX > 0:
                player.rect = player.rect.move(-player.dx, 0)
            else:
                self.cameraX = 0
        if player.rect.y > WindowSettings.height / 4 * 3:
            self.cameraY += player.speed
            if self.cameraY < self.get_height() - WindowSettings.height:
                player.rect = player.rect.move(0,-player.dy)
            else:
                self.cameraY = self.get_height() - WindowSettings.height
        elif player.rect.y < WindowSettings.height / 4:
            self.cameraY -= player.speed
            if self.cameraY > 0:
                player.rect = player.rect.move(0,-player.dy)
            else:
                self.cameraY = 0

        for obstacle in self.obstacles:
            obstacle.rect.topleft = (obstacle.before_rect[0] - self.cameraX, obstacle.before_rect[1] - self.cameraY)

        for portal in self.portals:
            portal.rect.topleft = (portal.before_rect[0]-self.cameraX,portal.before_rect[1] - self.cameraY)
        
        for npc in self.npcs:
            npc.rect.topleft = (npc.before_rect[0]-self.cameraX, npc.before_rect[1] - self.cameraY)

        self.cherry_tree.rect.topleft = (self.cherry_tree.before_rect[0] - self.cameraX,self.cherry_tree.before_rect[1] - self.cameraY)
    
    def gen_npcs(self):
        self.npcs.add(ShopNPC(175,250, 'glory_goddess',self.window,self.player,self.bgm,GamePath.glory_goddess,0))
        self.npcs.add(ShopNPC(525,150,"blacksmith",self.window,self.player,self.bgm,GamePath.Blacksmith,0))
        self.npcs.add(DialogNPC(275,250,"prophet",self.window,self.player,self.bgm,GamePath.Prophet,0))
        self.npcs.add(ShopNPC(1600,345,"Monster_Hunter",self.window,self.player,self.bgm,GamePath.Monster_Hunter,0))
        self.npcs.add(ShopNPC(1450,150,"Special_Merchant" ,self.window,self.player,self.bgm,GamePath.Special_Merchant,0))
        self.npcs.add(DialogNPC(550,850,"archer" ,self.window,self.player,self.bgm,GamePath.Archer))
        self.npcs.add(DialogNPC(1350,850,"singer" ,self.window,self.player,self.bgm,GamePath.Singer))

    def map_render(self):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                (SceneSettings.tileWidth * i - self.cameraX, SceneSettings.tileHeight * j - self.cameraY))
        self.cherry_tree.update()

    def get_cameraX(self):
        return self.cameraX
    
    def get_cameraY(self):
        return self.cameraY
    
class WildScene(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(window, player, bgm)
        self.type = SceneType.WILD
        self.cd = 100
        self.buddha = Buddha(WindowSettings.width / 2, WindowSettings.height / 2, 'buddha_wild', self.window, 'Mysterious stone statues')

    def gen_Map(self):
        self.map = Maps.gen_wild_map()
        self.obstacles = Maps.gen_wild_obstacle()
        self.portals.add(Portal(1180, 325, 'direction', self.window, 'THE FALLEN TOWN', SceneType.CITY))
        #self.npcs.add(DialogNPC(NPCSettings.npcstartx, NPCSettings.npcstarty, 'maqix', self.window, self.player, self.bgm, GamePath.npc))
    
    def gen_monsters(self, x, y):
        rand_num = randint(0, self.difficulty) % 4
        if rand_num == 0:
            self.monsters.add(Knight(x, y, 'knight', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.knight))
        elif rand_num == 1:
            self.monsters.add(Knight(x, y, 'soldier', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.soldier))
        elif rand_num == 2:
            self.monsters.add(Shaman(x, y, 'shaman', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.shaman))
        elif rand_num == 3:
            self.monsters.add(Zombie(x, y, 'zombie', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.zombie))

    def gen_elite(self):
        if self.difficulty == 3:
            self.monsters.add(Monk(-150 , WindowSettings.height // 2, 'Monk', self.window, 
                                self.difficulty, self.player, self.bgm, MonsterSettings.Monk, EliteSetting.Monk))

    def map_render(self):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                (SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))

class LavaScene(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(window, player, bgm)
        self.type = SceneType.LAVA
        self.buddha = Buddha(WindowSettings.width / 2, WindowSettings.height / 2, 'buddha_lava', self.window, 'Mysterious stone statues')

    def gen_Map(self):
        self.map = Maps.gen_lava_map()
        self.obstacles = Maps.gen_lava_obstacle()
        self.portals.add(Portal(45, 325, 'direction', self.window, 'THE FALLEN TOWN', SceneType.CITY, flip=True))

    def gen_monsters(self, x, y):
        rand_num = randint(0, self.difficulty) % 5
        if rand_num == 0:
            self.monsters.add(Tauren(x, y, 'tauren', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.tauren))
        elif rand_num == 1:
            self.monsters.add(Dragon(x, y, 'dragon', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.dragon))
        elif rand_num == 2:
            self.monsters.add(FireWorm(x, y, 'fireworm', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.fireworm))
        elif rand_num == 3:
            self.monsters.add(Mummy(x, y, 'mummy', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.mummy))
        elif rand_num == 4:
            self.monsters.add(Wizard(x, y, 'wizard', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.wizard))

    def gen_elite(self):
        if self.difficulty == 4:
            self.monsters.add(Melee(1430 , WindowSettings.height // 2, 'Melee', self.window, 
                                self.difficulty, self.player, self.bgm, MonsterSettings.Melee, EliteSetting.Melee))

    def map_render(self):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                (SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
      
class IceScene(Scene):

    def __init__(self, window, player, bgm):
        super().__init__(window, player, bgm)
        self.type = SceneType.ICE
        self.buddha = Buddha(WindowSettings.width / 2, WindowSettings.height / 2, 'buddha_ice', self.window, 'Mysterious stone statues')

    def gen_Map(self):
        self.map = Maps.gen_ice_map()
        self.obstacles = Maps.gen_ice_obstacle()
        self.portals.add(Portal(605, 45, 'direction', self.window, 'THE FALLEN TOWN', SceneType.CITY))

    def gen_monsters(self, x, y):
        rand_num = randint(0, self.difficulty) % 4
        if rand_num == 0:
            self.monsters.add(Simian(x, y, 'simian', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.simian))
        elif rand_num == 1:
            self.monsters.add(Miner(x, y, 'miner', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.miner))
        elif rand_num == 2:
            self.monsters.add(Iceworm(x, y, 'iceworm', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.iceworm))
        elif rand_num == 3:
            self.monsters.add(Ghour(x, y, 'ghour', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.ghour))

    def gen_elite(self):
        if self.difficulty == 3:
            self.monsters.add(Ninja(WindowSettings.width // 2 , 870, 'Ninja', self.window, 
                                self.difficulty, self.player, self.bgm, MonsterSettings.Ninja, EliteSetting.Ninja))

    def map_render(self):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                (SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))

class BossScene(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(window, player, bgm)
        self.boss = Demon(WindowSettings.width//2-180, -100, 'demon', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.Demon, EliteSetting.Demon)
        self.box = DialogBox(self.window, self.boss, Size=(1500, 1500), Location=(-600, -300), SRCALPHA=False)
        self.player.state = State.TALKING
        self.can_renderbox = True
        self.victory = False
        self.box.index += 1
        self.cd = -1

    def gen_Map(self):
        self.map = Maps.gen_boss_map()
        self.gen_monsters()
        self.obstacles = Maps.gen_boss_obstacle()

    def gen_monsters(self):
        self.monsters.add(self.boss)
        self.monsters.add(Fort(385, 197, 'fort', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.Fort, EliteSetting.Fort))
        self.monsters.add(Fort(915, 197, 'fort', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.Fort, EliteSetting.Fort))
        self.monsters.add(Fort(915, 527, 'fort', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.Fort, EliteSetting.Fort))
        self.monsters.add(Fort(385, 527, 'fort', self.window, self.difficulty, self.player, self.bgm, MonsterSettings.Fort, EliteSetting.Fort))

    def map_render(self):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                (SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
    
    def recover(self):
        self.cd = -1
        self.boss.ChangeActionTo(State.ALIVE)
        self.boss.location = None
        self.boss.defence = 0.4
        self.boss.speed = 10

    def gen_ghost(self):
        if self.cd == -1:
            self.cd = 150
        if self.cd % 20 == 0 and self.cd >= 80:
            if randint(1, 2) == 1:
                    self.monsters.add(Ghost(randint(300, 900) , randint(0, 620), 'ghost', self.window, 
                                            self.difficulty, self.player, self.bgm, MonsterSettings.Ghost, EliteSetting.Ghost))
            else:
                self.monsters.add(Ghost(randint(100, 1180) , randint(300, 400), 'ghost', self.window, 
                                            self.difficulty, self.player, self.bgm, MonsterSettings.Ghost, EliteSetting.Ghost))
        if self.cd == 0:
            self.recover()
        
    def gen_fort(self):
        if self.cd == -1:
            self.cd = 100
            for each in self.monsters:
                if each.tag == 'fort':
                    each.can_fire = True
        if self.cd == 0:
            self.recover()
    
    def cure_self(self):
        if self.cd == -1:
            self.cd = 250
        if self.cd % 50 == 0 and self.cd != 0:
            self.boss.recover()
        if self.cd == 0:
            self.recover()

    def curse_player(self):
        if self.cd == -1:
            self.cd = 100
            self.player.debuff.append(Debuff.CURSE)
        elif self.cd == 0:
            self.recover()

    def update(self, key, slow_key):

        if self.cd > 0 :
            self.cd -= 1
        if self.boss.state == State.SUMMON: 
            if self.boss.magic == 3:
                self.gen_ghost()
            elif self.boss.magic == 2:
                self.gen_fort()
            elif self.boss.magic == 1:
                self.cure_self() 
            elif self.boss.magic == 0:
                self.curse_player()

        self.can_flush = False
        self.detectmonster()
        self.detectplayer()
        self.detectportal()
        if slow_key['E'] and self.can_renderbox:
            self.box.index += 1
            if self.box.index == self.box.len:
                self.boss.ChangeActionTo(State.ALIVE)
                self.end_dialog()
                self.player.state = State.ALIVE
                self.can_renderbox = False
        
        if slow_key['E'] and self.can_flush:
            event = pygame.event.Event(Event.FlushScene, {'GOTO': self.goto})
            pygame.event.post(event)

        for each in self.monsters:
            if self.victory and each.state != State.DEAD:
                each.ChangeActionTo(State.DEAD)
            each.update()
            if each.completelydead:
                if each.tag != 'ghost':
                    self.dead.add(each)
                self.monsters.remove(each)
            
        for each in self.bullets:
            each.update()
            if each.disappear or not each.rect.centerx in range(0, 1280) or not each.rect.centery in range(0, 720):
                self.bullets.remove(each)
        
        if not self.victory and self.boss.completelydead:
            self.victory = True
            self.player.speed = PlayerSettings.playerSpeed
            self.player.original_speed = PlayerSettings.playerSpeed
            self.bgm.stop_bgm()
            self.bgm.addsound('endportal')
            self.portals.add(EndPortal(WindowSettings.width // 2, WindowSettings.height // 2 - 160, 'dangerous', self.window, 'Leave the Castle', SceneType.END))  

        if pygame.sprite.spritecollide(self.player, self.obstacles, False):
            self.player.rect = self.player.rect.move(-self.player.dx, -self.player.dy)
        
        for each in self.monsters:
            if each.tag == 'fort' and pygame.sprite.collide_mask(each, self.player):
                self.player.rect = self.player.rect.move(-self.player.dx, -self.player.dy)
                break


    def render(self):
        
        self.map_render()
        for each in self.dead:
            each.draw()

        self.obstacles.draw(self.window)

        for each in self.bullets:
            each.draw()

        if self.victory:
            for each in self.portals:
                each.draw()
       
        for each in self.monsters:
            each.draw()
        
class EndScene(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(window, player, bgm)
        self.type = SceneType.END
        self.bg = pygame.image.load(GamePath.introudction)
        self.bg = pygame.transform.scale(self.bg, (WindowSettings.width,WindowSettings.height))

        self.font =pygame.font.Font(None,MenuSetting.textSize)

        self.text = self.font.render("please press E to end",True,(0,0,0))

        self.textRect = self.text.get_rect(center = (WindowSettings.width//2,WindowSettings.height - 50))
        self.blinkTimer = 0

        a = pygame.font.SysFont('alibabapuhuiti245light',85)
        b = pygame.font.SysFont('alibabapuhuiti245light',40)
        self.words = []
        self.words.append(a.render('Congratulations',True,(0,0,0)))
        self.words.append(b.render("for successfully clearing the level",True,(0,0,0)))
        
    def render(self):
        self.window.blit(self.bg,(0,0))
        self.blinkTimer += 1 
        if self.blinkTimer >= MenuSetting.blinkInterval:
            self.window.blit(self.text,self.textRect)
            if self.blinkTimer >= MenuSetting.blinkInterval*2:
                self.blinkTimer = 0
        self.window.blit(self.words[0],(WindowSettings.width//4 + 80,250))
        for i in range(1,len(self.words)):
            self.window.blit(self.words[i],(407,300 + 30*i))

