# -*- coding:utf-8 -*-

import sys
import pygame

from Player import Player
from Scene import *
from Settings import *
from PopUpBox import *
from Maps import *
from Weapon import *

class GameManager:
    def __init__(self):
        
        self.window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))
        self.player = Player(self.window)
        self.npc = NPC(NPCSettings.npcstartx, NPCSettings.npcstarty, 'maqix', GamePath.npc, window=self.window)
        self.monster = Monster(MonsterSettings.coordx, MonsterSettings.coordy, 'knight', GamePath.monster, window=self.window, weaponindex=1)
        
        self.gamestate = GameState.GAME_PLAY_WILD
        self.wild_scene = WildScene(self.window)
        self.wild_scene.gen_WILD()

    def game_reset(self):

        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    # Necessary game components here ↓
    def tick(self, fps):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def get_time(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    # Scene-related update functions here ↓
    def flush_scene(self, GOTO:SceneType):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update(self):
        key = pygame.key.get_pressed()
        self.player.update(key)
        self.monster.update(self.player)
        self.npc.update()

    def update_main_menu(self, events):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update_city(self, events):
        # Deal with EventQueue First
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update_wild(self, events):
        # Deal with EventQueue First
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
        
        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update_boss(self, events):
        # Deal with EventQueue First
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
        
        # Then deal with regular updates
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    # Collision-relate update funtions here ↓
    def update_collide(self):
        # Player -> Obstacles
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

        # Player -> NPCs; if multiple NPCs collided, only first is accepted and dealt with.
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

        # Player -> Monsters
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
        
        # Player -> Portals
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
        
        # Player -> Boss
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def update_NPCs(self):
        # This is not necessary. If you want to re-use your code you can realize this.
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    # Render-relate update functions here ↓
    def render(self):
        
        if self.gamestate == GameState.GAME_PLAY_WILD:
            self.render_wild()
        self.monster.draw()
        self.npc.draw()
        self.player.draw()
    
    def render_main_menu(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####
    
    def render_city(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def render_wild(self):
        self.wild_scene.render(self.player)

    def render_boss(self):
        pass
