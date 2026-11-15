"""
Q6 – Exhaustive Search: Humanitarian Airlift Planning (Knapsack)
Student: HRUZHEECAYSHAN T K | Reg No: 192573021
CO2 Assignment – Design and Analysis of Algorithms
"""

import time
import itertools


# ─────────────────────────────────────────────
# PACKAGE DATA (Humanitarian Airlift)
# ─────────────────────────────────────────────
PACKAGES = [
    {"id": 1, "weight": 2, "value": 6,  "name": "Medical Kits"},
    {"id": 2, "weight": 3, "value": 7,  "name": "Food Packs"},
    {"id": 3, "weight": 4, "value": 8,  "name": "Water Supplies"},
    {"id": 4, "weight": 5, "value": 9,  "name": "Shelter Tarps"},
    {"id": 5, "weight": 1, "value": 3,  "name": "First Aid"},
    {"id": 6, "weight": 6, "value": 11, "name": "Generator"},
    {"id": 7, "weight": 2, "value": 5,  "name": "Blankets"},
]
PAYLOAD_LIMIT = 8


def exhaustive_knapsack(packages, capacity):
    """
    Exhaustive search: enumerate ALL 2^n subsets.
    Returns: best_subset, best_weight, best_value, combos_examined
    """
    n = len(packages)
    total_subsets = 2 ** n
    best_value  = 0
    best_weight = 0
    best_subset = []
    combos_examined = 0

    for mask in range(total_subsets):
        combos_examined += 1
        curr_weight = 0
        curr_value  = 0
        curr_subset = []

        for i in range(n):
            if mask & (1 << i):             # bit i is set → package i selected
                curr_weight += packages[i]["weight"]
                curr_value  += packages[i]["value"]
                curr_subset.append(packages[i])

        # Feasibility check
        if curr_weight <= capacity:
            if curr_value > best_value:
                best_value  = curr_value
                best_weight = curr_weight
                best_subset = curr_subset[:]

    return best_subset, best_weight, best_value, combos_examined, total_subsets


def correctness_check():
    """Small instance for independent manual verification."""
    print("\n" + "─" * 70)
    print("CORRECTNESS CHECK – Small Instance (n=3, W=5)")
    print("─" * 70)
    small_pkgs = [
        {"id": 1, "weight": 2, "value": 6,  "name": "P1"},
        {"id": 2, "weight": 3, "value": 7,  "name": "P2"},
        {"id": 3, "weight": 4, "value": 8,  "name": "P3"},
    ]
    W = 5

    print(f"\n  Packages: P1(w=2,v=6), P2(w=3,v=7), P3(w=4,v=8) | Limit W={W}")
    print(f"\n  {'Subset':>20} | {'Weight':>7} | {'Value':>6} | {'Feasible':>9} | {'Note':>15}")
    print(f"  {'─'*20}─|─{'─'*7}─|─{'─'*6}─|─{'─'*9}─|─{'─'*15}")

    all_subsets = []
    for mask in range(8):
        subset = []
        w = v = 0
        for i in range(3):
            if mask & (1 << i):
                subset.append(small_pkgs[i]["name"])
                w += small_pkgs[i]["weight"]
                v += small_pkgs[i]["value"]
        feasible = w <= W
        note = "← OPTIMAL" if (feasible and v == 13) else ""
        label = "{" + ",".join(subset) + "}" if subset else "{}"
        print(f"  {label:>20} | {w:>7} | {v:>6} | {'YES' if feasible else 'NO':>9} | {note:>15}")

    best, bw, bv, examined, total = exhaustive_knapsack(small_pkgs, W)
    print(f"\n  Algorithm found: {[p['name'] for p in best]} | Weight={bw} | Value={bv}")
    print(f"  Subsets examined: {examined} of {total}")
    print(f"  VERIFICATION: {'✓ CORRECT (matches manual)' if bv == 13 else '✗ MISMATCH'}")


