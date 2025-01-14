import pygame


def get_snake_surfs(cell_width, snake_color):

    snake_start_surf = pygame.Surface((cell_width, cell_width), pygame.SRCALPHA)
    snake_end_surf = pygame.Surface((cell_width, cell_width), pygame.SRCALPHA)


    pygame.draw.polygon(
        snake_start_surf,
        snake_color,
        points=[
            (cell_width / 2, cell_width / 4),
            (cell_width, cell_width / 4),
            (cell_width, 3 * cell_width / 4),
            (cell_width / 2, 3 * cell_width / 4),
            # (3 * cell_width / 4, cell_width / 2)
            ]
        )


    pygame.draw.circle(snake_end_surf, snake_color, center=(cell_width / 2, cell_width / 2), radius=cell_width / 4)
    pygame.draw.rect(snake_end_surf, snake_color, pygame.Rect(0, cell_width / 4, cell_width / 2 + 1, cell_width / 2 + 1))  # +1 to include the right edge of the rectangle (otherwise off by 1 pixel)

    snake_start_surfs = {
        "up": pygame.transform.rotate(snake_start_surf, 90),
        "right": snake_start_surf,
        "down": pygame.transform.rotate(snake_start_surf, -90),
        "left": pygame.transform.rotate(snake_start_surf, 180),
    }


    snake_end_surfs = {
        "up": pygame.transform.rotate(snake_end_surf, 90),
        "right": snake_end_surf,
        "down": pygame.transform.rotate(snake_end_surf, -90),
        "left": pygame.transform.rotate(snake_end_surf, 180),
    }

    return snake_start_surfs, snake_end_surfs


if __name__ == "__main__":

    CELL_WIDTH = 200
    BACKGROUND_COLOR = 'black'
    SNAKE_COLOR = 'darkgreen'

    snake_start_surfs, snake_end_surfs = get_snake_surfs(CELL_WIDTH, BACKGROUND_COLOR, SNAKE_COLOR)


    pygame.init()
    screen = pygame.display.set_mode((4 * CELL_WIDTH, 2 * CELL_WIDTH))

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        screen.blit(snake_start_surfs["up"], (0, 0))
        screen.blit(snake_start_surfs["right"], (CELL_WIDTH, 0))
        screen.blit(snake_start_surfs["down"], (2 * CELL_WIDTH, 0))
        screen.blit(snake_start_surfs["left"], (3 * CELL_WIDTH, 0))

        screen.blit(snake_end_surfs["up"], (0, CELL_WIDTH))
        screen.blit(snake_end_surfs["right"], (CELL_WIDTH, CELL_WIDTH))
        screen.blit(snake_end_surfs["down"], (2 * CELL_WIDTH, CELL_WIDTH))
        screen.blit(snake_end_surfs["left"], (3 * CELL_WIDTH, CELL_WIDTH))

        pygame.display.flip()
