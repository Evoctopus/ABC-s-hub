import pygame
import sys

pygame.init()
window = pygame.display.set_mode((800, 600))
player_right = pygame.image.load('pictures/figures/player.png')
player_right = pygame.transform.scale(player_right, (50,50))  
backgroud = pygame.image.load('pictures/background/grass.png')   
player_left = pygame.transform.flip(player_right, True, False)
player = player_right
player_rect = player.get_rect()
player_rect.center = (400, 300)
clock = pygame.time.Clock()
speed = 5
acceleration = -1
vert = 10
jump = False
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player = player_right
        player_rect.x += speed
    if keys[pygame.K_a]:
        player = player_left
        player_rect.x -= speed
    if keys[pygame.K_s]:
        player_rect.y += speed
    if keys[pygame.K_w]:
        player_rect.y -= speed
    if keys[pygame.K_SPACE]:
        jump = True
    if jump:
        
        player_rect.y -= vert
        vert += acceleration
        if(vert == -10):
            jump = False
            vert = 10
    window.blit(backgroud, (0, 0))
    window.blit(player, player_rect)
    
    clock.tick(60)
    
