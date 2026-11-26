#!/usr/bin/env python3
"""Task 2: compare ratio-greedy fractional and 0/1 knapsack."""

from dataclasses import dataclass
from time import perf_counter_ns
from typing import Iterable


@dataclass(frozen=True)
class Item:
    item_id: str
    weight: int
    value: int

    @property
    def ratio(self):
        return self.value / self.weight


def fractional_knapsack(items: Iterable[Item], capacity: int):
    items = list(items)
    if capacity < 0 or any(item.weight <= 0 or item.value < 0 for item in items):
        raise ValueError("capacity must be non-negative; weights positive; values non-negative")
    ordered = sorted(items, key=lambda item: (-item.ratio, item.item_id))
    remaining = capacity
    selected = []
    decisions = []
    total = 0.0
    for item in ordered:
        ratio = item.ratio
        if remaining == 0:
            decisions.append((item.item_id, ratio, 0.0, 0.0, remaining, "stop"))
            continue
        amount = min(item.weight, remaining)
        fraction = amount / item.weight
        gained = fraction * item.value
        selected.append((item.item_id, fraction, amount, gained))
        remaining -= amount
        total += gained
        decisions.append((item.item_id, ratio, fraction, gained, remaining, "take"))
    return total, selected, decisions, len(items), len(ordered)


def ratio_greedy_01(items: Iterable[Item], capacity: int):
    items = list(items)
    if capacity < 0 or any(item.weight <= 0 or item.value < 0 for item in items):
        raise ValueError("capacity must be non-negative; weights positive; values non-negative")
    ordered = sorted(items, key=lambda item: (-item.ratio, item.item_id))
    remaining = capacity
    selected = []
    trace = []
    total = 0
    for item in ordered:
        take = item.weight <= remaining
        before = remaining
        if take:
            selected.append(item)
            remaining -= item.weight
            total += item.value
        trace.append((item, before, "take" if take else "skip", remaining, total))
    return total, selected, trace, len(ordered)


def zero_one_knapsack(items: Iterable[Item], capacity: int):
    items = list(items)
    if capacity < 0 or any(item.weight <= 0 or item.value < 0 for item in items):
        raise ValueError("capacity must be non-negative; weights positive; values non-negative")
    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, item in enumerate(items, start=1):
        for current_capacity in range(capacity + 1):
            dp[i][current_capacity] = dp[i - 1][current_capacity]
            if item.weight <= current_capacity:
                dp[i][current_capacity] = max(
                    dp[i][current_capacity],
                    item.value + dp[i - 1][current_capacity - item.weight],
                )
    selected = []
    remaining = capacity
    decisions = []
    for i in range(n, 0, -1):
        item = items[i - 1]
        take = dp[i][remaining] > dp[i - 1][remaining]
        before = remaining
        if take:
            selected.append(item)
            remaining -= item.weight
        decisions.append((item.item_id, "take" if take else "skip", before, remaining, dp[i][before]))
    selected.reverse()
    return dp[n][capacity], selected, dp, decisions, n * (capacity + 1)


def describe(items, capacity):
    return ", ".join(f"{x.item_id}(w={x.weight},v={x.value},r={x.ratio:.2f})" for x in items) + f"; capacity={capacity}"


