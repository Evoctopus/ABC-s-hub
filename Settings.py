# -*- coding:utf-8 -*-

from enum import Enum
import pygame

pygame.init()

class Color:
    Golden = (255, 215, 0)
    Red = (255, 0, 0)
    Grey = (250, 250, 250)
    Yellow = (255, 255, 0)
    White = (255, 255, 255)
    Blue = (135, 206, 250)
    Greyish = (211, 211, 211)

class WindowSettings:
    name = "Thgink Luos"
    width = 1280
    height = 720
    outdoorScale = 1.5 # A necessary scale to allow camera movement in outdoor scenes

class SceneSettings:
    tileXnum = 48 # 64
    tileYnum = 27 # 36
    tileXnum_small = 32
    tileYnum_small = 18
    tileWidth = tileHeight = 40
    obstacleDensity = 0.2
    houseWidth = houseHeight = 160
    special_block_width = 80
    special_block_height = 100

class PlayerSettings:
    # Initial Player Settings
    playerSpeed = 10
    playerWidth = 60
    playerHeight = 55
    playerHP = 20
    playerAttack = 5
    playerDefence = 1
    playerMoney = 100
    FontSize = 60

class NPCSettings:
    npcSize = { 'maqix': (60, 60), 'goddess': (60, 60),'glory_goddess' : (60,60),
                'prophet': (60,60), 'blacksmith': (70,70),"Monster_Hunter": (60,60),
                'Special_Merchant': (60,60),'archer': (60,60),'singer': (60,60),
                'knight': (60, 60), 'soldier': (60, 60), 'shaman': (60, 60), 'zombie': (60, 60), 'Monk': (300, 300),
                'fireworm': (80, 80), 'dragon': (80, 80), 'mummy': (60, 60), 'tauren': (60, 60), 'wizard': (80, 80), 'Melee': (300, 300),
                'simian': (60, 60), 'ghour': (60, 60), 'miner': (60, 60), 'iceworm': (60, 60), 'Ninja': (300, 300),   
                'demon': (400, 400), 'ghost': (600, 400), 'fort': (200, 200), 
                }
    
    npcstartx = WindowSettings.width // 4
    npcstarty = WindowSettings.height // 4 + 80
    talkCD = 30
    namecolor = (255, 255, 255)
    Fontsize = 20

class NPCType(Enum):
    DIALOG = 1
    MONSTER = 2
    SHOP = 3

class State(Enum):
    ALIVE = 1
    TALKING = 2
    STILL = 3
    ATTACKING = 4
    DEAD = 5
    HIT = 6
    SUMMON = 7
    SPELL = 8
    FROZEN = 10
    APPEAR = 11

class Debuff(Enum):
    BURNING = 1
    FROZEN = 2
    DIZZY = 3
    REPELL = 4
    CURSE = 5

class AttackMethod(Enum):
    WEAPON = 1
    FIST = 2
    BULLET = 3
    SKILL = 4
    SACRIFICE = 5

class BossSettings:
    width = 300
    height = 300
    coordX = (SceneSettings.tileXnum / 2) * SceneSettings.tileWidth - width / 2
    coordY = (SceneSettings.tileYnum / 2) * SceneSettings.tileHeight - height / 2

class SceneType(Enum):
    CITY = 1
    WILD = 2
    ICE = 3
    LAVA = 4
    BOSS = 5
    INTRODUCTION = 6
    MENU = 7
    END = 8

class BulletType(Enum):
    FireBall = 1
    Fire_Pink = 2
    Fire_Red = 3
    Fire_Yellow = 4
    Mini_Blue = 5
    Mini_Black = 6

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

class TextSettings:
    texts = {'maqix': [['&*DJOfe(*(WIOF))'], ['Matrix, Matrix, Matrix !!'], ['Can you get the charm of Matrix ?']],
             'demon': [['Finally you have come'], ['Still fantasizing defeating','me by your weak power ?'], ['HAHAHAHAHAHA'],['You must be good at acting as a joker']],
             'goddess': [['']],
             'prophet' : [['TO save our town'],['I prophesied that you would conquer the demon', 'king']],
             'archer': [['Do you need my help ?']],
             'singer': [['hey,hey'],["Do you knon me"],["I'm iKun you can know " ]]}
    Font1 = pygame.font.Font(None, 60)