def run_main_experiment():
    print("\n" + "─" * 70)
    print("MAIN EXPERIMENT – Humanitarian Airlift (n=5, W=8)")
    print("─" * 70)
    pkgs5 = PACKAGES[:5]
    print(f"\n  Package List:")
    print(f"  {'ID':>4} | {'Name':>15} | {'Weight':>7} | {'Value':>6}")
    print(f"  {'─'*4}─|─{'─'*15}─|─{'─'*7}─|─{'─'*6}")
    for p in pkgs5:
        print(f"  {p['id']:>4} | {p['name']:>15} | {p['weight']:>7} | {p['value']:>6}")
    print(f"\n  Payload Limit: {PAYLOAD_LIMIT} kg")

    best, bw, bv, examined, total = exhaustive_knapsack(pkgs5, PAYLOAD_LIMIT)
    print(f"\n  RESULT:")
    print(f"  Best Subset:    {[p['name'] for p in best]}")
    print(f"  Total Weight:   {bw} kg (limit: {PAYLOAD_LIMIT} kg)")
    print(f"  Total Value:    {bv}")
    print(f"  Subsets Examined: {examined} of {total} (2^{len(pkgs5)}={total})")


def growth_investigation():
    print("\n" + "─" * 70)
    print("GROWTH INVESTIGATION – Exponential Scaling")
    print("─" * 70)
    print("\n  Prediction: T(n) = 2^n combinations")
    print(f"\n  {'n':>5} | {'2^n (theory)':>15} | {'Actual examined':>16} | {'Time (ms)':>12} | {'Feasible':>9}")
    print(f"  {'─'*5}─|─{'─'*15}─|─{'─'*16}─|─{'─'*12}─|─{'─'*9}")

    import random
    random.seed(123)
    for n in [5, 10, 15, 20, 23, 25]:
        # Generate n random packages
        pkgs = [{"id": i+1, "weight": random.randint(1, 10),
                 "value": random.randint(1, 20), "name": f"P{i+1}"}
                for i in range(n)]
        cap = n * 3  # moderate capacity

        t0 = time.perf_counter()
        _, _, bv, examined, total = exhaustive_knapsack(pkgs, cap)
        elapsed_ms = (time.perf_counter() - t0) * 1000

        feasible_count = sum(
            1 for mask in range(total)
            if sum(pkgs[i]["weight"] for i in range(n) if mask & (1 << i)) <= cap
        ) if n <= 20 else "skip"

        print(f"  {n:>5} | {total:>15,} | {examined:>16,} | {elapsed_ms:>12.2f} | {str(feasible_count):>9}")

    print("""
  EXPONENTIAL GROWTH EXPLANATION:
    Adding ONE package to n packages DOUBLES the solution space.
    Reason: Every existing subset can now INCLUDE or EXCLUDE the new package.
    This binary branching at each step gives: |subsets| = 2^n.

    Example: n=25 → n=26 adds 33,554,432 NEW candidate subsets.
    No matter how smart our evaluation, we must examine all 2^n combinations.

    This is unavoidable for exhaustive search – it is the FUNDAMENTAL cost
    of guaranteeing that the optimal solution is found by enumeration alone.

  DEPLOYMENT DECISION:
    Fixed response time: 5 seconds (justified: emergency context needs fast decision)
    Observed rate: ~1,000,000 subsets/second (Python)

    n=20: 1,048,576 subsets / 1,000,000 per sec ≈ 1 sec   [DEPLOY]
    n=23: 8,388,608 subsets / 1,000,000 per sec ≈ 8 sec   [BORDERLINE]
    n=25: 33,554,432 subsets / 1,000,000 per sec ≈ 33 sec [DO NOT DEPLOY]

    DEPLOYMENT BOUNDARY: n ≤ 22 packages for a 5-second response guarantee.
    For n > 22: use Dynamic Programming (O(nW)) or Branch-and-Bound.
    """)


if __name__ == "__main__":
    print("=" * 70)
    print("Q6 – EXHAUSTIVE SEARCH: HUMANITARIAN AIRLIFT PLANNING")
    print("Student: HRUZHEECAYSHAN T K | Reg No: 192573021")
    print("=" * 70)

    correctness_check()
    run_main_experiment()
    growth_investigation()
