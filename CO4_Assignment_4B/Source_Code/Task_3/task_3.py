#!/usr/bin/env python3
"""Task 3: routing under nonnegative, negative-edge, and negative-cycle conditions."""

from math import inf

VERTICES = tuple("ABCDEFGH")
BASE_EDGES = [
    ("A", "B", 2), ("A", "C", 5), ("B", "D", 2), ("B", "E", 6),
    ("C", "B", 1), ("C", "D", 1), ("C", "F", 5), ("D", "E", 1),
    ("D", "G", 4), ("E", "H", 2), ("F", "E", 1), ("G", "H", 1),
]


def validate_graph(vertices, edges, source=None):
    valid = set(vertices)
    if len(valid) != len(vertices):
        raise ValueError("vertex IDs must be unique")
    if source is not None and source not in valid:
        raise ValueError("source must belong to the graph")
    if any(u not in valid or v not in valid for u, v, _ in edges):
        raise ValueError("every edge endpoint must belong to the graph")


def adjacency(vertices, edges):
    graph = {v: [] for v in vertices}
    for u, v, weight in edges:
        graph[u].append((v, weight))
    return graph


def dijkstra(vertices, edges, source, require_nonnegative=True):
    validate_graph(vertices, edges, source)
    if require_nonnegative and any(weight < 0 for _, _, weight in edges):
        raise ValueError("Dijkstra requires nonnegative edge weights")
    graph = adjacency(vertices, edges)
    distance = {v: inf for v in vertices}
    predecessor = {v: None for v in vertices}
    distance[source] = 0
    unsettled = set(vertices)
    trace = []
    while unsettled:
        u = min(unsettled, key=lambda v: (distance[v], v))
        if distance[u] == inf:
            break
        unsettled.remove(u)
        changes = []
        for v, weight in graph[u]:
            if v in unsettled and distance[u] + weight < distance[v]:
                old = distance[v]
                distance[v] = distance[u] + weight
                predecessor[v] = u
                changes.append(f"{v}:{old}->{distance[v]}")
        trace.append((u, distance[u], tuple(changes)))
    return distance, predecessor, trace


def bellman_ford(vertices, edges, source):
    validate_graph(vertices, edges, source)
    distance = {v: inf for v in vertices}
    predecessor = {v: None for v in vertices}
    distance[source] = 0
    passes = []
    for pass_number in range(1, len(vertices)):
        changes = []
        for u, v, weight in edges:
            if distance[u] != inf and distance[u] + weight < distance[v]:
                old = distance[v]
                distance[v] = distance[u] + weight
                predecessor[v] = u
                changes.append(f"{u}->{v}:{old}->{distance[v]}")
        passes.append((pass_number, tuple(changes)))
        if not changes:
            break
    negative_cycle = any(
        distance[u] != inf and distance[u] + weight < distance[v]
        for u, v, weight in edges
    )
    return distance, predecessor, passes, negative_cycle


def reconstruct_path(predecessor, source, target):
    if target not in predecessor:
        raise ValueError("target must belong to the graph")
    path = []
    current = target
    seen = set()
    while current is not None:
        if current in seen:
            return ["predecessor cycle"]
        seen.add(current)
        path.append(current)
        if current == source:
            return list(reversed(path))
        current = predecessor[current]
    return []


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
                candidate = distance[i][k] + distance[k][j]
                if candidate < distance[i][j]:
                    distance[i][j] = candidate
                    updates.append((i, j, candidate))
        stages.append((k, updates))
    negative_cycle = any(distance[v][v] < 0 for v in vertices)
    return distance, stages, negative_cycle


def warshall(vertices, edges):
    validate_graph(vertices, edges)
    reachable = {u: {v: u == v for v in vertices} for u in vertices}
    for u, v, _ in edges:
        reachable[u][v] = True
    stages = []
    for k in vertices:
        added = []
        for i in vertices:
            for j in vertices:
                if not reachable[i][j] and reachable[i][k] and reachable[k][j]:
                    reachable[i][j] = True
                    added.append((i, j))
        stages.append((k, added))
    return reachable, stages


def fmt(value):
    return "INF" if value == inf else str(value)


def print_distances(label, vertices, distance, source):
    print(label)
    print(source, ":", {target: fmt(distance[target]) for target in vertices})


