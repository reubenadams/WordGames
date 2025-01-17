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

import asyncio
from sys import exit
import pygame


from backend import get_cycle_segments_and_char_arr, get_linked_list
from hamiltonian import grid_neighbours
from snake_pieces import get_snake_surfs


from frontend import cell_to_pix, pix_to_cell, draw_squares, draw_snake, draw_chars


ORIGINAL_SCREEN_WIDTH = 800
ORIGINAL_SCREEN_HEIGHT = 600
FONTSIZE = 30
BACKGROUND_COLOR = 'black'
TEXT_COLOR = 'white'
SNAKE_COLOR = 'darkgreen'
FPS = 60


grid_sizes = {
    pygame.K_t: (4, 4),
    pygame.K_s: (6, 6),
    pygame.K_m: (10, 10),
    pygame.K_l: (14, 14),
    pygame.K_h: (20, 20)
}

cell_widths = {
    pygame.K_t: 40,
    pygame.K_s: 40,
    pygame.K_m: 40,
    pygame.K_l: 30,
    pygame.K_h: 30
}


pygame.init()
screen = pygame.display.set_mode((ORIGINAL_SCREEN_WIDTH, ORIGINAL_SCREEN_HEIGHT))
clock = pygame.time.Clock()


alphabet = "abcdefghijklmnopqrstuvwxyz"
font = pygame.font.SysFont('arial', FONTSIZE, True)
alphabet_texts = {char: font.render(char, True, 'grey') for char in alphabet}


async def main():

    game_state = "welcome"

    while True:

        if game_state == "welcome":

            found_squares = set()
            selected_squares = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key in grid_sizes:
                        game_state = "play"
                        rows, cols = grid_sizes[event.key]
                        cell_width = cell_widths[event.key]
                        left_buffer, top_buffer = cell_width, cell_width
                        new_screen_width = (cols + 10) * cell_width
                        new_screen_height = (rows + 2) * cell_width
                        pygame.display.set_mode((new_screen_width, new_screen_height))

                        all_squares = {(r, c) for r in range(rows) for c in range(cols)}
                        cycle, snake, segments, char_arr = get_cycle_segments_and_char_arr(rows, cols)
                        cycle_linked_list = get_linked_list(cycle)
                        char_centers = {(r, c): cell_to_pix((r, c), cell_width, left_buffer, top_buffer, middle=True) for r in range(rows) for c in range(cols)}
                        char_rects = {(r, c): alphabet_texts[char_arr[r, c]].get_rect(center=char_centers[(r, c)]) for r in range(rows) for c in range(cols)}
                        snake_start_surfs, snake_end_surfs = get_snake_surfs(cell_width, SNAKE_COLOR)

                        # Uncomment to see the solution
                        # found_squares = all_squares

            screen.fill(BACKGROUND_COLOR)
            welcome_text = font.render("Press T(iny), S(mall), M(edium), L(arge) or H(uge) to start.", True, TEXT_COLOR)
            welcome_text_rect = welcome_text.get_rect(center=screen.get_rect().center)
            screen.blit(welcome_text, welcome_text_rect)

        elif game_state == "play":

            if found_squares == all_squares:
                game_state = "game_over"
                selected_squares = []

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEMOTION or pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        pos = pygame.mouse.get_pos()
                        coord = pix_to_cell(pos, cell_width, left_buffer, top_buffer)
                        if coord not in selected_squares:
                            if selected_squares:
                                last_coord = selected_squares[-1]
                                if coord in grid_neighbours(last_coord[0], last_coord[1], rows, cols):
                                    selected_squares.append(coord)
                            else:
                                if coord in all_squares:
                                    selected_squares.append(coord)
                if event.type == pygame.MOUSEBUTTONUP:
                    if selected_squares in segments:
                        found_squares |= set(selected_squares)
                    selected_squares = []
            
            screen.fill(BACKGROUND_COLOR)
            draw_snake(screen, found_squares, snake_start_surfs, snake_end_surfs, cycle_linked_list, cell_width, left_buffer, top_buffer)
            draw_squares(screen, selected_squares, cell_width, left_buffer, top_buffer, color=(80, 80, 80))
            draw_chars(screen, char_arr, alphabet_texts, char_rects, rows, cols)

        elif game_state == "game_over":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    game_state = "welcome"
                    pygame.display.set_mode((ORIGINAL_SCREEN_WIDTH, ORIGINAL_SCREEN_HEIGHT))

            screen.fill('black')
            complete_text = font.render("Grid complete!", True, TEXT_COLOR)
            replay_text = font.render("Click to play again.", True, TEXT_COLOR)
            complete_text_rect = complete_text.get_rect(center=(screen.get_width() - 200, screen.get_height() // 2 - cell_width))
            replay_text_rect = replay_text.get_rect(center=(screen.get_width() - 200, screen.get_height() // 2 + cell_width))
            screen.blit(complete_text, complete_text_rect)
            screen.blit(replay_text, replay_text_rect)

            draw_snake(screen, found_squares, snake_start_surfs, snake_end_surfs, cycle_linked_list, cell_width, left_buffer, top_buffer)
            draw_chars(screen, char_arr, alphabet_texts, char_rects, rows, cols)

        pygame.display.update()
        clock.tick(FPS)
        await asyncio.sleep(0)


asyncio.run(main())