def run_comparison(label, items, capacity):
    print(f"\n{label}")
    print("INPUT:", describe(items, capacity))
    start = perf_counter_ns()
    f_value, f_selected, f_trace, ratio_evals, visits = fractional_knapsack(items, capacity)
    fractional_ns = perf_counter_ns() - start
    print("Fractional greedy, sorted by decreasing value/weight:")
    print("ID | ratio | fraction | value gained | capacity left | decision")
    for item_id, ratio, fraction, gained, left, decision in f_trace:
        print(f"{item_id:>2} | {ratio:>5.2f} | {fraction:>8.3f} | {gained:>12.2f} | {left:>13} | {decision}")
    print("Selected fractions:", [(x[0], round(x[1], 3)) for x in f_selected], "value=", round(f_value, 2))

    g_value, g_selected, g_trace, g_work = ratio_greedy_01(items, capacity)
    print("Ratio-greedy 0/1 decisions:")
    for item, before, action, after, running in g_trace:
        print(f"{item.item_id}: {action}; remaining {before}->{after}; running value={running}")
    print("0/1 greedy selection:", [x.item_id for x in g_selected], "value=", g_value)

    start = perf_counter_ns()
    dp_value, dp_selected, table, backtrace, cells = zero_one_knapsack(items, capacity)
    dp_ns = perf_counter_ns() - start
    print("0/1 DP state: DP[i,w] = best value using first i items within capacity w.")
    print("i | item prefix | values for capacities 0..W")
    for i, row in enumerate(table):
        prefix = "none" if i == 0 else items[i - 1].item_id
        print(f"{i:>1} | {prefix:>11} | {row}")
    print("DP reconstruction (last item backwards):")
    for item_id, action, before, after, best in backtrace:
        print(f"{item_id}: {action}; remaining capacity {before}->{after}; prefix optimum={best}")
    print("0/1 DP selection:", [x.item_id for x in dp_selected], "value=", dp_value)
    print("ENGINEERING EVIDENCE")
    print(f"Work counters: fractional ratio evaluations={ratio_evals}, fractional item visits={visits}, 0/1 greedy decisions={g_work}, DP transitions={cells}.")
    print(f"State storage: fractional/greedy O(n) item records; DP stores {(len(items)+1)*(capacity+1)} integer cells = O(nW).")
    print(f"Observed elapsed time (informational only): fractional={fractional_ns/1000:.1f} us; DP={dp_ns/1000:.1f} us.")
    return f_value, g_value, dp_value, f_selected, g_selected, dp_selected, cells


def main():
    normal = [Item("A", 10, 60), Item("B", 20, 100), Item("C", 30, 120)]
    print("TASK 2 - GREEDY VS DYNAMIC PROGRAMMING")
    print("Normal fractional case: descending ratios are optimal because a final item may be split.")
    normal_result = run_comparison("NORMAL CASE", normal, 50)

    adversarial = [Item("G", 6, 99), Item("X", 5, 50), Item("Y", 5, 50)]
    print("\nSTUDENT-DESIGNED 0/1 COUNTEREXAMPLE")
    print("Prediction before execution: ratio greedy commits to G (ratio 16.50, value 99); that leaves capacity 4 and prevents the compatible pair X+Y (value 100).")
    bad_result = run_comparison("BREAK THE 0/1 GREEDY INTUITION", adversarial, 10)
    gap = (bad_result[2] - bad_result[1]) / bad_result[2] * 100
    print(f"First blocking commitment: G; greedy value {bad_result[1]} vs DP optimum {bad_result[2]} (gap {gap:.1f}%).")

    print("\nCHANGED REQUIREMENT: EXTREMELY FAST, NEAR-OPTIMAL ACCEPTABLE")
    print(f"On the student case, ratio greedy makes {len(adversarial)} decisions and returns {bad_result[1]}/{bad_result[2]} ({100-gap:.1f}% of optimum), while DP evaluates {bad_result[6]} transitions.")
    print("Decision: use ratio greedy only when a 1% loss is acceptable for this measured case; it has no quality guarantee and the normal 50-capacity 0/1 run shows a larger failure (160 vs 220).")

    assert round(normal_result[0]) == 240
    assert normal_result[1] == 160 and normal_result[2] == 220
    assert bad_result[1] == 99 and bad_result[2] == 100 and gap == 1.0
    assert zero_one_knapsack([], 0)[0] == 0
    assert zero_one_knapsack([Item("Z", 11, 20)], 10)[0] == 0
    assert fractional_knapsack([], 10)[0] == 0
    for bad_items, bad_capacity in (([], -1), ([Item("bad", 0, 5)], 10), ([Item("bad", 2, -1)], 10)):
        try:
            zero_one_knapsack(bad_items, bad_capacity)
        except ValueError:
            pass
        else:
            raise AssertionError("invalid capacity, weight, or value must be rejected")
    print("Boundary tests: negative capacity, zero weight, and negative value rejected.")
    print("Tests passed: fractional optimum, 0/1 optimum, greedy counterexample, empty input, overweight item, invalid data.")


if __name__ == "__main__":
    main()
