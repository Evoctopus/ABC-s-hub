import pygame
from Settings import *
import math

def custom_rotate(surface, angle, center):
    rect = surface.get_rect()
    a = - rect.topleft[1] + center[1]
    b = rect.topleft[0] - center[0]
    r = math.hypot(a, b)
    angle1 = math.asin(b / r)
    dx = r * math.sin(angle1 + angle) - b
    dy = a - r * math.cos(angle1 + angle)  
    surface = pygame.transform.rotate(surface, angle)
    rect.topleft = (rect.topleft[0] - dx, rect.topleft[1] - dy)
    return surface, rect


window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))

img = pygame.image.load(GamePath.weapon[0])

rect = img.get_rect()
img = pygame.transform.scale(img, (70, 20))
img1 = img
rect = img.get_rect()
print(rect.size)
rect.topleft = (50, 50)
midbottom = rect.midbottom
window.blit(img, rect)
print(midbottom)
print(rect.topleft)
center = midbottom
#img, rect = custom_rotate(img, 90, center)
angle = -60
img = pygame.transform.rotate(img, angle)
rect = img.get_rect()
rect.midbottom = [midbottom[0] + (35 - math.cos(angle * math.pi / 180)*35), midbottom[1]]
print(img.get_rect())

print(rect.midbottom)
print(rect.topleft)
pygame.init()
clock = pygame.time.Clock()

while True:

        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        window.blit(img, rect)
        pygame.display.flip()







