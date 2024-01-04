# -*- coding:utf-8 -*-

import pygame
import Maps
from random import randint

from enum import Enum
from Settings import *
from NPCs import *
from PopUpBox import *
from Portal import *
from BgmPlayer import *

class Scene():
    def __init__(self, window):
        self.type = None
        self.map = None
        self.obstacles = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.portals = pygame.sprite.Group()
        self.window = window
        self.width = WindowSettings.width
        self.height = WindowSettings.height

    def trigger_dialog(self, npc):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def end_dialog(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

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

    def render(self, player):
        for i in range(SceneSettings.tileXnum):
            for j in range(SceneSettings.tileYnum):
                self.window.blit(self.map[i][j], 
                (SceneSettings.tileWidth * i, SceneSettings.tileHeight * j))
        self.obstacles.draw(self.window)

class StartMenu():
    def __init__(self, window):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def render(self, time):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

class CityScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.type = SceneType.CITY

    def gen_CITY(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

class WildScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        self.type = SceneType.WILD

    def gen_WILD(self):
        self.map = Maps.gen_wild_map()
        self.obstacles = Maps.gen_wild_obstacle()


    def gen_monsters(self, num = 10):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

class BossScene(Scene):
    def __init__(self, window):
        super().__init__(window=window)
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    # Overwrite Scene's function
    def trigger_battle(self, player):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def gen_BOSS(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