class Shopingitems:
    items = {"Attack + 1": "Coin - 250", "Defence + 50": "Coin - 350",
             "Try Your Luck": "Coin - 150","Shieldlevel + 1":"Coin - 400",
             "Exit": " "}
    item1 = {"full HP" : "Coin - 50", "HPLimit + 200" : "Coin - 500",
             "Try Your Luck" : "Coin - 200" , "EXit":" "}
    item2 = {"Learn longcut(U)": "       Coin - 400","Learn spin(O)": "             Coin - 200",
             "Learn disappear(I)": "   Coin - 1500","EXit" : " "}
    item3 = { "get DIZZY Buff ":"Coin - 100" ,
             "get FROZEN Buff " : "Coin - 100", "get BURNING Buff " : "Coin - 100",
             "EXit" :' '}

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
    introudction = r".\assets\background\bg2.png"
    wild = r".\assets\background\wild.png"
    mapBlock = r".\assets\background\map.png"
    house = [r'.\assets\background\house_1.png',
             r'.\assets\background\castle1.png',
             r'.\assets/background/blacksmiith_1.png',
             r'.\assets\background\blacksmith_2.png',
             r'.\assets\background\cityhouse1.png',
             r'.\assets\background\cityhouse2.png',
             r'.\assets\background\cityhouse3.png',
             r'.\assets\background\cityhouse4.png',
             r'.\assets\background\cityhouse5.png',
             r'.\assets\background\cityhouse6.png',
             r'.\assets\background\cityhouse7.png']

    # player/npc related path
    npc = [r".\assets\npc\maqix\1.png"]
    goddess = [r"assets\npc\goddess\1.png",
               r'assets\npc\goddess\2.png']
    
    player = [f"./assets/player/{index}.png" for index in range(1, 5)]
    player2 = [f"./assets/player2/{index}.png" for index in range(1, 5)]

    glory_goddess = [r".\assets\npc\glory_goddess\1.png"]
    Monster_Hunter = [r".\assets\npc\Monster_Hunter\1.png"]
    Blacksmith = [r'.\assets\npc\blacksmith\1.png']
    Prophet = [r'.\assets\npc\prophet\1.png']
    Special_Merchant = [r".\assets\npc\Special_Merchant\1.png"]
    Archer = [f"./assets/npc/archer/{index}.png" for index in range(1, 5)]
    Singer = [r".\assets\npc\singer\singer1.png"]

    Sword = [f"./assets/weapon/Sword-cut/sword-{i}.png" for i in range(1, 7)]
    Claw = [f"./assets/weapon/claw/{i}.png" for i in range(1, 5)]

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

    roadTiles = [r".\assets\tiles\road1.png"]

    bossTiles = [
        r".\assets\tiles\boss1.png", 
        r".\assets\tiles\boss2.png", 
        r".\assets\tiles\boss3.png", 
        r".\assets\tiles\boss4.png", 
        r".\assets\tiles\boss5.png", 
        r".\assets\tiles\boss6.png", 
    ]

    lavaTiles = [r".\assets\tiles\lava1.png",
                 r".\assets\tiles\lava2.png",
                 r".\assets\tiles\lava3.png",
                 r".\assets\tiles\lava4.jpg",
                 r".\assets\tiles\lava5.png"]
    
    iceTiles = [r".\assets\tiles\ice1.png",
                r".\assets\tiles\ice2.png",
                r".\assets\tiles\ice5.png",
                ]

    bossWall = r".\assets\tiles\bossWall.png"

    portal = r".\assets\background\portal.png"

    tree = [r".\assets\tiles\tree.png",
            r".\assets\tiles\tree2.png",
            r".\assets\tiles\tree3.png",
            r".\assets\tiles\tree4.png"]

    cherry_blossom_tree = [f"./assets/tiles/Redtree{index}.png" for index in range(1, 9)]
                   
    bgm = [r".\assets\bgm\city.mp3",
           r".\assets\bgm\wild.mp3",
           r".\assets\bgm\boss.mp3"]
    
    wildOBS = [r".\assets\background\wildspecial1.png",
               r".\assets\background\wildspecial2.png"]
    
    iceOBS = [r".\assets\background\iceobs1.png",
              r".\assets\background\iceobs2.png"]
    
    lavaOBS = [r".\assets\background\lavaobs1.png",
               r".\assets\background\lavaobj2.png",
               r".\assets\background\lavaobs2.png"]
    
    Shopbg = [r".\assets\background\shopbg.png",
              r".\assets\background\shopbg1.png"]
    
    talkbg = [r".\assets\background\talkbg.png"]

