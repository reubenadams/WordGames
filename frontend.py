# TODO: When your mouse goes off the screen the selected cells seems to go awry

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


# from hamiltonian import hamiltonian_cycle
# from word_chain import get_snake
# from backend import get_segments

from backend import get_cycle_segments_and_char_arr


rows, cols = 14, 14
cell_width = 40
screen_width = cols * cell_width
screen_height = rows * cell_width
FONTSIZE = 30


def cell_to_pix(coord, middle=False):
    r, c = coord
    if middle:
        r += 0.5
        c += 0.5
    return c * cell_width, r * cell_width


def pix_to_cell(coord):
    x, y = coord
    return y // cell_width, x // cell_width


def draw_squares(screen, coords, color):
    for coord in coords:
        pixes = cell_to_pix(coord)
        rect = pygame.Rect(pixes[0], pixes[1], cell_width, cell_width)
        pygame.draw.rect(screen, color, rect)


def draw_chars(screen, char_arr, alphabet_texts, char_rects, rows, cols):
    for r in range(rows):
        for c in range(cols):
            char = char_arr[r, c]
            char_text = alphabet_texts[char]
            char_rect = char_rects[r, c]
            screen.blit(char_text, char_rect)


def draw_segments(screen, segments, color):
    for segment in segments:
        for start, end in zip(segment[:-1], segment[1:]):
            pygame.draw.line(screen, color, cell_to_pix(start, middle=True), cell_to_pix(end, middle=True), 3)


pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))


alphabet = "abcdefghijklmnopqrstuvwxyz"
font = pygame.font.SysFont('arial', FONTSIZE, True)


cycle, snake, segments, char_arr = get_cycle_segments_and_char_arr(rows, cols)
print(snake)

alphabet_texts = {char: font.render(char, True, 'grey') for char in alphabet}
char_centers = {(r, c): cell_to_pix((r + 0.5, c + 0.5)) for r in range(rows) for c in range(cols)}
char_rects = {(r, c): alphabet_texts[char_arr[r, c]].get_rect(center=char_centers[(r, c)]) for r in range(rows) for c in range(cols)}


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
                    selected_squares.append(coord)
        if event.type == pygame.MOUSEBUTTONUP:
            if selected_squares in segments:
                found_segments.append(selected_squares)
                found_squares.extend(selected_squares)
            selected_squares = []
    
    screen.fill('black')
    draw_squares(screen, found_squares, 'darkgreen')
    draw_squares(screen, selected_squares, color=(80, 80, 80))
    draw_segments(screen, found_segments, color='red')
    draw_chars(screen, char_arr, alphabet_texts, char_rects, rows, cols)
    pygame.display.update()