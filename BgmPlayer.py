import pygame
from Settings import *

class BgmPlayer():
    def __init__(self):

        pygame.mixer.init()
        pygame.mixer.music.set_volume(0.5)
        self.walking = pygame.mixer.Sound(f'./assets/bgm/walk_inside.mp3')
        self.burning = pygame.mixer.Sound(r'assets\bgm\burning.mp3')
        self.iswalking = False
        self.extra = []

    def play(self, name, loop=-1):
        pygame.mixer.music.load(f'./assets/bgm/{name}.mp3')
        pygame.mixer.music.play(loop)
        

    def stop_bgm(self):
        pygame.mixer.music.stop()

    def setwalking(self, scenetype):
        if scenetype == SceneType.ICE:
            self.walking = pygame.mixer.Sound(f'./assets/bgm/walk_snow.mp3')
        elif scenetype == SceneType.WILD:
            self.walking = pygame.mixer.Sound(f'./assets/bgm/walk_grass.mp3')
        else:
            self.walking = pygame.mixer.Sound(f'./assets/bgm/walk_inside.mp3')

    def stop(self):
        self.stopwalking()
        self.burning.stop()
        self.extra = []
        pygame.mixer.music.stop()

    def addsound(self, name):
        music = pygame.mixer.Sound(f'./assets/bgm/{name}.mp3')
        self.extra.append(music)

    def stopwalking(self):
        self.iswalking = False
        self.walking.stop()
    
    def startwalking(self):
        if not self.iswalking:
            self.iswalking = True
            self.walking.play(-1)

    def update(self):
        for music in self.extra:
            music.play()
        self.extra = []


    
