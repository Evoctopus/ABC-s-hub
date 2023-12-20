import pygame
import sys

pygame.init()
window = pygame.display.set_mode((800, 600))
player = pygame.image.load('player.png')  
backgroud = pygame.image.load('grass.png')   
player = pygame.transform.scale(player, (50, 50))
player_rect = player.get_rect()
player_rect.center = (400, 300)
clock = pygame.time.Clock()


speed = 5
while(True):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.flip()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        player_rect.x += speed
    if keys[pygame.K_a]:
        player_rect.x -= speed
    if keys[pygame.K_s]:
        player_rect.y += speed
    if keys[pygame.K_w]:
        player_rect.y -= speed
    window.blit(backgroud, (0, 0))
    window.blit(player, player_rect)
    
    clock.tick(60)
    
