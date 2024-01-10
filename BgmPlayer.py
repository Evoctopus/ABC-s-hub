import pygame
from Settings import *

class BgmPlayer():
    def __init__(self, gamestate):
        self.gamestate = gamestate
        self.extra = []


    def play(self, name, loop=-1):
        pygame.mixer.music.load(f'./assets/bgm/{name}.mp3')
        pygame.mixer.music.play(loop)
        

    def stop(self):
        ##### Your Code Here ↓ #####
        pass
        ##### Your Code Here ↑ #####

    def addsound(self, name):
        music = pygame.mixer.Sound(f'./assets/bgm/{name}.mp3')
        self.extra.append(music)

    def update(self):
        for music in self.extra:
            music.play()
        self.extra = []


    
