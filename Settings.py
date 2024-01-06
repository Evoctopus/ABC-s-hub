# -*- coding:utf-8 -*-

from enum import Enum
import pygame

class WindowSettings:
    name = "Thgink Luos"
    width = 1280
    height = 720
    outdoorScale = 1.5 # A necessary scale to allow camera movement in outdoor scenes

class SceneSettings:
    tileXnum = 48 # 64
    tileYnum = 27 # 36
    tileWidth = tileHeight = 40
    obstacleDensity = 0.1

class PlayerSettings:
    # Initial Player Settings
    playerSpeed = 7
    playerWidth = 60
    playerHeight = 55
    playerHP = 20
    playerAttack = 5
    playerDefence = 1
    playerMoney = 100

class NPCSettings:
    npcSize = {'maqix': (60, 60), 'knight': (60, 60)}
    npcHP = {'maqix': 10, 'knight': 150}
    npcSpeed = {"maqix": 1, 'knight': 3}
    npcstartx = WindowSettings.width // 4
    npcstarty = WindowSettings.height // 4 + 80
    talkCD = 30
    namecolor = (255, 255, 255)
    Fontsize = 20

class NPCType(Enum):
    DIALOG = 1
    MONSTER = 2
    SHOP = 3
    KNIGHT = 4

class State(Enum):
    ALIVE = 1
    DEAD = 2
    BURNING = 3
    FROZEN = 4
    DIZZY = 5
    REPELL = 6
    TALKING = 7
    STILL = 8
    ATTACKING = 9

class BossSettings:
    width = 300
    height = 300
    coordX = (SceneSettings.tileXnum / 2) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2

class SceneType(Enum):
    CITY = 1
    WILD = 2
    BOSS = 3

class DialogSettings:
    boxWidth = 800
    boxHeight = 180
    boxStartX = WindowSettings.width // 4           # Coordinate X of the box
    boxStartY = WindowSettings.height // 3 * 2 + 20 # Coordinate Y of the box

    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 + 10         # Coordinate X of the first line of dialog
    textStartY = WindowSettings.height // 3 * 2 + 30    # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3                # Vertical distance of two lines

    npcWidth = WindowSettings.width // 5
    npcHeight = WindowSettings.height // 3
    npcCoordX = 0
    npcCoordY = WindowSettings.height * 2 // 3 - 20

class BattleSettings:
    boxWidth = WindowSettings.width * 3 // 4 
    boxHeight = WindowSettings.height * 3 // 4 
    boxStartX = WindowSettings.width // 8           # Coordinate X of the box
    boxStartY = WindowSettings.height // 8
    textSize = 48 # Default font size
    textStartX = WindowSettings.width // 4 
    textPlayerStartX = WindowSettings.width // 4          # Coordinate X of the first line of dialog
    textMonsterStartX = WindowSettings.width // 2 +100   
    textStartY = WindowSettings.height // 3         # Coordinate Y of the first line of dialog
    textVerticalDist = textSize // 4 * 3            # Vertical distance of two lines

    playerWidth = WindowSettings.width // 6
    playerHeight = WindowSettings.height // 3
    playerCoordX = WindowSettings.width // 8
    playerCoordY = WindowSettings.height // 2 

    monsterWidth = WindowSettings.width // 6
    monsterHeight = WindowSettings.height // 3
    monsterCoordX = WindowSettings.width * 5 // 8
    monsterCoordY = WindowSettings.height // 2 

    stepSize = 20

class ShopSettings:
    boxWidth = 800
    boxHeight = 200
    boxStartX = WindowSettings.width // 4   # Coordinate X of the box
    boxStartY = WindowSettings.height // 3  # Coordinate Y of the box

    textSize = 56 # Default font size
    textStartX = boxStartX + 10         # Coordinate X of the first line of dialog
    textStartY = boxStartY + 25    # Coordinate Y of the first line of dialog

