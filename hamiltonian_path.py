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


# rows, cols = 6, 6
# graph = grid_graph(rows, cols)
# print(graph)
# start = (0, 0)
# end = (0, 0)

# path = hamiltonian_path(graph, start, end)
# print(path)


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


graph = grid_graph(6, 6)
tree1 = spanning_tree(graph)
tree2 = spanning_tree(graph)
print(tree1)
print(tree2)
