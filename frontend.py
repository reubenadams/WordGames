import pygame


directions = {
    (-1, 0): "up",
    (1, 0): "down",
    (0, -1): "left",
    (0, 1): "right"
}


def get_direction(start, end):
    return directions[(end[0] - start[0], end[1] - start[1])]


def cell_to_pix(coord, cell_width, left_buffer, top_buffer, middle=False):
    r, c = coord
    if middle:
        r += 0.5
        c += 0.5
    return c * cell_width + left_buffer, r * cell_width + top_buffer


def pix_to_cell(coord, cell_width, left_buffer, top_buffer):
    x, y = coord
    return (y - top_buffer) // cell_width, (x - left_buffer) // cell_width


def draw_squares(screen, coords, cell_width, left_buffer, top_buffer, color):
    for coord in coords:
        pixes = cell_to_pix(coord, cell_width, left_buffer, top_buffer)
        rect = pygame.Rect(pixes[0], pixes[1], cell_width, cell_width)
        pygame.draw.rect(screen, color, rect)


def draw_snake(screen, found_squares, snake_start_surfs, snake_end_surfs, cycle_linked_list, cell_width, left_buffer, top_buffer):
    for square in found_squares:
        before, after = cycle_linked_list[square]
        if before in found_squares:
            direction = get_direction(before, square)
            screen.blit(snake_end_surfs[direction], cell_to_pix(square, cell_width, left_buffer, top_buffer))
        if after in found_squares:
            direction = get_direction(square, after)
            screen.blit(snake_start_surfs[direction], cell_to_pix(square, cell_width, left_buffer, top_buffer))


def draw_chars(screen, char_arr, alphabet_texts, char_rects, rows, cols):
    for r in range(rows):
        for c in range(cols):
            char = char_arr[r, c]
            char_text = alphabet_texts[char]
            char_rect = char_rects[r, c]
            screen.blit(char_text, char_rect)
