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


def get_cycle_segments_and_char_arr(rows, cols, reverse_cycle=True):
    cycle = hamiltonian_cycle(rows, cols)
    if reverse_cycle:
        cycle.reverse()
    snake = get_snake(len(cycle) - 1)    
    segments = get_segments(cycle, snake)
    char_arr = get_char_arr(cycle, snake, rows, cols)
    return cycle, snake, segments, char_arr


def get_linked_list(cycle):
    linked_list = {}
    nodes = cycle[:-1]
    num_nodes = len(nodes)
    for i, node in enumerate(nodes):
        before = cycle[(i - 1) % num_nodes]
        after = cycle[(i + 1) % num_nodes]
        linked_list[node] = (before, after)
    return linked_list


if __name__ == "__main__":

    rows, cols = 2, 4
    cycle, snake, segments, char_arr = get_cycle_segments_and_char_arr(rows, cols)

    print("cycle", cycle)
    print("snake", snake)
    print("segments", segments)
    print("char_arr")
    print(char_arr)

    cycle = [0, 1, 2, 3, 4, 5, 0]
    print(get_linked_list(cycle))
