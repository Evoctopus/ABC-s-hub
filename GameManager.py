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
        self.gamestate = GameState.GAME_PLAY_WILD
        self.scenetype = SceneType.WILD
        self.bgm = BgmPlayer(self.gamestate)
        self.player = Player(self.window, self.bgm)
        self.player_sword = self.player.weapon
        self.collidemanager = Collidable()
        
        
        self.scene = WildScene(self.window, self.player, self.bgm)
        if self.scenetype == SceneType.WILD:
            self.bgm.play('wild')
        
        self.scene.gen_Map()
        self.scene.gen_monsters()

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
        self.scenetype = GOTO
        self.player.reset_pos(self.scenetype)
        if self.scenetype == SceneType.CITY:
            self.scene = CityScene(self.window, self.player, self.bgm)
            self.scene.gen_Map()
            self.bgm.play('city')


    def update(self):
        slow_key = {'E': False, 'W': False, 'S': False}
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    slow_key['E'] = True
            if event.type == Event.FlushScene:
                self.flush_scene(event.GOTO)

        key = pygame.key.get_pressed()
        self.player.update(key, slow_key)
        self.scene.update(key, slow_key)
        self.update_collide()
        self.bgm.update()
        

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
        
        ##### Your Code Here ↑ #####

        # Player -> Monsters
        ##### Your Code Here ↓ #####
        
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
        pass

    # Render-relate update functions here ↓
    def render(self):
        
        self.scene.render()
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
        self.scene.render()

    def render_boss(self):
        pass
