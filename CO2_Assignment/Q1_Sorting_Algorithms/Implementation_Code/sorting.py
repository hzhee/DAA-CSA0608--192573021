"""
Q1 – Sorting Under Different Data Conditions
Selection Sort | Bubble Sort | Insertion Sort
Student: HRUZHEECAYSHAN T K | Reg No: 192573021
CO2 Assignment – Design and Analysis of Algorithms
"""

import random
import time

# ─────────────────────────────────────────────
# SORTING ALGORITHMS WITH COMPARISON COUNTING
# ─────────────────────────────────────────────

def selection_sort(arr):
    """Selection Sort with comparison counting."""
    A = arr[:]
    n = len(A)
    comparisons = 0
    swaps = 0
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if A[j] < A[min_idx]:
                min_idx = j
        if min_idx != i:
            A[i], A[min_idx] = A[min_idx], A[i]
            swaps += 1
    return A, comparisons, swaps


def bubble_sort(arr):
    """Bubble Sort with early termination and comparison counting."""
    A = arr[:]
    n = len(A)
    comparisons = 0
    swaps = 0
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if A[j] > A[j + 1]:
                A[j], A[j + 1] = A[j + 1], A[j]
                swaps += 1
                swapped = True
        if not swapped:
            break
    return A, comparisons, swaps


def insertion_sort(arr):
    """Insertion Sort with comparison counting."""
    A = arr[:]
    n = len(A)
    comparisons = 0
    swaps = 0
    for i in range(1, n):
        key = A[i]
        j = i - 1
        while j >= 0 and A[j] > key:
            comparisons += 1
            A[j + 1] = A[j]
            swaps += 1
            j -= 1
        if j >= 0:
            comparisons += 1  # The failing comparison
        A[j + 1] = key
    return A, comparisons, swaps


# ─────────────────────────────────────────────
# TEST DATA GENERATORS
# ─────────────────────────────────────────────

def generate_random(n):
    return random.sample(range(1, 10 * n), n)

def generate_sorted(n):
    return list(range(1, n + 1))

def generate_reverse_sorted(n):
    return list(range(n, 0, -1))

