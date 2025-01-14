# TODO: Rename snake to word chain
# TODO: It's hard to see the snake's tails

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

from sys import exit
import pygame
from random import seed
# seed(1)


# from hamiltonian import hamiltonian_cycle
# from word_chain import get_snake
# from backend import get_segments

from backend import get_cycle_segments_and_char_arr, get_linked_list
from hamiltonian import grid_neighbours
from snake_pieces import get_snake_surfs



ORIGINAL_SCREEN_WIDTH = 1200
ORIGINAL_SCREEN_HEIGHT = 800
FONTSIZE = 40
BACKGROUND_COLOR = 'black'
SNAKE_COLOR = 'darkgreen'
FPS = 60


def cell_to_pix(coord, cell_width, middle=False):
    r, c = coord
    if middle:
        r += 0.5
        c += 0.5
    return c * cell_width, r * cell_width


def pix_to_cell(coord, cell_width):
    x, y = coord
    return y // cell_width, x // cell_width


def draw_squares(screen, coords, cell_width, color):
    for coord in coords:
        pixes = cell_to_pix(coord, cell_width)
        rect = pygame.Rect(pixes[0], pixes[1], cell_width, cell_width)
        pygame.draw.rect(screen, color, rect)


def draw_snake(screen, found_squares, snake_start_surfs, snake_end_surfs, cycle_linked_list, cell_width):
    for square in found_squares:
        before, after = cycle_linked_list[square]
        if before in found_squares:
            direction = get_direction(before, square)
            screen.blit(snake_end_surfs[direction], cell_to_pix(square, cell_width))
        if after in found_squares:
            direction = get_direction(square, after)
            screen.blit(snake_start_surfs[direction], cell_to_pix(square, cell_width))


def draw_chars(screen, char_arr, alphabet_texts, char_rects, rows, cols):
    for r in range(rows):
        for c in range(cols):
            char = char_arr[r, c]
            char_text = alphabet_texts[char]
            char_rect = char_rects[r, c]
            screen.blit(char_text, char_rect)


directions = {
    (-1, 0): "up",
    (1, 0): "down",
    (0, -1): "left",
    (0, 1): "right"
}


def get_direction(start, end):
    return directions[(end[0] - start[0], end[1] - start[1])]


screen_sizes = {
    pygame.K_t: (4, 4),
    pygame.K_s: (6, 6),
    pygame.K_m: (10, 10),
    pygame.K_l: (14, 14),
    pygame.K_h: (20, 20)
}

cell_widths = {
    pygame.K_t: 50,
    pygame.K_s: 50,
    pygame.K_m: 50,
    pygame.K_l: 40,
    pygame.K_h: 40
}


pygame.init()
screen = pygame.display.set_mode((ORIGINAL_SCREEN_WIDTH, ORIGINAL_SCREEN_HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()


alphabet = "abcdefghijklmnopqrstuvwxyz"
font = pygame.font.SysFont('arial', FONTSIZE, True)
alphabet_texts = {char: font.render(char, True, 'grey') for char in alphabet}


game_state = "welcome"


while True:

    if game_state == "welcome":

        found_squares = set()
        selected_squares = []
        found_segments = []

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key in screen_sizes:
                    game_state = "play"
                    rows, cols = screen_sizes[event.key]
                    cell_width = cell_widths[event.key]
                    new_screen_width = cols * cell_width
                    new_screen_height = rows * cell_width
                    pygame.display.set_mode((new_screen_width, new_screen_height))

                    all_squares = {(r, c) for r in range(rows) for c in range(cols)}
                    cycle, snake, segments, char_arr = get_cycle_segments_and_char_arr(rows, cols)
                    cycle_linked_list = get_linked_list(cycle)
                    char_centers = {(r, c): cell_to_pix((r, c), cell_width, middle=True) for r in range(rows) for c in range(cols)}
                    char_rects = {(r, c): alphabet_texts[char_arr[r, c]].get_rect(center=char_centers[(r, c)]) for r in range(rows) for c in range(cols)}
                    snake_start_surfs, snake_end_surfs = get_snake_surfs(cell_width, SNAKE_COLOR)

        screen.fill('white')
        welcome_text = font.render("Welcome! Press T(iny), S(mall), M(edium), L(arge) or H(uge) to start.", True, 'black')
        welcome_text_rect = welcome_text.get_rect(center=screen.get_rect().center)
        screen.blit(welcome_text, welcome_text_rect)
        pygame.display.update()


    elif game_state == "play":

        if found_squares == all_squares:
            game_state = "game_over"
            pygame.display.set_mode((ORIGINAL_SCREEN_WIDTH, ORIGINAL_SCREEN_HEIGHT))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEMOTION or pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    pos = pygame.mouse.get_pos()
                    coord = pix_to_cell(pos, cell_width)
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
                    found_squares |= set(selected_squares)
                    # found_squares.extend(selected_squares)
                selected_squares = []
        
        screen.fill(BACKGROUND_COLOR)
        draw_snake(screen, found_squares, snake_start_surfs, snake_end_surfs, cycle_linked_list, cell_width)
        draw_squares(screen, selected_squares, cell_width, color=(80, 80, 80))
        draw_chars(screen, char_arr, alphabet_texts, char_rects, rows, cols)
        pygame.display.update()


    elif game_state == "game_over":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "welcome"
                found_squares = set()
                selected_squares = []
                found_segments = []

        screen.fill('black')
        text = font.render("Game over. Click to play again!", True, 'white')
        text_rect = text.get_rect(center=screen.get_rect().center)
        screen.blit(text, text_rect)
        pygame.display.update()
    
    clock.tick(FPS)
