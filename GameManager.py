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
        self.scenetype = SceneType.MENU
        self.bgm = BgmPlayer()
        self.player = Player(self.window, self.bgm, WindowSettings.width // 2, WindowSettings.height - 60)
        self.player_sword = self.player.weapon
        self.scene = StartMenu(self.window, self.player, self.bgm)
        
        self.player_is_dead = False
        self.cd = 150

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
        self.bgm.setwalking(GOTO)
        if self.scenetype == SceneType.CITY:
            self.scene = CityScene(self.window, self.player, self.bgm)
            self.scene.gen_Map()
            self.bgm.play('city')
        if self.scenetype == SceneType.WILD:
            self.scene = WildScene(self.window,self.player,self.bgm)
            self.scene.gen_Map()
            self.bgm.play('wild')
        if self.scenetype == SceneType.INTRODUCTION:
            self.scene = Introduction(self.window,self.player,self.bgm)
            self.bgm.play("wild")
        if self.scenetype == SceneType.ICE:
            self.scene = IceScene(self.window,self.player,self.bgm)
            self.scene.gen_Map()
            self.bgm.play('city')
        if self.scenetype == SceneType.LAVA:
            self.scene = LavaScene(self.window,self.player,self.bgm)
            self.scene.gen_Map()
            self.bgm.play('wild')
        if self.scenetype == SceneType.BOSS:
            self.scene = BossScene(self.window,self.player,self.bgm)
            self.scene.gen_Map()
            self.bgm.play('boss')
        if self.scenetype == SceneType.END:
            self.scene = EndScene(self.window,self.player,self.bgm)
            self.bgm.play('boss')

    def update(self):

        if not self.player_is_dead:
            slow_key = {'E': False, 'W': False, 'S': False,'Q': False,'ENTER': False}
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        slow_key['E'] = True
                        if self.scene.type == SceneType.MENU:
                            self.flush_scene(SceneType.INTRODUCTION)
                        elif self.scene.type == SceneType.INTRODUCTION:
                            self.flush_scene(SceneType.CITY)
                        elif self.scene.type == SceneType.END:
                            pygame.quit()
                    if event.key == pygame.K_w:
                        slow_key['W'] = True
                    if event.key == pygame.K_s:
                        slow_key['S'] = True
                    if event.key == pygame.K_q:
                        slow_key['Q'] = True
                    if event.key == pygame.K_RETURN:
                        slow_key['ENTER'] = True
                        
                elif event.type == Event.FlushScene:
                    self.flush_scene(event.GOTO)
                
                elif event.type == Event.PlayerDead:
                    self.player_is_dead = True
                    self.cd = 0  
                    self.bgm.stop()
                
            key = pygame.key.get_pressed()
            self.player.update(key, slow_key)
            self.scene.update(key, slow_key)
            self.bgm.update()
        
        else:
            self.cd += 1
            if self.cd >= 150:
                self.flush_scene(SceneType.CITY)
                self.player_is_dead = False
                self.player.reset_pos(SceneType.CITY)
                self.player.attr_update(addCoins= -100, addHP=self.player.hp_limit)
                self.player.state = State.ALIVE
                self.bgm.addsound('reset')


    def render(self):
        
        self.scene.render()
        if self.scene.type != SceneType.MENU and self.scene.type != SceneType.INTRODUCTION and self.scene.type != SceneType.END:
            self.player.draw()

        if self.scenetype == SceneType.BOSS and self.scene.boss.state != State.DEAD and self.scene.boss.state != State.TALKING:
            pygame.draw.rect(self.window, (255, 0, 0), [0, WindowSettings.height - 30, self.scene.boss.hp * self.scene.boss.hp_coord, 20], 0)
            self.window.blit(self.scene.boss.namerender, (WindowSettings.width // 2 - self.scene.boss.namerender.get_width() / 2 , WindowSettings.height - 80)) 
        if self.scene.can_renderbox:
            self.scene.box.draw()

        if self.player_is_dead:
            self.render_dead_msg()
            
            
    def render_dead_msg(self):
        size = min(self.cd, 80)
        font = pygame.font.Font(None, size)
        dead_text = font.render('You Have Been Killed', True, Color.Yellow)
        self.window.blit(dead_text, ((WindowSettings.width - dead_text.get_width()) / 2 , (WindowSettings.height - dead_text.get_height()) / 2))
        font = pygame.font.Font(None, size // 3)
        dead_text2 = font.render('Cai Jiu Duo Lian', True, Color.Yellow)
        self.window.blit(dead_text2, ((WindowSettings.width - dead_text2.get_width()) / 2 , (WindowSettings.height + dead_text.get_height()) / 2))