def generate_nearly_sorted(n):
    arr = list(range(1, n + 1))
    swaps = max(1, n // 10)
    for _ in range(swaps):
        i, j = random.randint(0, n - 1), random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


# ─────────────────────────────────────────────
# EXPERIMENT RUNNER
# ─────────────────────────────────────────────

def run_experiment(sizes, trials=3):
    """Run all sorting algorithms under all data conditions."""
    algorithms = {
        "Selection Sort": selection_sort,
        "Bubble Sort": bubble_sort,
        "Insertion Sort": insertion_sort,
    }
    conditions = {
        "Random": generate_random,
        "Sorted": generate_sorted,
        "Reverse Sorted": generate_reverse_sorted,
        "Nearly Sorted": generate_nearly_sorted,
    }

    results = {}
    for algo_name, algo in algorithms.items():
        results[algo_name] = {}
        for cond_name, generator in conditions.items():
            results[algo_name][cond_name] = {}
            for n in sizes:
                total_comps = 0
                total_time = 0.0
                for _ in range(trials):
                    arr = generator(n)
                    start = time.perf_counter()
                    _, comps, _ = algo(arr)
                    elapsed = time.perf_counter() - start
                    total_comps += comps
                    total_time += elapsed
                avg_comps = total_comps // trials
                avg_time = total_time / trials
                results[algo_name][cond_name][n] = (avg_comps, avg_time)
    return results


def print_results(results, sizes):
    """Display results in a formatted table."""
    algorithms = list(results.keys())
    conditions = list(results[algorithms[0]].keys())

    print("\n" + "=" * 100)
    print("Q1 – SORTING ALGORITHMS: COMPARISON COUNT ANALYSIS")
    print("Student: HRUZHEECAYSHAN T K | Reg No: 192573021")
    print("=" * 100)

    for cond in conditions:
        print(f"\n{'─' * 100}")
        print(f"  DATA CONDITION: {cond}")
        print(f"{'─' * 100}")
        header = f"  {'n':>8} | " + " | ".join(f"{a:>22}" for a in algorithms)
        print(header)
        print(f"  {'─' * 8}─|─" + "─|─".join("─" * 22 for _ in algorithms))
        for n in sizes:
            row_parts = []
            for algo in algorithms:
                comps, t = results[algo][cond][n]
                row_parts.append(f"{comps:>14,} ({t*1000:5.2f}ms)")
            print(f"  {n:>8} | " + " | ".join(row_parts))

    # Theoretical comparison
    print("\n" + "=" * 100)
    print("  THEORETICAL vs ACTUAL COMPARISON COUNT (n=1000, Worst/Random Case)")
    print("=" * 100)
    n = 1000
    theoretical_sel = n * (n - 1) // 2
    print(f"  Selection Sort theoretical: n(n-1)/2 = {theoretical_sel:,}")
    if 1000 in sizes:
        actual_sel = results["Selection Sort"]["Random"][1000][0]
        print(f"  Selection Sort actual (random, n=1000): {actual_sel:,}")
        print(f"  Match: {'✓ EXACT' if actual_sel == theoretical_sel else f'close – ratio {actual_sel/theoretical_sel:.4f}'}")

    print(f"\n  Bubble Sort worst case theoretical: n(n-1)/2 = {theoretical_sel:,}")
    if 1000 in sizes:
        actual_bub = results["Bubble Sort"]["Reverse Sorted"][1000][0]
        print(f"  Bubble Sort actual (reverse, n=1000): {actual_bub:,}")

    print(f"\n  Insertion Sort worst case theoretical: n(n-1)/2 = {theoretical_sel:,}")
    if 1000 in sizes:
        actual_ins = results["Insertion Sort"]["Reverse Sorted"][1000][0]
        print(f"  Insertion Sort actual (reverse, n=1000): {actual_ins:,}")


def print_recommendation():
    print("\n" + "=" * 100)
    print("  ENGINEERING RECOMMENDATION")
    print("=" * 100)
    print("""
  Context: Emergency dispatch priority score sorting system.

  ANALYSIS:
  ┌─────────────────┬────────────────┬──────────────────────────────────────────────────┐
  │ Algorithm       │ Best Scenario  │ Recommendation                                   │
  ├─────────────────┼────────────────┼──────────────────────────────────────────────────┤
  │ Selection Sort  │ Fixed O(n²)    │ AVOID – no benefit from partially sorted data    │
  │ Bubble Sort     │ Already sorted │ ACCEPTABLE only for near-sorted, tiny datasets   │
  │ Insertion Sort  │ Nearly sorted  │ BEST CHOICE for emergency dispatch system        │
  └─────────────────┴────────────────┴──────────────────────────────────────────────────┘

  RECOMMENDATION: Use INSERTION SORT for the emergency dispatch system.
  Reasoning:
  1. Emergency data is frequently NEARLY SORTED (recent events, priority updates)
  2. Insertion Sort achieves O(n) for sorted/nearly-sorted → minimal overhead
  3. Insertion Sort is STABLE – preserves original order for equal-priority items
  4. Insertion Sort is ADAPTIVE – performance scales with actual disorder level
  5. For large-scale systems (n > 10,000), migrate to merge sort or timsort (O(n log n))
    """)


def print_complexity_analysis():
    print("\n" + "=" * 100)
    print("  MATHEMATICAL COMPLEXITY DERIVATION")
    print("=" * 100)
    print("""
  Selection Sort:
    Comparison count = Σ(i=0 to n-2) (n-1-i)
                     = (n-1) + (n-2) + ... + 1
                     = n(n-1)/2
    → T(n) = n(n-1)/2 ∈ Θ(n²) for ALL input cases

  Bubble Sort:
    Worst case (reverse sorted):
      Comparison count = Σ(i=0 to n-2) (n-1-i) = n(n-1)/2 ∈ Θ(n²)
    Best case (already sorted):
      With early termination: n-1 comparisons ∈ Θ(n)
    Average case: n(n-1)/4 ∈ Θ(n²)

  Insertion Sort:
    Worst case (reverse sorted):
      Comparison count = Σ(i=1 to n-1) i = n(n-1)/2 ∈ Θ(n²)
    Best case (already sorted):
      1 comparison per element: n-1 ∈ Θ(n)
    Average case: n(n-1)/4 ∈ Θ(n²)

  KEY INSIGHT: All three are Θ(n²) on average, but Insertion Sort and Bubble Sort
  degrade gracefully toward O(n) as input becomes more ordered.
    """)


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────

if __name__ == "__main__":
    random.seed(42)

    # Small demo
    print("\n" + "=" * 60)
    print("  DEMO RUN – Small Dataset (n=10)")
    print("=" * 60)
    demo = [64, 34, 25, 12, 22, 11, 90, 45, 67, 3]
    print(f"  Input:    {demo}")

    sorted_sel, c_sel, s_sel = selection_sort(demo)
    print(f"\n  Selection Sort Result: {sorted_sel}")
    print(f"    Comparisons: {c_sel},  Swaps: {s_sel}")

    sorted_bub, c_bub, s_bub = bubble_sort(demo)
    print(f"\n  Bubble Sort Result:    {sorted_bub}")
    print(f"    Comparisons: {c_bub},  Swaps: {s_bub}")

    sorted_ins, c_ins, s_ins = insertion_sort(demo)
    print(f"\n  Insertion Sort Result: {sorted_ins}")
    print(f"    Comparisons: {c_ins},  Swaps: {s_ins}")

    # Full experiment
    sizes = [100, 500, 1000, 2000]
    results = run_experiment(sizes)
    print_results(results, sizes)
    print_complexity_analysis()
    print_recommendation()

    print("\n" + "=" * 100)
    print("  PERFORMANCE COMPARISON TABLE (n=1000)")
    print("=" * 100)
    n = 1000
    print(f"\n  {'Algorithm':<20} {'Random':>15} {'Sorted':>15} {'Reverse':>15} {'Nearly Sorted':>15}")
    print(f"  {'─' * 20} {'─' * 15} {'─' * 15} {'─' * 15} {'─' * 15}")
    for algo in ["Selection Sort", "Bubble Sort", "Insertion Sort"]:
        row = f"  {algo:<20}"
        for cond in ["Random", "Sorted", "Reverse Sorted", "Nearly Sorted"]:
            comps, _ = results[algo][cond][1000]
            row += f" {comps:>15,}"
        print(row)

    print("""
  OBSERVATIONS:
  1. Selection Sort: Exactly 499,500 comparisons for ALL conditions (truly O(n²))
  2. Bubble Sort: 999 comparisons when already sorted (O(n)), ~499,500 when reversed
  3. Insertion Sort: n-1=999 comparisons when sorted, ~499,500 when reversed
  4. For nearly sorted: Insertion Sort makes far fewer comparisons → best adaptive choice
    """)