class CoinSettings:
    value = {'goldcoin': 10, 'silvercoin': 20}
    size = (30, 30)

class MenuSetting:
    textSize = 36
    blinkInterval = 20
 
class PortalSettings:
    FontSize = 25
    ButtonSize = 25
    PortalSize = (70, 70)
    BuddhaSize = (140, 140)
    EndPortalSize = (200, 200)

class MonsterSettings:
    
    DetectingRange = 500
    AttackingRange = 70
    BulletRange = 300
    EliteRange = 130
    WholeRange = 1500

    knight = [f'assets/npc/knight/{index}.png' for index in range(1, 5)]
    soldier = [f'assets/npc/soldier/{index}.png' for index in range(1, 4)]
    shaman = [f'assets/npc/shaman/{index}.png' for index in range(1, 7)]
    zombie = [f'assets/npc/zombie/{index}.png' for index in range(1, 5)]
    Monk = [f'assets/npc/monk/run/{index}.png' for index in range(1, 9)]

    simian = [f'assets/npc/simian/{index}.png' for index in range(1, 5)]
    miner = [f'assets/npc/miner/{index}.png' for index in range(1, 5)]
    ghour = [f'assets/npc/ghour/{index}.png' for index in range(1, 5)]
    iceworm = [f'assets/npc/iceworm/{index}.png' for index in range(1, 5)]
    Ninja = [f'assets/npc/ninja/run/{index}.png' for index in range(1, 9)]

    fireworm = [f'assets/npc/fireworm/{index}.png' for index in range(1, 5)]
    dragon = [f'assets/npc/dragon/{index}.png' for index in range(1, 5)]
    tauren = [f'assets/npc/tauren/{index}.png' for index in range(1, 5)]
    mummy = [f'assets/npc/mummy/{index}.png' for index in range(1, 5)]
    wizard = [f'assets/npc/wizard/{index}.png' for index in range(1, 3)]
    Melee = [f'assets/npc/melee/run/{index}.png' for index in range(1, 7)]
    
    Ghost = [f'./assets/npc/ghost/appear/{index}.png' for index in range(1, 7)]
    Fort = [f'./assets/npc/fort/breath/{index}.png' for index in range(1, 15)]
    Demon = [f'./assets/npc/demon/idle/{index}.png' for index in range(1, 15)]

class BuffSettings:
    curse = {
        'path': [f'assets\specialeffect\curse\{index}.png' for index in range(1, 19)],
        'size': (400, 300),
        'fps': 0.5
    }
    swordplay = {
        'path': [f'assets\specialeffect\swordplay\{index}.png' for index in range(1, 7)],
        'size': (400, 400),
        'fps': 0.5
    }
    flame = {
        'path': [f'assets/specialeffect/flame/{index}.png' for index in range(1, 13)],
        'size': (80, 80),
        'fps': 0.5
    }
    frozen = {
        'path': [f'assets/specialeffect/frozen/{index}.png' for index in range(1, 2)],
        'size': (80, 80),
        'fps': 1
    }
    dizzy = {
        'path': [f'assets/specialeffect/dizzy/{index}.png' for index in range(1, 4)],
        'size': (60, 60),
        'fps': 0.5
    }
    fire_explode = {
        'path': [f'assets/specialeffect/explosion/fire_explode/{index}.png' for index in range(1, 45)],
        'size': (250, 250),
        'fps': 1.5
    }
    ice_explode = {
        'path': [f'assets/specialeffect/explosion/ice_explode/{index}.png' for index in range(1, 29)],
        'size': (200, 200),
        'fps': 1.5
    }
    curse_flame = {
        'path': [f'assets/specialeffect/curse_flame/{index}.png' for index in range(1, 15)],
        'size': (120, 120),
        'fps': 1
    }

