#!/usr/bin/env python3
"""Task 1: diagnose vague fractional-knapsack pseudocode and execute a repair."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Item:
    item_id: str
    weight: float
    value: float

    @property
    def ratio(self) -> float:
        return self.value / self.weight


DEFICIENCIES = [
    "Inputs are unspecified: package records and vehicle capacity have no defined fields or types.",
    "Arrange packages gives no ordering rule, so different implementations may choose different packages.",
    "Select the best package does not define best; it must compare value per unit weight.",
    "Suitable package does not state the feasibility test against remaining capacity.",
    "The design does not say that a package may be split when only part of its weight fits.",
    "Remaining capacity is not updated after each choice, so the loop can overfill or fail to progress.",
    "The result construction and objective value are undefined, and the loop has no precise stop condition.",
]


def fractional_knapsack(items: Iterable[Item], capacity: float):
    """Return selected fractions, a decision trace, and the maximum value."""
    if capacity < 0:
        raise ValueError("capacity must be non-negative")
    items = list(items)
    if any(item.weight <= 0 or item.value < 0 for item in items):
        raise ValueError("weights must be positive and values non-negative")

    ordered = sorted(items, key=lambda item: (-item.ratio, item.item_id))
    remaining = float(capacity)
    total_value = 0.0
    selected = []
    trace = []
    for item in ordered:
        if remaining == 0:
            break
        taken_weight = min(item.weight, remaining)
        fraction = taken_weight / item.weight
        value_gained = fraction * item.value
        selected.append((item.item_id, fraction, taken_weight, value_gained))
        trace.append((item, fraction, taken_weight, value_gained, remaining - taken_weight))
        total_value += value_gained
        remaining -= taken_weight
    return ordered, selected, trace, total_value


def main():
    print("TASK 1 - ALGORITHM DESIGN REVIEW")
    print("Deficiencies in the proposed pseudocode:")
    for number, deficiency in enumerate(DEFICIENCIES, start=1):
        print(f"  {number}. {deficiency}")

    items = [Item("A", 10, 60), Item("B", 20, 100), Item("C", 30, 120)]
    capacity = 50
    ordered, selected, trace, total = fractional_knapsack(items, capacity)
    print("\nGreedy rule: process packages by decreasing value/weight ratio.")
    print("Input: A(10,60), B(20,100), C(30,120); capacity=50")
    print("Order:", " -> ".join(f"{item.item_id}({item.ratio:.2f})" for item in ordered))
    print("Item | fraction | weight taken | value gained | remaining capacity")
    remaining = float(capacity)
    for item, fraction, taken_weight, value_gained, after in trace:
        print(f"{item.item_id:>4} | {fraction:8.2f} | {taken_weight:12.2f} | {value_gained:12.2f} | {after:18.2f}")
        remaining = after
    print("Selected:", ", ".join(f"{item_id}:{fraction:.2f}" for item_id, fraction, _, _ in selected))
    print(f"Maximum value: {total:.2f}; capacity used: {capacity - remaining:.2f}/{capacity}")

    assert len(DEFICIENCIES) >= 5
    assert total == 240.0
    assert fractional_knapsack(items, 0)[3] == 0
    assert fractional_knapsack([Item("X", 8, 16)], 4)[3] == 8
    assert fractional_knapsack([], 10)[3] == 0
    print("Tests passed: supplied design, zero capacity, fractional final item, empty input.")


if __name__ == "__main__":
    main()
