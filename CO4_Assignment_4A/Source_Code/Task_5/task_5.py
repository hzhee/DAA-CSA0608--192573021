#!/usr/bin/env python3
"""Task 5: single-source and all-pairs shortest paths."""

from math import inf


def validate_graph(vertices, edges, source=None):
    vertex_set = set(vertices)
    if len(vertex_set) != len(vertices):
        raise ValueError("vertices must be unique")
    if source is not None and source not in vertex_set:
        raise ValueError("source must be a graph vertex")
    for u, v, _ in edges:
        if u not in vertex_set or v not in vertex_set:
            raise ValueError("every edge endpoint must be a graph vertex")


def dijkstra(vertices, edges, source, require_nonnegative=True):
    validate_graph(vertices, edges, source)
    if require_nonnegative and any(weight < 0 for _, _, weight in edges):
        raise ValueError("Dijkstra requires non-negative edge weights")
    adjacency = {vertex: [] for vertex in vertices}
    for u, v, weight in edges:
        adjacency[u].append((v, weight))

    distance = {vertex: inf for vertex in vertices}
    predecessor = {vertex: None for vertex in vertices}
    distance[source] = 0
    unsettled = set(vertices)
    trace = []
    while unsettled:
        u = min(unsettled, key=lambda vertex: distance[vertex])
        if distance[u] == inf:
            break
        unsettled.remove(u)
        updates = []
        for v, weight in adjacency[u]:
            if v in unsettled and distance[u] + weight < distance[v]:
                old_distance = distance[v]
                distance[v] = distance[u] + weight
                predecessor[v] = u
                updates.append(f"{v}:{old_distance}->{distance[v]}")
        trace.append((u, distance[u], updates))
    return distance, predecessor, trace


def bellman_ford(vertices, edges, source):
    validate_graph(vertices, edges, source)
    distance = {vertex: inf for vertex in vertices}
    predecessor = {vertex: None for vertex in vertices}
    distance[source] = 0
    passes = []
    for pass_number in range(1, len(vertices)):
        changes = []
        for u, v, weight in edges:
            if distance[u] != inf and distance[u] + weight < distance[v]:
                old_distance = distance[v]
                distance[v] = distance[u] + weight
                predecessor[v] = u
                changes.append(f"{u}->{v}:{old_distance}->{distance[v]}")
        passes.append((pass_number, changes))
        if not changes:
            break
    negative_cycle = any(
        distance[u] != inf and distance[u] + weight < distance[v]
        for u, v, weight in edges
    )
    return distance, predecessor, passes, negative_cycle


def floyd_warshall(vertices, edges):
    validate_graph(vertices, edges)
    distance = {u: {v: (0 if u == v else inf) for v in vertices} for u in vertices}
    for u, v, weight in edges:
        distance[u][v] = min(distance[u][v], weight)
    stages = []
    for k in vertices:
        updates = []
        for i in vertices:
            for j in vertices:
                through_k = distance[i][k] + distance[k][j]
                if through_k < distance[i][j]:
                    distance[i][j] = through_k
                    updates.append((i, j, through_k))
        stages.append((k, updates))
    negative_cycle = any(distance[v][v] < 0 for v in vertices)
    return distance, stages, negative_cycle


def fmt(value):
    return "INF" if value == inf else str(value)


def main():
    vertices = ["A", "B", "C", "D", "E"]
    edges = [("A", "B", 4), ("A", "C", 7), ("B", "C", 2), ("B", "D", 6),
             ("C", "D", 1), ("D", "E", 3), ("C", "E", 8)]
    print("TASK 5 - SHORTEST PATHS")
    distance, predecessor, trace = dijkstra(vertices, edges, "A")
    print("Dijkstra trace (settle vertex; relax updates):")
    for vertex, value, updates in trace:
        print(f"  {vertex} at {value}; {', '.join(updates) if updates else 'no updates'}")
    print("Dijkstra distances:", {v: fmt(distance[v]) for v in vertices})
    print("Predecessors:", predecessor)

    bf_distance, _, passes, reachable_cycle = bellman_ford(vertices, edges, "A")
    print("Bellman-Ford passes:")
    for pass_number, changes in passes:
        print(f"  {pass_number}: {', '.join(changes) if changes else 'no changes'}")
    print("Bellman-Ford distances:", {v: fmt(bf_distance[v]) for v in vertices})
    print("Reachable negative cycle:", reachable_cycle)

    all_pairs, _, any_negative_cycle = floyd_warshall(vertices, edges)
    print("Floyd-Warshall distances (rows/columns A-E):")
    print("     " + " ".join(f"{v:>4}" for v in vertices))
    for u in vertices:
        print(f"{u:>3}: " + " ".join(f"{fmt(all_pairs[u][v]):>4}" for v in vertices))
    print("Negative cycle in supplied graph:", any_negative_cycle)

    neg_vertices = ["A", "B", "C", "D"]
    neg_edges = [("A", "B", 4), ("A", "C", 5), ("C", "B", -3), ("B", "D", 2)]
    invalid_dijkstra = dijkstra(neg_vertices, neg_edges, "A", require_nonnegative=False)[0]
    valid_bf = bellman_ford(neg_vertices, neg_edges, "A")[0]
    print("Negative-edge counterexample (Dijkstra run outside its precondition):")
    print(f"  distance to D: Dijkstra={invalid_dijkstra['D']}, Bellman-Ford={valid_bf['D']}")

    cycle_edges = [("A", "B", 1), ("B", "C", -2), ("C", "B", -2)]
    reachable_cycle = bellman_ford(["A", "B", "C"], cycle_edges, "A")[3]
    print("Reachable negative-cycle test:", reachable_cycle)
    try:
        dijkstra(neg_vertices, neg_edges, "A")
        raise AssertionError("Dijkstra should reject negative edges")
    except ValueError:
        pass
    assert distance == bf_distance == {"A": 0, "B": 4, "C": 6, "D": 7, "E": 10}
    assert all_pairs["A"]["E"] == 10
    assert invalid_dijkstra["D"] == 6 and valid_bf["D"] == 4
    assert reachable_cycle
    print("Tests passed: supplied graph agreement, all-pairs distance, negative edge, negative cycle.")


if __name__ == "__main__":
    main()
