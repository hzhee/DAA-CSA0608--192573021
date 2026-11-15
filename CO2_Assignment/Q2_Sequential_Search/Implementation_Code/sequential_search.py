"""
Q2 – Sequential Search Engineering Decision
Student: HRUZHEECAYSHAN T K | Reg No: 192573021
CO2 Assignment – Design and Analysis of Algorithms
"""

import random
import math

def sequential_search(arr, target):
    """Sequential search with comparison counting."""
    comparisons = 0
    for i, elem in enumerate(arr):
        comparisons += 1
        if elem == target:
            return i, comparisons
    return -1, comparisons


def run_experiments():
    print("=" * 70)
    print("Q2 – SEQUENTIAL SEARCH: ENGINEERING DECISION ANALYSIS")
    print("Student: HRUZHEECAYSHAN T K | Reg No: 192573021")
    print("=" * 70)

    # ── EXPERIMENT 1: Successful searches at different positions ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 1: Successful Searches at Different Positions (n=100)")
    print("─" * 70)

    n = 100
    tools = [f"T-{i:03d}" for i in range(1, n + 1)]
    positions = [0, 9, 24, 49, 74, 99]  # 1st, 10th, 25th, 50th, 75th, last

    print(f"\n  {'Target':>10} | {'Position':>10} | {'Comparisons':>12} | {'Theory':>8}")
    print(f"  {'-'*10}─|─{'-'*10}─|─{'-'*12}─|─{'-'*8}")
    for pos in positions:
        target = tools[pos]
        idx, comps = sequential_search(tools, target)
        theory = pos + 1
        print(f"  {target:>10} | {pos+1:>10} | {comps:>12} | {theory:>8}")

    # ── EXPERIMENT 2: Unsuccessful searches ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 2: Unsuccessful Search (n=100)")
    print("─" * 70)
    target_absent = "T-999"
    idx, comps = sequential_search(tools, target_absent)
    print(f"\n  Searching for '{target_absent}' in list of {n} tools.")
    print(f"  Result:      Not found (index = {idx})")
    print(f"  Comparisons: {comps}  (must check ALL {n} elements)")
    print(f"  Theory:      n = {n}")

    # ── EXPERIMENT 3: Average comparisons across many searches ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 3: Average Comparisons – Successful vs Unsuccessful")
    print("─" * 70)
    print(f"\n  {'n':>8} | {'Avg (success)':>15} | {'Theory (n+1)/2':>16} | {'Unsuccessful':>14}")
    print(f"  {'─'*8}─|─{'─'*15}─|─{'─'*16}─|─{'─'*14}")

    for n in [10, 50, 100, 500, 1000]:
        arr = list(range(1, n + 1))
        total = sum(sequential_search(arr, x)[1] for x in arr)
        avg_succ = total / n
        theory = (n + 1) / 2
        _, unsucc_comps = sequential_search(arr, -1)
        print(f"  {n:>8} | {avg_succ:>15.1f} | {theory:>16.1f} | {unsucc_comps:>14}")

    # ── EXPERIMENT 4: Engineering boundary ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 4: Engineering Boundary Analysis")
    print("─" * 70)
    print("""
  ORIGINAL SYSTEM: n = 100 tools
  ─────────────────────────────────────────────────────────────
    Worst-case comparisons per query:  100
    Assumed search frequency:          50 queries/day
    Daily comparisons:                 50 × 100 = 5,000
    VERDICT: Sequential Search is APPROPRIATE ✓

  CHANGED CONDITION: n = 10,000 tools, 1,000 queries/day
  ─────────────────────────────────────────────────────────────
    Worst-case comparisons per query:  10,000
    Daily comparisons (sequential):    1,000 × 10,000 = 10,000,000
    Daily comparisons (binary search): 1,000 × 14 = 14,000
      (binary search needs log2(10,000) ≈ 14 comparisons)
    One-time sort cost:                10,000 × log2(10,000) ≈ 140,000

    Ratio: sequential / binary = 10,000,000 / 14,000 ≈ 714×
    VERDICT: Sequential Search NO LONGER APPROPRIATE ✗
    RECOMMENDATION: Pre-sort tools list once, then use Binary Search
    """)

    # ── EXPERIMENT 5: Decision boundary computation ──
    print("─" * 70)
    print("EXPERIMENT 5: Decision Boundary – At What n Should You Switch?")
    print("─" * 70)
    print(f"\n  {'n':>8} | {'Seq Daily Comps':>18} | {'BS Daily Comps':>16} | {'Ratio':>8} | {'Decision':>12}")
    print(f"  {'─'*8}─|─{'─'*18}─|─{'─'*16}─|─{'─'*8}─|─{'─'*12}")
    queries_per_day = 1000
    for n in [100, 500, 1000, 5000, 10000, 50000]:
        seq_daily = queries_per_day * n
        bs_per_q  = math.ceil(math.log2(n)) if n > 1 else 1
        bs_daily  = queries_per_day * bs_per_q
        ratio     = seq_daily / bs_daily
        decision  = "SEQUENTIAL" if n <= 500 else "BINARY SRCH"
        print(f"  {n:>8} | {seq_daily:>18,} | {bs_daily:>16,} | {ratio:>8.1f}x | {decision:>12}")

    print("""
  CONCLUSION:
    Sequential Search is a reasonable engineering choice when:
      • n is small (≤ 500 elements), AND
      • Search frequency is low (≤ 100 queries/day), AND
      • Data changes frequently (re-sorting cost is high)

    STOP recommending Sequential Search when:
      • n > 1,000 tools, OR
      • Search frequency > 100/day
      SWITCH TO: Sort once + Binary Search = O(n log n) + O(log n) per query
    """)


if __name__ == "__main__":
    random.seed(42)
    run_experiments()
