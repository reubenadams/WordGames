import pygame

pygame.init()

rows, cols = 6, 6
cell_width = 50
screen_width = (cols + 1) * cell_width
screen_height = (rows + 1) * cell_width


screen = pygame.display.set_mode((screen_width, screen_height))


def cell_to_pix(coord):
    r, c = coord
    return (c + 1) * cell_width, (r + 1) * cell_width

def draw_path(path):
    for coord1, coord2 in zip(path[:-1], path[1:]):
        pygame.draw.line(screen, 'white', cell_to_pix(coord1), cell_to_pix(coord2), 3)

def draw_edges(edges):
    for coord1, coord2 in edges:
        pygame.draw.line(screen, 'white', cell_to_pix(coord1), cell_to_pix(coord2), 3)


path = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (5, 1), (4, 1), (3, 1), (2, 1), (1, 1), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (5, 3), (4, 3), (3, 3), (2, 3), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4), (5, 4), (5, 5), (4, 5), (3, 5), (2, 5), (1, 5), (0, 5), (0, 4), (0, 3), (0, 2), (0, 1), (0, 0)]
edges = [((5, 5), (4, 5)), ((5, 5), (5, 4)), ((5, 4), (4, 4)), ((4, 4), (3, 4)), ((5, 4), (5, 3)), ((4, 5), (3, 5)), ((3, 4), (2, 4)), ((3, 4), (3, 3)), ((3, 3), (4, 3)), ((4, 3), (4, 2)), ((5, 3), (5, 2)), ((3, 5), (2, 5)), ((2, 4), (1, 4)), ((1, 4), (0, 4)), ((0, 4), (0, 5)), ((4, 2), (3, 2)), ((3, 3), (2, 3)), ((5, 2), (5, 1)), ((3, 2), (2, 2)), ((5, 1), (4, 1)), ((5, 1), (5, 0)), ((2, 2), (1, 2)), ((1, 4), (1, 5)), ((1, 4), (1, 3)), ((5, 0), (4, 0)), ((1, 3), (0, 3)), ((3, 2), (3, 1)), ((4, 0), (3, 0)), ((1, 2), (0, 2)), ((2, 2), (2, 1)), ((1, 2), (1, 1)), ((0, 2), (0, 1)), ((2, 1), (2, 0)), ((0, 1), (0, 0)), ((1, 1), (1, 0))]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('black')
    # draw_path(path)
    draw_edges(edges)
    pygame.display.update()
