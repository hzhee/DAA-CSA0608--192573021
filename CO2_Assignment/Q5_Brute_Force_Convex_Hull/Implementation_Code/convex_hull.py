"""
Q5 – Brute-Force Convex Hull
Student: HRUZHEECAYSHAN T K | Reg No: 192573021
CO2 Assignment – Design and Analysis of Algorithms
"""

import math
import random


def cross_product(o, a, b):
    """
    Compute the cross product of vectors OA and OB.
    > 0: b is to the left  of line o->a  (counter-clockwise)
    < 0: b is to the right of line o->a  (clockwise)
    = 0: b is collinear with o and a
    """
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def brute_force_convex_hull(points):
    """
    Brute-force convex hull: for each directed edge (i->j),
    check that all other points lie on the same side.
    Returns hull_vertices (ordered), edge_check_count.
    """
    n = len(points)
    if n < 3:
        return points[:], 0

    hull_edges = set()
    edge_checks = 0

    for i in range(n):
        for j in range(n):
            if i == j:
                continue

            pi, pj = points[i], points[j]
            all_same_side = True
            sign = 0  # 0=undecided, 1=left, -1=right

            for k in range(n):
                if k == i or k == j:
                    continue
                edge_checks += 1
                cross = cross_product(pi, pj, points[k])

                if cross != 0:
                    s = 1 if cross > 0 else -1
                    if sign == 0:
                        sign = s
                    elif s != sign:
                        all_same_side = False
                        break

            if all_same_side:
                hull_edges.add((i, j))

    # Extract unique hull vertices
    hull_indices = set()
    for (i, j) in hull_edges:
        hull_indices.add(i)
        hull_indices.add(j)

    hull_pts = [points[i] for i in hull_indices]

    # Sort hull points by angle from centroid for ordered boundary
    if hull_pts:
        cx = sum(p[0] for p in hull_pts) / len(hull_pts)
        cy = sum(p[1] for p in hull_pts) / len(hull_pts)
        hull_pts.sort(key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

    return hull_pts, edge_checks


def print_hull_ascii(points, hull):
    """ASCII visualisation of convex hull."""
    if not points:
        return
    
    # Determine bounds
    all_x = [p[0] for p in points]
    all_y = [p[1] for p in points]
    min_x, max_x = min(all_x), max(all_x)
    min_y, max_y = min(all_y), max(all_y)

    W, H = 60, 20
    grid = [['.' for _ in range(W)] for _ in range(H)]

    def to_grid(px, py):
        gx = int((px - min_x) / max(max_x - min_x, 1) * (W - 1))
        gy = H - 1 - int((py - min_y) / max(max_y - min_y, 1) * (H - 1))
        return max(0, min(W-1, gx)), max(0, min(H-1, gy))

    hull_set = set(map(tuple, hull))

    for p in points:
        gx, gy = to_grid(p[0], p[1])
        if tuple(p) in hull_set:
            grid[gy][gx] = 'H'  # Hull vertex
        else:
            grid[gy][gx] = '*'  # Interior point

    print("\n  ASCII Visualisation (H=Hull vertex, *=Interior point):")
    print("  " + "┌" + "─" * W + "┐")
    for row in grid:
        print("  │" + ''.join(row) + "│")
    print("  " + "└" + "─" * W + "┘")


def run_experiments():
    print("=" * 70)
    print("Q5 – BRUTE-FORCE CONVEX HULL")
    print("Student: HRUZHEECAYSHAN T K | Reg No: 192573021")
    print("=" * 70)

    # ── TEST 1: Boundary + Interior points ──
    print("\n" + "─" * 70)
    print("TEST 1: Mixed Boundary and Interior Points")
    print("─" * 70)
    points1 = [(0,0), (4,0), (4,4), (0,4), (2,2), (1,1), (3,3), (2,0.5)]
    hull1, checks1 = brute_force_convex_hull(points1)
    print(f"\n  Input Points:  {points1}")
    print(f"  Hull Vertices: {hull1}")
    print(f"  Edge Checks:   {checks1}")
    print(f"  Theory O(n³):  n(n-1)(n-2) = {len(points1)*(len(points1)-1)*(len(points1)-2)}")
    print_hull_ascii(points1, hull1)

    # ── TEST 2: Challenging – collinear points ──
    print("\n" + "─" * 70)
    print("TEST 2: Challenging Configuration – Collinear Points")
    print("─" * 70)
    points2 = [(0,0),(1,0),(2,0),(2,2),(1,2),(0,2),(1,1),(0.5,0.5)]
    hull2, checks2 = brute_force_convex_hull(points2)
    print(f"\n  Input Points:  {points2}")
    print(f"  Hull Vertices: {hull2}")
    print(f"  Edge Checks:   {checks2}")
    print(f"  Theory O(n³):  {len(points2)*(len(points2)-1)*(len(points2)-2)}")
    print_hull_ascii(points2, hull2)

    # ── GROWTH ANALYSIS ──
    print("\n" + "─" * 70)
    print("GROWTH ANALYSIS: Edge Checks vs n")
    print("─" * 70)
    print(f"\n  {'n':>6} | {'Edge Checks':>14} | {'Theory n(n-1)(n-2)':>20} | {'Ratio':>8}")
    print(f"  {'─'*6}─|─{'─'*14}─|─{'─'*20}─|─{'─'*8}")

    prev = None
    for n in [5, 8, 10, 15, 20]:
        pts = [(random.uniform(0, 10), random.uniform(0, 10)) for _ in range(n)]
        _, checks = brute_force_convex_hull(pts)
        theory = n * (n - 1) * (n - 2)
        ratio = f"{checks / prev:.2f}x" if prev else "─"
        print(f"  {n:>6} | {checks:>14,} | {theory:>20,} | {ratio:>8}")
        prev = checks

    print("""
  GROWTH OBSERVATION:
    When n doubles: edge checks ≈ multiply by 8 (confirms O(n³)).
    n=10 → n=20: ~720 → ~6,840 ≈ 9.5x (theoretical: 2³=8x for doubling)

  CORRECTNESS ARGUMENT (Geometric Reasoning):
    An edge (P_i → P_j) lies on the convex hull if and only if ALL
    other points lie on the SAME SIDE of the directed line P_i → P_j.

    WHY THIS IS CORRECT:
      The convex hull is the smallest convex polygon containing all points.
      By definition, every edge of a convex polygon has ALL other polygon
      vertices (and enclosed points) on ONE side – the interior side.
      If even one point were on the opposite side, the polygon would be
      CONCAVE at that edge, violating the convexity requirement.

      The cross product of vectors (P_i→P_j) and (P_i→P_k) gives the
      SIGNED AREA of the triangle (P_i, P_j, P_k). Its sign tells us
      which side of line P_i→P_j the point P_k lies on.

      If ALL cross products have the SAME SIGN (or are zero/collinear),
      then ALL points are on ONE side → the edge is a valid hull edge.

      This is a geometric necessity, not an empirical observation.
    """)


if __name__ == "__main__":
    random.seed(42)
    run_experiments()
