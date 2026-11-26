#!/usr/bin/env python3
"""Task 6: Held-Karp exact TSP dynamic programming and independent checks."""

from itertools import permutations
from statistics import median
from time import perf_counter
import tracemalloc


def validate_matrix(cost, hub=0):
    n = len(cost)
    if n < 2 or any(len(row) != n for row in cost):
        raise ValueError("cost matrix must be square and contain a hub and at least one stop")
    if not 0 <= hub < n:
        raise ValueError("hub index is outside the matrix")
    if any(cost[i][i] != 0 for i in range(n)):
        raise ValueError("diagonal travel costs must be zero")
    if any(cost[i][j] < 0 for i in range(n) for j in range(n) if i != j):
        raise ValueError("travel costs must be nonnegative")


def held_karp(cost, hub=0):
    validate_matrix(cost, hub)
    nodes = [i for i in range(len(cost)) if i != hub]
    bit = {node: 1 << i for i, node in enumerate(nodes)}
    dp, parent, updates = {}, {}, 0
    for j in nodes:
        state = (bit[j], j)
        dp[state] = cost[hub][j]
        parent[state] = None
    for size in range(2, len(nodes) + 1):
        for mask in range(1, 1 << len(nodes)):
            if mask.bit_count() != size:
                continue
            for j in nodes:
                if not mask & bit[j]:
                    continue
                prev_mask = mask ^ bit[j]
                candidates = [(dp[(prev_mask, i)] + cost[i][j], i)
                              for i in nodes if prev_mask & bit[i]]
                best_cost, best_prev = min(candidates)
                dp[(mask, j)] = best_cost
                parent[(mask, j)] = best_prev
                updates += len(candidates)
    full = (1 << len(nodes)) - 1
    total, last = min((dp[(full, j)] + cost[j][hub], j) for j in nodes)
    reverse_route = [last]
    mask, current = full, last
    while parent[(mask, current)] is not None:
        previous = parent[(mask, current)]
        mask ^= bit[current]
        current = previous
        reverse_route.append(current)
    route = [hub] + list(reversed(reverse_route)) + [hub]
    return total, route, dp, parent, updates


def brute_force(cost, hub=0):
    stops = [i for i in range(len(cost)) if i != hub]
    best = None
    best_route = None
    for order in permutations(stops):
        route = (hub,) + order + (hub,)
        total = sum(cost[route[i]][route[i + 1]] for i in range(len(route) - 1))
        if best is None or total < best:
            best, best_route = total, route
    return best, list(best_route)


def deterministic_matrix(n):
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            value = ((i + 3) * (j + 7) + abs(i - j) * 11) % 40 + 5
            matrix[i][j] = matrix[j][i] = value
    return matrix


def timed_run(cost):
    tracemalloc.start()
    start = perf_counter()
    answer = held_karp(cost)
    elapsed = perf_counter() - start
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return answer, elapsed, peak