def main():
    print("TASK 3 - ROUTING ENGINE UNDER CHANGING NETWORK CONDITIONS")
    print("Vertices:", ", ".join(VERTICES))
    print("BASE DIRECTED EDGES (12):", BASE_EDGES)

    dist, pred, settled = dijkstra(VERTICES, BASE_EDGES, "A")
    base_bf_dist = bellman_ford(VERTICES, BASE_EDGES, "A")[0]
    print("\nSTAGE A - DIJKSTRA, SOURCE A")
    print("Finalization order and relaxations:")
    for vertex, value, changes in settled:
        print(f"{vertex} finalized at {value}; relaxations: {', '.join(changes) if changes else 'none'}")
    print_distances("Distances from A:", VERTICES, dist, "A")
    print("Predecessors:", pred)
    for target in VERTICES:
        print(f"Path A->{target}:", "->".join(reconstruct_path(pred, "A", target)) or "unreachable")

    negative_edges = [(u, v, -4 if (u, v) == ("C", "B") else w) for u, v, w in BASE_EDGES]
    print("\nSTAGE B - PREDICTION BEFORE EXECUTION")
    print("Replace C->B weight +1 by -4. Prediction: Dijkstra's nonnegative-weight assumption is violated; after finalizing B at 2, the later A->C->B route costs 1 and may be ignored. Bellman-Ford should revise B and its descendants.")
    print("Modified edge list:", negative_edges)
    unsafe_dist, unsafe_pred, unsafe_trace = dijkstra(VERTICES, negative_edges, "A", require_nonnegative=False)
    bf_dist, bf_pred, bf_passes, has_cycle = bellman_ford(VERTICES, negative_edges, "A")
    print("Experimental Dijkstra finalization:", [(u, d) for u, d, _ in unsafe_trace])
    print("Experimental Dijkstra distances:", {v: fmt(unsafe_dist[v]) for v in VERTICES})
    print("Bellman-Ford pass updates:")
    for number, changes in bf_passes:
        print(number, ":", ", ".join(changes) if changes else "no changes")
    print("Bellman-Ford distances:", {v: fmt(bf_dist[v]) for v in VERTICES})
    print("Bellman-Ford path A->H:", "->".join(reconstruct_path(bf_pred, "A", "H")))
    print("Prediction check: B distance is", fmt(unsafe_dist["B"]), "under Dijkstra and", fmt(bf_dist["B"]), "under Bellman-Ford.")

    cycle_edges = negative_edges + [("D", "C", -5)]
    cycle_dist, _, cycle_passes, cycle_detected = bellman_ford(VERTICES, cycle_edges, "A")
    print("\nSTAGE C - REACHABLE NEGATIVE-CYCLE FAILURE")
    print("Added D->C=-5. The reachable cycle C->B->D->C has total weight -4+2-5=-7.")
    print("Bellman-Ford passes:", len(cycle_passes), "of at most", len(VERTICES)-1)
    print("Negative cycle detected by an additional relaxability scan:", cycle_detected)
    if cycle_detected:
        print("Shortest-path values are not reported for this graph because repeated cycle traversal can lower cost without bound.")

    all_distance, fw_stages, fw_cycle = floyd_warshall(VERTICES, negative_edges)
    reach, warshall_stages = warshall(VERTICES, negative_edges)
    print("\nSTAGE D - ALL-PAIRS ANALYTICS ON THE NEGATIVE-EDGE, NO-CYCLE GRAPH")
    print("Floyd intermediate vertices and improved pairs:")
    for k, changes in fw_stages:
        print(k, ":", changes)
    print("Floyd distance matrix (rows are sources, columns are destinations):")
    print("    " + " ".join(f"{v:>4}" for v in VERTICES))
    for u in VERTICES:
        print(f"{u:>3} " + " ".join(f"{fmt(all_distance[u][v]):>4}" for v in VERTICES))
    print("Floyd reports negative cycle:", fw_cycle)
    print("Warshall intermediate vertices and newly reachable pairs:")
    for k, added in warshall_stages:
        print(k, ":", added)
    print("Warshall reachability matrix (1=reachable, including self):")
    print("    " + " ".join(f"{v:>3}" for v in VERTICES))
    for u in VERTICES:
        print(f"{u:>3} " + " ".join(f"{int(reach[u][v]):>3}" for v in VERTICES))

    disconnected = dijkstra(("A", "B", "Z"), [("A", "B", 1)], "A")[0]
    disconnected_reach, _ = warshall(("A", "B", "Z"), [("A", "B", 1)])
    try:
        dijkstra(VERTICES, negative_edges, "A")
    except ValueError as error:
        strict_negative_rejected = True
        print("Boundary validation: strict Dijkstra rejects the negative edge:", error)
    else:
        strict_negative_rejected = False
    assert [v for v, _, _ in settled] == ["A", "B", "D", "C", "E", "H", "G", "F"]
    assert dist == base_bf_dist
    assert unsafe_dist["B"] == 2 and bf_dist["B"] == 1
    assert unsafe_dist["H"] != bf_dist["H"]
    assert cycle_detected and not fw_cycle
    assert disconnected["Z"] == inf and not disconnected_reach["A"]["Z"]
    assert strict_negative_rejected
    print("Tests passed: 8 vertices/12 edges, route reconstruction, negative-edge divergence, reachable negative cycle, all-pairs matrices, unreachable vertex.")


if __name__ == "__main__":
    main()
