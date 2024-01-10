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
        self.portal = None
        self.box = None
        self.can_renderbox = False
        self.keydown = False
        self.Coin = pygame.sprite.Group()
        self.dead = pygame.sprite.Group()
        self.window = window
        self.difficulty = 1
        self.width = WindowSettings.width
        self.height = WindowSettings.height

    def trigger_dialog(self, npc):
        self.box = DialogBox(self.window, npc)

    def end_dialog(self):
        self.box = None

    def trigger_battle(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def end_battle(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def trigger_shop(self, npc, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def end_shop(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update_camera(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    

    
    def detectnpc(self):
        
        for npc in self.npcs:
            if pygame.sprite.collide_rect(self.player, npc):
                npc.can_talk = True
                self.can_talk = True
                if self.box == None:
                    self.trigger_dialog(npc)
            else:
                npc.can_talk = False
    
    def detectmonster(self):
        object = pygame.sprite.spritecollide(self.playerweapon, self.monsters, False)
        if object and self.playerweapon.attacking:
            for monster in object:
                monster.beingattacked = True
    
    def detectplayer(self):
        for each in self.monsters:
            if each.attacking_method == AttackMethod.WEAPON:
                if each.weapon.attacking and pygame.sprite.collide_rect(self.player, each.weapon):
                    if not each.weapon.hasattacked:
                        self.player.beingattacked(each)
                        each.weapon.hasattacked = True

    def detectportal(self):
        if pygame.sprite.collide_rect(self.player, self.portal):
            self.portal.blink = True
        else:
            self.portal.blink = False

    def gen_npcs(self):
        pass

    def update(self, key, slow_key):
        self.can_talk = False
        self.detectmonster()
        self.detectnpc()
        self.detectplayer()
        self.detectportal()
        self.update_camera(self.player)
        if slow_key['E'] and self.can_talk:
            self.can_renderbox = True
            self.box.index += 1
            self.box.npc.state = State.TALKING
            self.player.state = State.TALKING
            if self.box.index == self.box.len:
                self.box.npc.state = State.ALIVE
                self.end_dialog()
                self.player.state = State.ALIVE
                self.can_renderbox = False
        
        if slow_key['E'] and self.portal.blink:
            event = pygame.event.Event(Event.FlushScene, {'GOTO': self.portal.goto})
            pygame.event.post(event)

        for each in self.npcs:
            each.update()
        for each in self.monsters:
            each.update()
            if each.state == State.DEAD:
                self.dead.add(each)
                self.monsters.remove(each)
                for _ in range(each.money[0]):
                    self.Coin.add(Coin(self.window, self.player, 'goldcoin', randint(1, 360)*math.pi/180, each.rect.center))
                for _ in range(each.money[1]):
                    self.Coin.add(Coin(self.window, self.player, 'silvercoin', randint(1, 360)*math.pi/180, each.rect.center)) 

        for each in self.Coin:
            if not each.disappear:
                each.update()
            else:
                self.Coin.remove(each)

    def render(self):
        
        self.map_render()
        self.obstacles.draw(self.window)
        self.portal.draw()
        for each in self.dead:
            each.draw()
        for each in self.npcs:
            each.draw()
        for each in self.monsters:
            each.draw()
        for each in self.Coin:
            each.draw()
        if self.can_renderbox:
            self.box.draw()

    def map_render(self):
        pass

class StartMenu():
    def __init__(self, window):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def render(self, time):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

class WildScene(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(window, player, bgm)
        self.type = SceneType.WILD

    def gen_Map(self):
        self.map = Maps.gen_wild_map()
        self.obstacles = Maps.gen_wild_obstacle()
        self.portal = Portal(500, 300, 'direction', self.window, 'THE FALLEN TOWN', SceneType.CITY)
        self.npcs.add(NPC(NPCSettings.npcstartx, NPCSettings.npcstarty, 'maqix', self.window, self.difficulty, self.player, self.bgm, GamePath.npc))
    
    def gen_monsters(self):
        self.monsters.add(Knight(WindowSettings.width //2 , WindowSettings.height // 2, 'knight', self.window, self.difficulty, self.player, self.bgm, GamePath.knight))
            
    def map_render(self):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                (SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))

class CityScene(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(window, player, bgm)
        self.type = SceneType.CITY

    def gen_Map(self):
        self.map = Maps.gen_city_map()
        self.portal = Portal(1000, 400, 'dangerous', self.window, 'Infernal Isle', SceneType.LAVA, True)
        self.rect = self.map.get_rect()
        self.rect.topleft = (0, 0)
        self.size = self.map.get_size()
    
    def map_render(self):
        self.window.blit(self.map, self.rect)
    
    def update_camera(self, player):
        if ((player.rect.centerx < WindowSettings.width / 4 and -self.rect.x > 0 and player.dx < 0) or 
            (player.rect.centerx > WindowSettings.width / 4 * 3 and -self.rect.x < WindowSettings.width and player.dx > 0)):
            self.rect = self.rect.move(-player.dx, 0)
            player.rect = player.rect.move(-player.dx, 0)        
        if ((player.rect.centery < WindowSettings.height / 4 and -self.rect.y > 0 and player.dy < 0)  or
            (player.rect.centery > WindowSettings.height / 4 * 3 and -self.rect.y < WindowSettings.height and player.dy > 0)):
            self.rect = self.rect.move(0, -player.dy)
            player.rect = player.rect.move(0, -player.dy)    
    
class LavaScene(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(self, window, player, bgm)
        self.type = SceneType.LAVA

    def gen_Map(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

class IceScene(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(self, window, player, bgm)
        self.type = SceneType.ICE

    def gen_Map(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    def gen_npcs(self):
        self.npcs.add(NPC(NPCSettings.npcstartx, NPCSettings.npcstarty, 'maqix', self.window, self.difficulty, self.player, self.bgm, GamePath.npc))

    def gen_monsters(self, num = 10):
        # for i in range(num):
        #     coordx = randint(0, SceneSettings.tileXnum - 1) * SceneSettings.tileWidth
        #     coordy = randint(0, SceneSettings.tileYnum - 1) * SceneSettings.tileHeight
        #     if randint(0, 3) == 0:
        #         self.monsters.add(Knight(WindowSettings.width - 50, coordy, 'knight', self.window, self.difficulty, self.player, self.bgm, GamePath.knight))
        #     elif randint(0, 3) == 1:
        #         self.monsters.add(Monster(0, coordy, 'knight', self.window, self.difficulty, self.player, GamePath.knight))
        #     elif randint(0, 3) == 2:
        #         self.monsters.add(Monster(coordx, WindowSettings.height - 50, 'knight', self.window, self.difficulty, self.player, GamePath.knight))
        #     elif randint(0, 3) == 3:
        #         self.monsters.add(Monster(coordx, 0, 'knight', self.window, self.difficulty, self.player, GamePath.knight)
        pass

class BossScene(Scene):
    def __init__(self, window, player, bgm):
        super().__init__(self, window, player, bgm)
    # Overwrite Scene's function
    def trigger_battle(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    
    def gen_Map(self):
        self.map = Maps.gen_wild_map()
        self.obstacles = Maps.gen_wild_obstacle()

    def gen_monsters(self):
        self.monsters.add(Demon(WindowSettings.width//2-60, 480, self.window, self.player, self.bgm))

    def update(self):
        self.detectmonster()
        self.detectplayer()
        for each in self.monsters:
            each.update()
            if each.completelydead:
                self.monsters.remove(each)

    def render(self):

        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                (SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
        self.obstacles.draw(self.window)
        for each in self.monsters:
            each.draw()