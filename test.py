import pygame
from sys import exit


pygame.init()
screen = pygame.display.set_mode((800, 600), pygame.RESIZABLE)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('green')
    pygame.draw.rect(screen, 'red', (screen.get_width() // 2 - 50, screen.get_height() // 2 - 50, 100, 100))
    pygame.display.update()