class GamePath:
    # Window related path
    menu = r".\assets\background\menu.png"
    wild = r".\assets\background\wild.png"
    mapBlock = r".\assets\background\map.png"

    # player/npc related path
    npc = [r".\assets\npc\maqix\1.png"]
    player = [
        r".\assets\player\1.png", 
        r".\assets\player\1.png",
        r".\assets\player\2.png", 
        r".\assets\player\2.png", 
        r".\assets\player\3.png", 
        r".\assets\player\3.png", 
        r".\assets\player\4.png", 
        r".\assets\player\4.png", 
        # 8 frames for a single loop of animation looks much better.
    ]

    knight = [r".\assets\npc\knight\1.png",
              r".\assets\npc\knight\2.png",
              r".\assets\npc\knight\3.png",
              r".\assets\npc\knight\4.png",]
    
    boss = r".\assets\npc\boss.png"

    Sword1 = [f"./assets/weapon/Sword1/sword1-{i}.png" for i in range(1, 7)]


    groundTiles = [
        r".\assets\tiles\ground1.png", 
        r".\assets\tiles\ground2.png", 
        r".\assets\tiles\ground3.png", 
        r".\assets\tiles\ground4.png", 
        r".\assets\tiles\ground5.png", 
        r".\assets\tiles\ground6.png", 
    ]

    cityTiles = [
        r".\assets\tiles\city1.png", 
        r".\assets\tiles\city2.png", 
        r".\assets\tiles\city3.png", 
        r".\assets\tiles\city4.png", 
        r".\assets\tiles\city5.png", 
        r".\assets\tiles\city6.png", 
    ]

    cityWall = r".\assets\tiles\cityWall.png"

    bossTiles = [
        r".\assets\tiles\boss1.png", 
        r".\assets\tiles\boss2.png", 
        r".\assets\tiles\boss3.png", 
        r".\assets\tiles\boss4.png", 
        r".\assets\tiles\boss5.png", 
        r".\assets\tiles\boss6.png", 
    ]

    bossWall = r".\assets\tiles\bossWall.png"

    portal = r".\assets\background\portal.png"

    tree = r".\assets\tiles\tree.png"

    bgm = [r".\assets\bgm\city.mp3",
           r".\assets\bgm\wild.mp3",
           r".\assets\bgm\boss.mp3"]
    

class PortalSettings:
    width = 320
    height = 320
    coordX = (SceneSettings.tileXnum - 10) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2

class GameState(Enum):
    MAIN_MENU = 1
    GAME_TRANSITION = 2
    GAME_OVER = 3
    GAME_WIN = 4
    GAME_PAUSE = 5
    GAME_PLAY_WILD = 6
    GAME_PLAY_CITY = 7
    GAME_PLAY_BOSS = 8

class GameEvent:
    EVENT_BATTLE = pygame.USEREVENT + 1
    EVENT_DIALOG = pygame.USEREVENT + 2
    EVENT_SWITCH = pygame.USEREVENT + 3
    EVENT_RESTART = pygame.USEREVENT + 4
    EVENT_SHOP = pygame.USEREVENT + 5

class MonsterSettings:
    monsterSize = {'knight': (60, 60)}
    coordx = WindowSettings.width // 2 + 80
    coordy = WindowSettings.height // 2
    DetectingRange = 500

class WeaponSettings:
    weaponwidth = [65, 60]
    weaponheight = [55, 50]
    weaponatk = [10, 5]
    weaponas = [2, 2]

class SwordSettings:
    cooldown = 10
    skillmsg = {'cut': [6, (65, 55), (2, 10), 10, 4] ,
                'longcut': [8, (95, 65), (4, 20), 25, 5], 
                'spin': [20, (65, 55), (1,10), 10, 0], 
                'disappear': [20, (65, 55), (1, 30), 0, 0], 
                'stab': [8, (95, 30), (1, 5), 5, 3]}

class SwordPath:
    cut = [f"./assets/weapon/Sword-cut/sword-{i}.png" for i in range(1, 7)]
    longcut = [f"./assets/weapon/Sword-longcut/sword-{i}.png" for i in range(1, 9)]
    spin = [f"./assets/weapon/Sword-spin/sword-{i}.png" for i in range(1, 21)]
    stab = [f"./assets/weapon/Sword-stab/sword-{i}.png" for i in range(1, 9)]
    disappear = [f"./assets/weapon/Sword-disappear/sword-{i}.png" for i in range(1, 21)]
    

