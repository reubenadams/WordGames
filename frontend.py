# TODO: Rename snake to word chain

# Steps:
# 1. User specifies rows and cols
# 2. Construct a Hamiltonian cycle
# 3. Construct a word chain of that length
# 4. Divide the cycle into segments the same length as the words
# 5. Create a letter grid from the chain and the cycle

# Visuals:
# 1. Display the letters
# 2. Let the user select letters, (draw these before letters)
# 3. Once mouse releases, if cells match a cycle segment, colour in those squares


import pygame
from random import seed
seed(1)


# from hamiltonian import hamiltonian_cycle
# from word_chain import get_snake
# from backend import get_segments

from backend import get_cycle_segments_and_char_arr, get_linked_list
from hamiltonian import grid_neighbours
from snake_pieces import get_snake_surfs


rows, cols = 6, 6
CELL_WIDTH = 100
screen_width = cols * CELL_WIDTH
screen_height = rows * CELL_WIDTH
FONTSIZE = 40
BACKGROUND_COLOR = 'black'
SNAKE_COLOR = 'darkgreen'


def cell_to_pix(coord, middle=False):
    r, c = coord
    if middle:
        r += 0.5
        c += 0.5
    return c * CELL_WIDTH, r * CELL_WIDTH


def pix_to_cell(coord):
    x, y = coord
    return y // CELL_WIDTH, x // CELL_WIDTH


def draw_squares(screen, coords, color):
    for coord in coords:
        pixes = cell_to_pix(coord)
        rect = pygame.Rect(pixes[0], pixes[1], CELL_WIDTH, CELL_WIDTH)
        pygame.draw.rect(screen, color, rect)


def draw_snake(screen, found_squares, snake_start_surfs, snake_end_surfs, cycle_linked_list):
    for square in found_squares:
        before, after = cycle_linked_list[square]
        if before in found_squares:
            direction = get_direction(before, square)
            screen.blit(snake_end_surfs[direction], cell_to_pix(square))
        if after in found_squares:
            direction = get_direction(square, after)
            screen.blit(snake_start_surfs[direction], cell_to_pix(square))


def draw_chars(screen, char_arr, alphabet_texts, char_rects, rows, cols):
    for r in range(rows):
        for c in range(cols):
            char = char_arr[r, c]
            char_text = alphabet_texts[char]
            char_rect = char_rects[r, c]
            screen.blit(char_text, char_rect)


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))


alphabet = "abcdefghijklmnopqrstuvwxyz"
font = pygame.font.SysFont('arial', FONTSIZE, True)


cycle, snake, segments, char_arr = get_cycle_segments_and_char_arr(rows, cols)
print(snake)
cycle_linked_list = get_linked_list(cycle)


directions = {
    (-1, 0): "up",
    (1, 0): "down",
    (0, -1): "left",
    (0, 1): "right"
}


def get_direction(start, end):
    return directions[(end[0] - start[0], end[1] - start[1])]



alphabet_texts = {char: font.render(char, True, 'grey') for char in alphabet}
char_centers = {(r, c): cell_to_pix((r, c), middle=True) for r in range(rows) for c in range(cols)}
char_rects = {(r, c): alphabet_texts[char_arr[r, c]].get_rect(center=char_centers[(r, c)]) for r in range(rows) for c in range(cols)}

snake_start_surfs, snake_end_surfs = get_snake_surfs(CELL_WIDTH, SNAKE_COLOR)


found_squares = []
selected_squares = []
found_segments = []

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION or pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                coord = pix_to_cell(pos)
                if coord not in selected_squares:
                    if selected_squares:
                        last_coord = selected_squares[-1]
                        if coord in grid_neighbours(last_coord[0], last_coord[1], rows, cols):
                            selected_squares.append(coord)
                    else:
                        selected_squares.append(coord)
        if event.type == pygame.MOUSEBUTTONUP:
            if selected_squares in segments:
                found_segments.append(selected_squares)
                found_squares.extend(selected_squares)
            selected_squares = []
    
    screen.fill(BACKGROUND_COLOR)
    draw_snake(screen, found_squares, snake_start_surfs, snake_end_surfs, cycle_linked_list)
    draw_squares(screen, selected_squares, color=(80, 80, 80))
    draw_chars(screen, char_arr, alphabet_texts, char_rects, rows, cols)
    pygame.display.update()
