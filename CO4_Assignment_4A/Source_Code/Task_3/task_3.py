#!/usr/bin/env python3
"""Task 3: bottom-up dynamic programming for 0/1 knapsack."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Item:
    item_id: str
    weight: int
    value: int


def knapsack(items: Iterable[Item], capacity: int):
    items = list(items)
    if capacity < 0 or any(item.weight <= 0 or item.value < 0 for item in items):
        raise ValueError("capacity must be non-negative; weights positive; values non-negative")

    n = len(items)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i, item in enumerate(items, start=1):
        for current_capacity in range(capacity + 1):
            exclude = dp[i - 1][current_capacity]
            include = -1
            if item.weight <= current_capacity:
                include = item.value + dp[i - 1][current_capacity - item.weight]
            dp[i][current_capacity] = max(exclude, include)

    selected = []
    decisions = []
    remaining = capacity
    for i in range(n, 0, -1):
        item = items[i - 1]
        if dp[i][remaining] > dp[i - 1][remaining]:
            selected.append(item)
            decisions.append((item.item_id, "include", remaining, remaining - item.weight))
            remaining -= item.weight
        else:
            decisions.append((item.item_id, "exclude", remaining, remaining))
    selected.reverse()
    decisions.reverse()
    return dp, selected, decisions


def main():
    items = [Item("P", 2, 12), Item("Q", 3, 20), Item("R", 4, 25), Item("S", 5, 30)]
    capacity = 7
    dp, chosen, decisions = knapsack(items, capacity)
    print("TASK 3 - 0/1 KNAPSACK")
    print("State: dp[i][w] is the maximum value from the first i items with capacity at most w.")
    print("w       :", " ".join(f"{w:>3}" for w in range(capacity + 1)))
    for i, row in enumerate(dp):
        label = "none" if i == 0 else items[i - 1].item_id
        print(f"first {label:>4}:", " ".join(f"{value:>3}" for value in row))
    print("\nReconstruction (from S back to P):")
    for item_id, decision, before, after in reversed(decisions):
        print(f"  {item_id}: {decision}; remaining capacity {before} -> {after}")
    print("Selected:", ", ".join(item.item_id for item in chosen))
    print("Total weight:", sum(item.weight for item in chosen))
    print("Optimal value:", dp[len(items)][capacity])
    assert dp[-1][capacity] == 45
    assert {item.item_id for item in chosen} == {"Q", "R"}
    assert knapsack(items, 0)[0][-1][0] == 0
    assert knapsack([Item("X", 8, 50)], 7)[0][-1][7] == 0
    print("Tests passed: supplied instance, zero capacity, overweight item.")


if __name__ == "__main__":
    main()
