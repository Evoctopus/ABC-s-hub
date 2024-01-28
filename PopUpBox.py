# -*- coding:utf-8 -*-

import pygame
import random
from typing import *
from Settings import *

class DialogBox:
    def __init__(self, window, npc,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (0, 0, 0), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150),
                 Location: Tuple[float, float] =  (DialogSettings.npcCoordX,DialogSettings.npcCoordY),
                 Size: Tuple[float, float] = (DialogSettings.npcWidth,DialogSettings.npcHeight),
                 SRCALPHA=True):
        
        self.window = window
        self.index = -1
        self.texts = TextSettings.texts[npc.name]
        self.len = len(self.texts)

        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None,self.fontSize)

        self.bg = pygame.image.load(GamePath.talkbg[0])
        self.bg = pygame.transform.scale(self.bg,(DialogSettings.boxWidth+65,DialogSettings.boxHeight))
        self.npc = npc
        self.location = Location
        self.size = Size
        
        
    def draw(self):
        
        self.window.blit(pygame.transform.scale(self.npc.image, self.size),self.location)
        self.window.blit(self.bg,(DialogSettings.boxStartX-70,DialogSettings.boxStartY))
        
        self.text = self.texts[self.index]
        offset = 0 
        for text in self.text:
            self.window.blit(self.font.render(text,True,self.fontColor),(DialogSettings.textStartX+10,DialogSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        

class ShoppingBox:
    def __init__(self, window, npc, player,
                 fontSize: int = DialogSettings.textSize, 
                 fontColor: Tuple[int, int, int] = (255, 255, 255), 
                 bgColor: Tuple[int, int, int, int] = (0, 0, 0, 150),
                 SRCALPHA=True):
        self.window = window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pygame.font.Font(None,self.fontSize)

        self.bg = pygame.image.load(GamePath.Shopbg[1])
        self.bg = pygame.transform.scale(self.bg,(ShopSettings.boxWidth+90,ShopSettings.boxHeight+25))
        self.index = -1
        
        self.npc = npc
        if npc.name == 'blacksmith':
            
            self.items = Shopingitems.items
            
        if npc.name == 'glory_goddess':
            self.items = Shopingitems.item1
        if npc.name == 'Monster_Hunter':
            self.items = Shopingitems.item2
        if npc.name == 'Special_Merchant':
            self.items = Shopingitems.item3
        self.player = player
        self.selectedID = 0

    def buy(self):
        
        if self.selectedID == 0:
            if self.npc.name == 'blacksmith' :
                self.player.attr_update(addCoins = -250, addAttack = 1)
            if self.npc.name == 'glory_goddess' and self.player.hp_limit != self.player.hp:
                self.player.attr_update(addCoins = -50, addHP = self.player.hp_limit-self.player.hp)
            if self.npc.name == 'Monster_Hunter' and not(self.player.ability['longcut']):
                self.player.attr_update(addCoins = -400, ability='longcut')
            if self.npc.name == 'Special_Merchant' and not(self.player.buff_get['DIZZY']) and self.player.ability['spin']:
                self.player.attr_update(addCoins = -100, buff='DIZZY')
        elif self.selectedID == 1:
            if self.npc.name == 'blacksmith':
                self.player.attr_update(addCoins = -350, addDefence = 0.1)
            if self.npc.name == 'glory_goddess':
                self.player.attr_update(addCoins = -500, addHP_limit = 200, addHP = self.player.hp_limit - self.player.hp + 200)
            if self.npc.name == 'Monster_Hunter'and not(self.player.ability['spin']):
                self.player.attr_update(addCoins = -200, ability='spin')
            if self.npc.name == 'Special_Merchant' and not(self.player.buff_get['FROZEN']):
                self.player.attr_update(addCoins = -100, buff='FROZEN')
        elif self.selectedID == 2:
            if self.npc.name == 'blacksmith':
                self.player.attr_update(addCoins = -150, addAttack = random.randint(-2,2), addDefence = random.uniform(-0.2,0.2),islottery = True)
            if self.npc.name == 'glory_goddess':
                tem = random.randint(100,200)
                self.player.attr_update(addCoins = -200, addHP_limit = tem,addHP = self.player.hp_limit +tem -self.player.hp)
            if self.npc.name == 'Monster_Hunter' and not(self.player.ability['disappear']):
                self.player.attr_update(addCoins = -1500, ability='disappear')
            if self.npc.name == "Special_Merchant" and not(self.player.buff_get['BURNING']) and self.player.ability['longcut']:
                self.player.attr_update(addCoins = -100, buff='BURNING')
        elif self.selectedID == 3:
            if self.npc.name == "blacksmith":
                self.player.attr_update(addCoins = -400, addShield = 1)
                    

    def draw(self):
        self.window.blit(self.bg,(ShopSettings.boxStartX,ShopSettings.boxStartY))
        self.window.blit(pygame.transform.scale(self.npc.image, (DialogSettings.npcWidth,DialogSettings.npcHeight)),(DialogSettings.npcCoordX,DialogSettings.npcCoordY))

        offset = 0
        for id,item in enumerate(list(self.items.keys())):
            if id == self.selectedID:
                text = '-->' + item + '  ' + self.items[item]
            else:
                text = '     ' + item + self.items[item]
            self.window.blit(self.font.render(text,True,self.fontColor),
                             (ShopSettings.textStartX,ShopSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist


        texts = ["Shieldlevel: "  + str(self.player.shieldlevel),
                 "HP_Limit: " + str(self.player.hp_limit),
                 "Attack: " + str(self.player.atk),
                 "Defence: " + str(format(self.player.defence,'.1f'))]
        
        offset = 0
        for text in texts:
            self.window.blit(self.font.render(text,True,self.fontColor),
                             (ShopSettings.textStartX + ShopSettings.boxWidth *3/4,ShopSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist

