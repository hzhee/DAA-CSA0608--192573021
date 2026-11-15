"""
Q4 – Brute-Force Closest Pair of Points
Student: HRUZHEECAYSHAN T K | Reg No: 192573021
CO2 Assignment – Design and Analysis of Algorithms
"""

import math
import random


def euclidean_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def brute_force_closest_pair(points):
    """
    Find the closest pair of points using brute force O(n^2).
    Returns: (p1, p2, min_distance, distance_calculations)
    """
    n = len(points)
    min_dist = float('inf')
    closest_pair = (None, None)
    dist_calcs = 0

    for i in range(n - 1):
        for j in range(i + 1, n):
            dist_calcs += 1
            d = euclidean_distance(points[i], points[j])
            if d < min_dist:
                min_dist = d
                closest_pair = (points[i], points[j])

    return closest_pair[0], closest_pair[1], min_dist, dist_calcs


def run_experiments():
    print("=" * 70)
    print("Q4 – BRUTE-FORCE CLOSEST PAIR OF POINTS")
    print("Student: HRUZHEECAYSHAN T K | Reg No: 192573021")
    print("=" * 70)

    # ── TEST 1: Small dataset with manual verification ──
    print("\n" + "─" * 70)
    print("TEST 1: Small Dataset (Boundary + Interior Points) n=8")
    print("─" * 70)
    points1 = [(0,0), (10,0), (10,10), (0,10), (5,5), (3,3), (7,8), (1,9)]
    p1, p2, min_d, calcs = brute_force_closest_pair(points1)
    print(f"\n  Points: {points1}")
    print(f"\n  Closest Pair:  {p1}  and  {p2}")
    print(f"  Min Distance:  {min_d:.4f}")
    print(f"  Distance Calcs: {calcs}")
    print(f"  Theory: n(n-1)/2 = {len(points1)*(len(points1)-1)//2}")

    # Verify manually
    print("\n  Manual verification (all pairwise distances):")
    n = len(points1)
    print(f"  {'Pair':>20} | {'Distance':>10}")
    print(f"  {'─'*20}─|─{'─'*10}")
    for i in range(n - 1):
        for j in range(i + 1, n):
            d = euclidean_distance(points1[i], points1[j])
            marker = " ← CLOSEST" if abs(d - min_d) < 1e-9 else ""
            print(f"  {str(points1[i]):>10} ↔ {str(points1[j]):<10} | {d:>10.4f}{marker}")

    # ── TEST 2: Dense cluster (challenging case) ──
    print("\n" + "─" * 70)
    print("TEST 2: Dense Random Cluster (Challenging Configuration) n=20")
    print("─" * 70)
    random.seed(99)
    points2 = [(round(random.uniform(0, 5), 2), round(random.uniform(0, 5), 2))
               for _ in range(20)]
    p1, p2, min_d, calcs = brute_force_closest_pair(points2)
    print(f"\n  Closest Pair:  {p1}  and  {p2}")
    print(f"  Min Distance:  {min_d:.4f}")
    print(f"  Distance Calcs: {calcs}")
    print(f"  Theory: {len(points2)*(len(points2)-1)//2}")

    # ── EXPERIMENT: Growth Analysis ──
    print("\n" + "─" * 70)
    print("EXPERIMENT: Growth Analysis – Distance Calculations vs n")
    print("─" * 70)
    print(f"\n  {'n':>8} | {'Dist Calcs':>14} | {'Theory n(n-1)/2':>16} | {'Ratio (prev)':>14}")
    print(f"  {'─'*8}─|─{'─'*14}─|─{'─'*16}─|─{'─'*14}")

    prev_calcs = None
    sizes = [10, 20, 50, 100, 200, 500, 1000]
    for n in sizes:
        pts = [(random.uniform(0, 100), random.uniform(0, 100)) for _ in range(n)]
        _, _, _, calcs = brute_force_closest_pair(pts)
        theory = n * (n - 1) // 2
        ratio = f"{calcs / prev_calcs:.2f}x" if prev_calcs else "─"
        print(f"  {n:>8} | {calcs:>14,} | {theory:>16,} | {ratio:>14}")
        prev_calcs = calcs

    print("""
  GROWTH OBSERVATION:
    When n doubles: distance calculations ≈ quadruple (4x).
    This confirms T(n) = n(n-1)/2 ∈ Θ(n²).

    n doubles from 100 → 200: calcs go from ~4,950 → ~19,900 (≈4x) ✓
    n doubles from 500 → 1000: calcs go from ~124,750 → ~499,500 (≈4x) ✓

  MATHEMATICAL DERIVATION:
    Total pairs = Σ(i=0 to n-2)(n-1-i) = n(n-1)/2
    For n=1000: 1000×999/2 = 499,500 distance calculations.

  LIMITATION IDENTIFICATION:
    Brute-force O(n²) is impractical for large drone fleets (n > 100,000).
    At n=100,000: ~5,000,000,000 calculations – infeasible in real-time.
    Solution: Divide-and-Conquer Closest Pair runs in O(n log n).
    """)


if __name__ == "__main__":
    random.seed(42)
    run_experiments()