class SwordSettings:
    cooldown = 10
    skillmsg = {'cut':       [6 , (65, 55), (2, 20), 60, 4],
                'longcut':   [8 , (95, 65), (4, 40), 80, 5], 
                'spin':      [20, (65, 55), (1, 40), 20, 0], 
                'disappear': [20, (65, 55), (1, 30), 50, 0], 
                'stab':      [8 , (95, 30), (1, 15), 30, 3]}

class BulletSettings:
    fireball = {'move': [f'assets/specialeffect/fireball/move/{index}.png' for index in range(1, 8)],
                'hit': [f'assets/specialeffect/fireball/explode/{index}.png' for index in range(1, 6)],
                'speed': 2,
                'atk': 40,
                'debuff': [Debuff.BURNING],
                'as': 0.5,
                'size': (60, 60),
                'sound': ['firewind', 'explode']}
    
    redfire = {'move': [f'assets/specialeffect/fire_red/{index}.png' for index in range(1, 15)],
                'speed': 1,
                'atk': 400,
                'debuff': [],
                'as': 0.5,
                'size': (60, 60),
                'sound': ['electronmagnetic', 'explode']}

    yellowfire = {'move': [f'assets/specialeffect/fire_yellow/{index}.png' for index in range(1, 15)],
                'speed': 1,
                'atk': 20,
                'debuff': [],
                'as': 0.5,
                'size': (60, 60),
                'sound': ['firewind', 'explode']}

    pinkfire = {'move': [f'assets/specialeffect/fire_pink/{index}.png' for index in range(1, 15)],
                'speed': 1,
                'atk': 50,
                'debuff': [],
                'as': 0.5,
                'size': (60, 60),
                'sound': ['firewind', 'explode']}
    
    miniblue = {'move': [f'assets/specialeffect/mini_blue/{index}.png' for index in range(1, 31)],
                'speed': 1,
                'atk': 50,
                'debuff': [Debuff.FROZEN],
                'as': 0.5,
                'size': (60, 60),
                'sound': ['firewind', 'explode']}

    miniblack = {'move': [f'assets/specialeffect/mini_black/{index}.png' for index in range(1, 31)],
                'speed': 1,
                'atk': 70,
                'debuff': [],
                'as': 0.5,
                'size': (60, 60),
                'sound': ['firewind', 'explode']}
  
class ShieldSettings:
    hp = [50, 100, 250, 400, 650, 900]

class Event:
    FlushScene = pygame.USEREVENT + 1
    PlayerDead = pygame.USEREVENT + 2

class EliteSetting:

    Monk = {'attack': 22, 'dead': 19, 'hit': 4, 'idle': 15, 'run': 9}
    Melee = {'attack': 11, 'dead': 11, 'hit': 4, 'idle': 9, 'run': 7}
    Ninja = {'attack': 30, 'dead': 26, 'hit': 4, 'idle': 16, 'run': 9} 
    Ghost = {'attack': 20, 'dead': 9, 'hit': 8, 'idle': 8,'run': 8}
    Fort = {'attack': 21, 'dead': 23, 'hit': 4, 'idle': 15, 'breath': 15}
    Demon = {'attack': 21, 'dead': 21, 'hit': 6, 'idle': 15, 'breath': 15, 'run': 10}
