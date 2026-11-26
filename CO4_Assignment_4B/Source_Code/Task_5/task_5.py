#!/usr/bin/env python3
"""Task 5: compare Kruskal, Prim, and Boruvka minimum spanning trees."""

from heapq import heappop, heappush

VERTICES = tuple("ABCDEFGH")
BASE_EDGES = [
    ("A", "B", 4), ("A", "C", 3), ("B", "C", 1), ("B", "D", 2),
    ("C", "D", 4), ("C", "E", 5), ("D", "E", 2), ("D", "F", 3),
    ("E", "F", 1), ("E", "G", 6), ("F", "G", 2), ("F", "H", 4), ("G", "H", 3),
]


def validate(vertices, edges):
    if not vertices or len(set(vertices)) != len(vertices):
        raise ValueError("graph must have a nonempty set of unique vertices")
    valid = set(vertices)
    if any(u not in valid or v not in valid or u == v for u, v, _ in edges):
        raise ValueError("edges must connect distinct known vertices")


class DSU:
    def __init__(self, items):
        self.parent = {x: x for x in items}
        self.rank = {x: 0 for x in items}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


def kruskal(vertices, edges):
    validate(vertices, edges)
    dsu = DSU(vertices)
    chosen, trace = [], []
    ordered = sorted(((w, min(u, v), max(u, v)) for u, v, w in edges))
    for w, u, v in ordered:
        added = dsu.union(u, v)
        trace.append((u, v, w, "accept" if added else "reject: cycle"))
        if added:
            chosen.append((u, v, w))
            if len(chosen) == len(vertices) - 1:
                break
    if len(chosen) != len(vertices) - 1:
        raise ValueError("a spanning tree does not exist: graph is disconnected")
    return chosen, sum(w for _, _, w in chosen), trace


def prim(vertices, edges, start):
    validate(vertices, edges)
    if start not in vertices:
        raise ValueError("Prim start vertex must belong to the graph")
    graph = {v: [] for v in vertices}
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    visited, chosen, trace = {start}, [], []
    heap = []
    # Reverse lexical destination tie-break is deliberate and documented for the multiple-MST case.
    def push_from(u):
        for v, w in graph[u]:
            if v not in visited:
                heappush(heap, (w, tuple(-ord(ch) for ch in v), tuple(-ord(ch) for ch in u), u, v))
    push_from(start)
    while heap and len(visited) < len(vertices):
        w, _, _, u, v = heappop(heap)
        if v in visited:
            trace.append((u, v, w, "skip: endpoint already in tree"))
            continue
        visited.add(v)
        chosen.append((u, v, w))
        trace.append((u, v, w, "accept"))
        push_from(v)
    if len(visited) != len(vertices):
        raise ValueError("a spanning tree does not exist: graph is disconnected")
    return chosen, sum(w for _, _, w in chosen), trace


def boruvka(vertices, edges):
    validate(vertices, edges)
    dsu = DSU(vertices)
    chosen, rounds = [], []
    while len(chosen) < len(vertices) - 1:
        cheapest = {}
        for u, v, w in edges:
            ru, rv = dsu.find(u), dsu.find(v)
            if ru == rv:
                continue
            edge = (w, min(u, v), max(u, v), u, v)
            if ru not in cheapest or edge < cheapest[ru]:
                cheapest[ru] = edge
            if rv not in cheapest or edge < cheapest[rv]:
                cheapest[rv] = edge
        if not cheapest:
            raise ValueError("a spanning tree does not exist: graph is disconnected")
        accepted = []
        seen = set()
        for _, _, _, u, v in sorted(cheapest.values()):
            key = (min(u, v), max(u, v))
            if key in seen:
                continue
            seen.add(key)
            if dsu.union(u, v):
                chosen.append((u, v, next(w for a, b, w in edges if {a, b} == {u, v})))
                accepted.append((u, v, chosen[-1][2]))
        rounds.append(accepted)
    return chosen, sum(w for _, _, w in chosen), rounds


