from typing import Optional


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


# TODO: I think avoid is always the negation of visit and so you don't need it.
def hamiltonian_path(graph: dict[int, list[int]], start: int, end: int, visit: Optional[set[int]]=None, avoid: Optional[set[int]]=None):
    if visit is None:
        visit = list(graph)
        if end != start:
            visit.remove(start)
    if avoid is None:
        if end == start:
            avoid = set()
        else:
            avoid = {start}
    if visit == [end] and end in graph[start]:
        return [start, end]
    for child in graph[start]:
        if child in visit and child not in avoid and child != end:
            next_visit, next_avoid = list(visit), list(avoid)
            next_visit.remove(child)
            next_avoid.append(child)
            next_start = child
            sub_path = hamiltonian_path(graph, next_start, end, next_visit, next_avoid)
            if sub_path is not None:
                return [start] + sub_path


rows, cols = 6, 6
graph = grid_graph(rows, cols)
start = (0, 0)
end = (0, 0)

path = hamiltonian_path(graph, start, end)
print(path)
