# import pygame
# from Settings import *
# import math
# from Special import *

# def custom_rotate(surface, angle, center):
#     rect = surface.get_rect()
#     a = - rect.topleft[1] + center[1]
#     b = rect.topleft[0] - center[0]
#     r = math.hypot(a, b)
#     angle1 = math.asin(b / r)
#     dx = r * math.sin(angle1 + angle) - b
#     dy = a - r * math.cos(angle1 + angle)  
#     surface = pygame.transform.rotate(surface, angle)
#     rect.topleft = (rect.topleft[0] - dx, rect.topleft[1] - dy)
#     return surface, rect


# window = pygame.display.set_mode((WindowSettings.width, WindowSettings.height))

# #img = pygame.image.load(GamePath.weapon[0])
# img =  pygame.transform.scale(pygame.image.load(r'assets\specialeffect\array\summon.png'), (200, 200))
# rect = img.get_rect()
# rect.topleft = (40, 40)

# # img1 = img

# # print(rect.size)

# # midbottom = rect.midbottom
# # window.blit(img, rect)
# # print(midbottom)
# # print(rect.topleft)
# # center = midbottom
# # #img, rect = custom_rotate(img, 90, center)
# # angle = -60
# # img = pygame.transform.rotate(img, angle)
# # rect = img.get_rect()
# # rect.midbottom = [midbottom[0] + (35 - math.cos(angle * math.pi / 180)*35), midbottom[1]]
# # print(img.get_rect())

# # print(rect.midbottom)
# # print(rect.topleft)
# pygame.init()
# clock = pygame.time.Clock()
# i = 0
# angle = 0
# img = pygame.transform.scale(pygame.image.load(r'assets\npc\ghost\appear\5.png'), (300, 300))
# rect = img.get_rect()
# rect.topleft = (0, 0)
# window.fill((255, 255, 255))
# group = pygame.sprite.Group()

# bullet = Bullet(0, 0, window, 
#                 1, angle=(0.5, 0.5), bgm=None, paths=BulletSettings.fireball)
# while True:

#         clock.tick(30)
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.quit()
#             if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
#                 i += 1
#                 print(i)
#                 img =  pygame.transform.scale(pygame.image.load(r'assets\specialeffect\array\summon.png'), (200, 200))
#                 img = pygame.transform.rotate(img, angle)
#                 rect = img.get_rect()
#                 angle += 2
#                 rect.center = (140, 140)
#         bullet.update()
#         bullet.draw()
#         pygame.draw.rect(window, [0, 0, 0], [rect[0], rect[1], img.get_size()[0], img.get_size()[1]], 1)

#         window.blit(img, rect)
#         pygame.display.flip()