def display(label, result, algorithm):
    edges, cost, trace = result
    print(f"\n{label}")
    if algorithm == "Boruvka":
        for i, accepted in enumerate(trace, 1):
            print(f"Round {i}: component cheapest edges accepted: {accepted}")
    else:
        print("Decision trace (u,v,w,action):")
        for row in trace:
            print(row)
    print("MST edges:", edges)
    print("MST cost:", cost)
    return edges, cost


def run_all(vertices, edges, label, start="C"):
    print(f"\n{label}: |V|={len(vertices)}, |E|={len(edges)}")
    k = display("Kruskal", kruskal(vertices, edges), "Kruskal")
    p = display(f"Prim (start={start})", prim(vertices, edges, start), "Prim")
    b = display("Boruvka", boruvka(vertices, edges), "Boruvka")
    print("Independent verification:", "all three trees have |V|-1 edges and equal total cost" if k[1] == p[1] == b[1] and all(len(x[0]) == len(vertices)-1 for x in (k,p,b)) else "FAILED")
    return k, p, b


def main():
    print("TASK 5 - MINIMUM SPANNING TREES IN A NETWORK")
    print("Undirected weighted graph:", BASE_EDGES)
    base = run_all(VERTICES, BASE_EDGES, "BASELINE CONNECTED GRAPH")

    print("\nMULTIPLE-MST MODIFICATION")
    print("Before execution: set AB, AC, BC to weight 1. Equal-cost cycles create multiple valid MST edge sets; lexical Kruskal and reverse-lexical Prim from C are expected to select different ties.")
    modified = [(u, v, 1 if {u, v} in ({"A", "B"}, {"A", "C"}, {"B", "C"}) else w) for u, v, w in BASE_EDGES]
    varied = run_all(VERTICES, modified, "EQUAL-WEIGHT ALTERNATIVE TREES", start="C")
    print("Tie outcome check: Kruskal edges:", varied[0][0], "; Prim edges:", varied[1][0])

    print("\nENGINEERING COMPARISON")
    print("Kruskal sorts edges once: O(E log E), with near-constant amortized DSU operations; suitable for sparse edge lists.")
    print("Prim with a binary heap: O(E log V), grows one connected frontier; useful for adjacency lists and dense graphs with a matrix implementation.")
    print("Boruvka scans all edges in O(E) per phase and reduces components by at least half: O(E log V); each component can choose its cheapest outgoing edge in parallel, which fits distributed network construction.")

    assert all(len(result[0]) == len(VERTICES)-1 for result in base)
    assert base[0][1] == base[1][1] == base[2][1]
    assert varied[0][1] == varied[1][1] == varied[2][1]
    assert set(varied[0][0]) != set(varied[1][0])
    try:
        kruskal(("A", "B", "C"), [("A", "B", 1)])
    except ValueError as error:
        print("Failure test: disconnected graph rejected:", error)
    else:
        raise AssertionError("disconnected graph must not return a spanning tree")
    try:
        prim(VERTICES, BASE_EDGES, "Z")
    except ValueError:
        pass
    else:
        raise AssertionError("invalid Prim start must be rejected")
    try:
        kruskal(("A", "B"), [("A", "A", 0)])
    except ValueError:
        pass
    else:
        raise AssertionError("self-loop input must be rejected")
    negative_case = (
        kruskal(("A", "B"), [("A", "B", -2)]),
        prim(("A", "B"), [("A", "B", -2)], "A"),
        boruvka(("A", "B"), [("A", "B", -2)]),
    )
    assert all(result[1] == -2 for result in negative_case)
    print("Boundary test: negative edge accepted (-2 MST cost); self-loop rejected.")
    print("Tests passed: 8 vertices/13 edges, equal optimal costs, alternate MSTs, disconnected graph, invalid Prim root, negative weight, self-loop.")


if __name__ == "__main__":
    main()
