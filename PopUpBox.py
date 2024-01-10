# -*- coding:utf-8 -*-

import pygame

from typing import *
from Settings import *

class DialogBox:
    def __init__(self, window, npc,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        
        self.window = window
        self.index = -1
        self.texts = TextSettings.texts[npc.name]
        self.len = len(self.texts)

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None,self.fontSize)

        self.bg = pygame.Surface((DialogSettings.boxWidth,DialogSettings.boxHeight),pygame.SRCALPHA)
        self.bg.fill(bgColor)

        self.npc = npc

        
    def draw(self):
        self.window.blit(self.bg,(DialogSettings.boxStartX,DialogSettings.boxStartY))
        self.window.blit(pygame.transform.scale(self.npc.image, (DialogSettings.npcWidth,DialogSettings.npcHeight)),
                         (DialogSettings.npcCoordX,DialogSettings.npcCoordY))
        self.text = self.texts[self.index]
        offset = 0 
        for text in self.text:
            self.window.blit(self.font.render(text,True,self.fontColor),(DialogSettings.textStartX,DialogSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        

class BattleBox:
    def __init__(self, window, player, monster, fontSize: int = BattleSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), bgColor: Tuple[int, int, int, int] = (0, 0, 0, 200)) :
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####


    def draw(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

class ShoppingBox:
    def __init__(self, window, npc, player,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150)):
        self.window = window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None,self.fontSize)

        self.bg = pygame.Surface((ShopSettings.boxWidth,ShopSettings.boxHeight),pygame.SRCALPHA)
        self.bg.fill(bgColor)

        
        self.npc = pygame.transform.scale(npc.image, (DialogSettings.npcWidth,DialogSettings.npcHeight))

        self.player = player
        self.items = npc.items

        self.selectedID = 0

    def buy(self):
        if self.selectedID == 0:
            self.player.attr_update(addCoins = -10, addAttack = 1)
        elif self.selectedID == 1:
            self.player.attr_update(addCoins = -10, addDefence = 1)
        elif self.selectedID == 2:
            self.player.attr_update(addCoins = -10, addHP = 1)

    def draw(self):
        self.window.blit(self.bg,(ShopSettings.boxStartX,ShopSettings.boxStartY))
        self.window.blit(self.npc,(DialogSettings.npcCoordX,DialogSettings.npcCoordY))

        offset = 0
        for id,item in enumerate(list(self.items.keys())):
            if id == self.selectedID:
                text = '-->' + item + '  ' + self.items[item]
            else:
                text = '     ' + item + self.items[item]
            self.window.blit(self.font.render(text,True,self.fontColor),
                             (ShopSettings.textStartX,ShopSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist


        texts = ["Coin: "  + str(self.player.money),
                 "HP: " + str(self.player.hp),
                 "Attack: " + str(self.player.attack),
                 "Defence: " + str(self.player.defence)]
        
        offset = 0
        for text in texts:
            self.window.blit(self.font.render(text,True,self.fontColor),
                             (ShopSettings.textStartX + ShopSettings.boxWidth *3/4,ShopSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist

