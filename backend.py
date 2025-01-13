from hamiltonian import hamiltonian_cycle
from word_chain import get_snake
import numpy as np


def get_segments(cycle, snake):
    segments = []
    start = 0
    for word in snake:
        end = start + len(word)
        segments.append(cycle[start : end])
        start = end - 1
    return segments


def collapse_snake(snake):
    return ''.join([word[:-1] for word in snake])


def get_char_arr(cycle, snake, rows, cols):
    snake = collapse_snake(snake)
    arr = np.full((rows, cols), '_')
    for cell, char in zip(cycle, snake):
        arr[cell] = char
    return arr


def get_cycle_segments_and_char_arr(rows, cols):
    cycle = hamiltonian_cycle(rows, cols)
    snake = get_snake(len(cycle) - 1)    
    segments = get_segments(cycle, snake)
    char_arr = get_char_arr(cycle, snake, rows, cols)
    return cycle, snake, segments, char_arr


if __name__ == "__main__":

    rows, cols = 2, 4
    cycle, snake, segments, char_arr = get_cycle_segments_and_char_arr(rows, cols)

    print("cycle", cycle)
    print("snake", snake)
    print("segments", segments)
    print("char_arr")
    print(char_arr)
