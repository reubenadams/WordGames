from random import shuffle


def grid_neighbours(r: int, c: int, max_r: int, max_c: int):
    neighbs = []
    for dr in {-1, 1}:
        if 0 <= r + dr < max_r:
            neighbs.append((r + dr, c))
    for dc in {-1, 1}:
        if 0 <= c + dc < max_c:
            neighbs.append((r, c + dc))
    return neighbs


def grid_graph(rows: int, cols: int):
    return {(r, c): grid_neighbours(r, c, rows, cols) for r in range(rows) for c in range(cols)}


def hamiltonian_path(graph: dict, start, end, visit=None):
    if visit is None:
        visit = list(graph)
        if end != start:
            visit.remove(start)
    if visit == [end] and end in graph[start]:
        return [start, end]
    for child in graph[start]:
        if child in visit and child != end:
            next_visit = list(visit)
            next_visit.remove(child)
            next_start = child
            sub_path = hamiltonian_path(graph, next_start, end, next_visit)
            if sub_path is not None:
                return [start] + sub_path


def spanning_tree(graph):
    unvisited = list(graph)
    visited = [unvisited.pop()]
    tree_edges = []
    while unvisited:
        child_added = False
        shuffle(visited)
        for node in visited:
            for child in graph[node]:
                if child in unvisited:
                    tree_edges.append((node, child))
                    visited.append(child)
                    unvisited.remove(child)
                    child_added = True
                    break
            if child_added:
                break
    return tree_edges


turn_right = {
    (-1, 0): (0, 1),    # up -> right
    (0, 1): (1, 0),     # right -> down
    (1, 0): (0, -1),    # down -> left
    (0, -1): (-1, 0)    # left -> up
}

turn_left = {
    (0, 1): (-1, 0),
    (1, 0): (0, 1),
    (0, -1): (1, 0),
    (-1, 0): (0, -1)
}


def transform_edges(edges, factor, shift):
    """Scales and then shifts all the edges"""
    transform = lambda x: factor * x  + shift
    new_edges = []
    for start, end in edges:
        new_start = (transform(start[0]), transform(start[1]))
        new_end = (transform(end[0]), transform(end[1]))
        new_edges.append((new_start, new_end))
    return new_edges


def split_edges(edges):
    """Doubles the number of edges, leaving the graph the same size"""
    new_edges = []
    for start, end in edges:
        mid = midpoint(start, end)
        new_edges.append((start, mid))
        new_edges.append((mid, end))
    return new_edges


def expand_tree(edges):
    return transform_edges(split_edges(edges), 2, 0.5)


def midpoint(start, end):
    mean = lambda x, y: (x + y) / 2
    return mean(start[0], end[0]), mean(start[1], end[1])


def midpoints(edges):
    return [midpoint(edge[0], edge[1]) for edge in edges]


def hamiltonian_cycle_from_tree(grid_cycle_points, tree_midpoints):
    path = [(0, 0), (0, 1)]  # Start going rightwards
    direction = (0, 1)  # Right
    while True:
        last_node = path[-1]
        for new_direction in [turn_right[direction], direction, turn_left[direction]]:
            new_node = (last_node[0] + new_direction[0], last_node[1] + new_direction[1])
            if new_node in grid_cycle_points and new_node not in path[1:] and midpoint(last_node, new_node) not in tree_midpoints:
                path.append(new_node)
                direction = new_direction
                break
        else:
            raise ValueError("Direction not found")
        if new_node == path[0]:
            break
    return path


def hamiltonian_cycle(rows, cols, return_tree=False):
    if not (rows % 2 == 0 and cols % 2 == 0):
        raise ValueError("The number of rows and columns must both be even.")
    grid_cycle = grid_graph(rows, cols)
    grid_tree = grid_graph(rows // 2, cols // 2)
    tree = spanning_tree(grid_tree)
    tree_midpoints = midpoints(expand_tree(tree))
    hamiltonian_cycle = hamiltonian_cycle_from_tree(list(grid_cycle), tree_midpoints)
    if return_tree:
        return hamiltonian_cycle, expand_tree(tree)
    return hamiltonian_cycle


if __name__ == "__main__":
    print(hamiltonian_cycle(4, 4))
