import pygame

from hamiltonian import hamiltonian_cycle


rows, cols = 4, 4
cell_width = 20
screen_width = (cols + 1) * cell_width
screen_height = (rows + 1) * cell_width


def cell_to_pix(coord):
    r, c = coord
    return (c + 1) * cell_width, (r + 1) * cell_width

def draw_path(screen, path):
    for start, end in zip(path[:-1], path[1:]):
        pygame.draw.line(screen, 'red', cell_to_pix(start), cell_to_pix(end), 2)

def draw_edges(screen, edges):
    for start, end in edges:
        pygame.draw.line(screen, 'white', cell_to_pix(start), cell_to_pix(end), 1)


cycle = hamiltonian_cycle(rows, cols, return_tree=False)
print(f"Cycle: {cycle}")


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    screen.fill('black')
    # draw_edges(screen, tree)
    draw_path(screen, cycle)
    pygame.display.update()
