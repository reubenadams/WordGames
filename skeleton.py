import pygame
from sys import exit


pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Game")

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BLACK = (0, 0, 0)

font = pygame.font.SysFont('arial', 50, True, False)


clock = pygame.time.Clock()
FPS = 60


def welcome():

    text = font.render("Welcome! Press Enter to start...", True, BLACK)
    text_rect = text.get_rect(center=screen.get_rect().center)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
        
        screen.fill(WHITE)
        screen.blit(text, text_rect)
        pygame.display.update()
        clock.tick(FPS)


def play():

    text = font.render("Playing. Don't press X!", True, "red")
    text_rect = text.get_rect(center=screen.get_rect().center)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    running = False
        
        screen.fill(GREY)
        screen.blit(text, text_rect)
        pygame.display.update()
        clock.tick(FPS)


def game_over():

    text = font.render("Game over. Click to play again!", True, "white")
    text_rect = text.get_rect(center=screen.get_rect().center)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        screen.fill(BLACK)
        screen.blit(text, text_rect)
        pygame.display.update()
        clock.tick(FPS)


def main():

    while True:
        welcome()
        play()
        game_over()


if __name__ == "__main__":
    main()