def main():
    labels = ("Hub", "A", "B", "C", "D", "E", "F")
    matrix = [
        [0, 10, 15, 20, 12, 18, 25],
        [10, 0, 8, 12, 9, 14, 20],
        [15, 8, 0, 10, 16, 11, 18],
        [20, 12, 10, 0, 7, 13, 9],
        [12, 9, 16, 7, 0, 6, 11],
        [18, 14, 11, 13, 6, 0, 10],
        [25, 20, 18, 9, 11, 10, 0],
    ]
    print("TASK 6 - HELD-KARP TRAVELING SALESPERSON DESIGN CHALLENGE")
    print("Locations:", labels)
    print("Symmetric travel cost matrix:")
    print("     " + " ".join(f"{name:>5}" for name in labels))
    for label, row in zip(labels, matrix):
        print(f"{label:>5} " + " ".join(f"{value:>5}" for value in row))
    answer, elapsed, peak = timed_run(matrix)
    total, route, dp, _, transitions = answer
    print("State definition: DP[S,j] is the least cost from Hub, visiting exactly S, and ending at j.")
    print("Optimal tour:", " -> ".join(labels[i] for i in route))
    print("Minimum tour cost:", total)
    print("Final-state comparison:", [(labels[j], dp[((1 << 6) - 1, j)] + matrix[j][0]) for j in range(1, 7)])
    print("DP states stored:", len(dp), "(expected m*2^(m-1) = 192)")
    print("Predecessor transitions evaluated:", transitions)
    print(f"Observed execution: {elapsed * 1000:.3f} ms; Python traced peak memory: {peak / 1024:.1f} KiB")

    small = [row[:5] for row in matrix[:5]]
    exact_dp = held_karp(small)
    exact_brute = brute_force(small)
    print("\nINDEPENDENT VALIDATION ON FOUR DELIVERY STOPS")
    print("Held-Karp:", exact_dp[0], "route", [labels[i] for i in exact_dp[1]])
    print("Exhaustive permutation enumeration:", exact_brute[0], "route", [labels[i] for i in exact_brute[1]], "(4! = 24 tours)")
    assert exact_dp[0] == exact_brute[0]

    print("\nSCALING EXPERIMENT (three runs; median time and maximum traced memory)")
    print("Stops | theoretical states | observed states | predecessor transitions | median ms | max KiB")
    for stops in range(4, 9):
        sample = deterministic_matrix(stops + 1)
        runs = [timed_run(sample) for _ in range(3)]
        observed_states = len(runs[0][0][2])
        times = [result[1] * 1000 for result in runs]
        peak_kib = max(result[2] for result in runs) / 1024
        transitions_for_n = runs[0][0][4]
        print(f"{stops:>5} | {stops * 2**(stops-1):>18} | {observed_states:>14} | {transitions_for_n:>23} | {median(times):>8.3f} | {peak_kib:>7.1f}")

    print("\nLARGE-SCALE FEASIBILITY (200 delivery locations)")
    print("Exact Held-Karp would store 200*2^199 =", 200 * 2**199, "states and examine on the order of n^2*2^n transitions; it is infeasible in ordinary memory and time. No exact run is attempted.")
    print("For a seconds-scale, approximate requirement, use multi-start nearest-neighbor construction followed by 2-opt improvement. This polynomial-time local search returns a feasible tour quickly but has no general optimality guarantee; use Christofides when a metric-cost 1.5-approximation guarantee is required and its extra construction cost is acceptable.")

    reflection = ("Held-Karp replaces repeated route enumeration with overlapping subset states. Each state DP[S,j] stores the cheapest partial tour ending at j after visiting S, and a predecessor reconstructs an optimal route. The method is exact, so it also provides a useful benchmark for heuristics on small instances. Its cost is exponential: with m delivery locations it stores O(m 2^m) states and takes O(m^2 2^m) time. It fits small routing problems where optimality matters and memory is sufficient; for hundreds of locations, multi-start construction plus local improvement is more practical when a fast, high-quality tour is acceptable.")
    print("\nREFLECTION (", len(reflection.split()), "words)")
    print(reflection)
    assert len(route) == 8 and route[0] == route[-1] == 0 and len(set(route[1:-1])) == 6
    assert total == sum(matrix[route[i]][route[i+1]] for i in range(len(route)-1))
    try:
        held_karp([[0, -1], [-1, 0]])
    except ValueError:
        pass
    else:
        raise AssertionError("negative travel cost must be rejected")
    try:
        held_karp([[0]])
    except ValueError:
        pass
    else:
        raise AssertionError("a hub with no delivery stops must be rejected")
    print("Boundary tests: negative travel cost and zero delivery stops rejected.")
    print("Tests passed: six-stop route, return to hub, independent brute-force optimum, scaling counts, invalid matrix boundaries.")


if __name__ == "__main__":
    main()
