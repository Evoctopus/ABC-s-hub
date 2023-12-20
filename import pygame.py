import pygame
import sys 

pygame.init()
height = 600
width = 600
window = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()
bg = pygame.image.load(".\grass.png")
player = pygame.image.load(".\player.png")
player = pygame.transform.scale(player,(50,50))
player_rect = player.get_rect()
player_rect.center = (width//2, height//2)
speed = 10
while(True):
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= speed
    if keys[pygame.K_s]:
        player_rect.y += speed
    if keys[pygame.K_a]:
        player_rect.x -= speed
    if keys[pygame.K_d]:
        player_rect.x += speed

    pygame.display.flip()

    window.blit(bg,(0,0))
    window.blit(player,player_rect)
    clock.tick(60)