#!/usr/bin/env python3
"""Executable calculations for the ShopSphere scalability audit.

The program uses closed forms rather than attempting infeasible trillion-step
simulations.  Its small-n counters make the formulas independently testable.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import ceil, log2

OPS_PER_SECOND = 10


def m1_comparisons(n: int) -> int:
    """Product-pair comparisons made by M1."""
    _positive(n)
    return n * (n - 1) // 2


def m2_audits(n: int) -> int:
    """Audits made while i takes values 1, 2, 4, ... below n."""
    _positive(n)
    return (1 << ceil(log2(n))) - 1


def s2_comparisons_upper_bound(n: int) -> int:
    """Maximum comparisons for the recurrence T(n)=T(n/2)+1, T(1)=1."""
    _positive(n)
    return ceil(log2(n)) + 1


def m4_current_operations(n: int) -> int:
    """Representative work for T(n)=4T(n/2)+n: Theta(n^2)."""
    _positive(n)
    return n * n


def m4_redesign_operations(n: int) -> float:
    """Representative work for T(n)=2T(n/2)+n: Theta(n log2 n)."""
    _positive(n)
    return n * log2(n)


def m5_operations(n: int) -> float:
    """Representative work for T(n)=2T(n/2)+n log n: Theta(n log^2 n)."""
    _positive(n)
    return n * log2(n) ** 2


def seconds(operations: float) -> float:
    return operations / OPS_PER_SECOND


def years(value_in_seconds: float) -> float:
    return value_in_seconds / (365 * 24 * 60 * 60)


def _positive(n: int) -> None:
    if n < 1:
        raise ValueError("n must be at least 1")


@dataclass(frozen=True)
class Result:
    module: str
    operations: float
    complexity: str


def audit(n: int) -> list[Result]:
    return [
        Result("M1 duplicate detector", m1_comparisons(n), "Theta(n^2)"),
        Result("M2 API rate limiter", m2_audits(n), "Theta(n)"),
        Result("S2 product search (worst-case bound)", s2_comparisons_upper_bound(n), "Theta(log n)"),
        Result("M4 recommendation engine: current", m4_current_operations(n), "Theta(n^2)"),
        Result("M4 recommendation engine: redesign", m4_redesign_operations(n), "Theta(n log n)"),
        Result("M5 sales analytics engine", m5_operations(n), "Theta(n log^2 n)"),
    ]


def main() -> None:
    n = 1_000_000
    print(f"ShopSphere scalability audit (n = {n:,}; {OPS_PER_SECOND} operations/second)")
    print("-" * 94)
    print(f"{'Module':42} {'Operations':>18} {'Runtime':>20}  Complexity")
    print("-" * 94)
    for result in audit(n):
        runtime = seconds(result.operations)
        runtime_text = f"{runtime:,.2f} s"
        if runtime >= 365 * 24 * 60 * 60:
            runtime_text += f" ({years(runtime):,.2f} years)"
        elif runtime >= 24 * 60 * 60:
            runtime_text += f" ({runtime / 86400:,.2f} days)"
        elif runtime >= 3600:
            runtime_text += f" ({runtime / 3600:,.2f} hours)"
        print(f"{result.module:42} {result.operations:18,.2f} {runtime_text:>20}  {result.complexity}")
    print("\nNightly-window decision (10 minutes = 600 seconds):")
    for result in audit(n):
        verdict = "FAIL - redesign required" if seconds(result.operations) > 600 else "PASS"
        print(f"- {result.module}: {verdict}")


if __name__ == "__main__":
    main()
