"""
SentinelOps SOC Alert-Triage Module - Fully Corrected Implementation
===================================================================
This module fixes all nine defects from the original junior developer's code
without altering the core algorithmic structure (Insertion Sort, Sequential Search,
Brute-force String Matching, Brute-force Closest Pair).

Every change documents what was wrong, why it was wrong, and how it was fixed and verified.
"""

import math
from typing import List, Tuple, Optional, Any


def sort_alerts(alerts: List[Tuple[str, int]]) -> List[Tuple[str, int]]:
    """
    Sort alerts by severity in descending order (highest severity first) using Insertion Sort.
    Maintains stability: alerts with equal severity remain in their original arrival order.

    Defects Fixed:
        - Defect 1 (Line 8): Changed `while j > 0` to `while j >= 0`.
          Root Cause: Condition terminated before comparing against index 0, preventing
          elements from shifting past or being inserted at the very beginning of the list.
        - Defect 2 (Line 11): Changed `alerts[j] = key` to `alerts[j + 1] = key`.
          Root Cause: Decrementing `j` in the while loop left `j` pointing one position to
          the left of the open slot. Assigning to `alerts[j]` directly overwrote preceding
          items and left a duplicate copy at `alerts[j + 1]`.

    Stability:
        Using strict inequality `alerts[j][1] < key[1]` guarantees that when severities are equal,
        the while loop terminates without shifting, preserving original arrival order.
    """
    alerts = list(alerts)  # Create shallow copy to prevent unintended side effects
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        # Fix for Defect 1: j >= 0 ensures index 0 is compared and can receive shifts
        while j >= 0 and alerts[j][1] < key[1]:
            alerts[j + 1] = alerts[j]
            j -= 1
        # Fix for Defect 2: alerts[j + 1] places key into the vacancy created by the shifts
        alerts[j + 1] = key
    return alerts


def is_blocked(blocklist: List[str], ip: str) -> bool:
    """
    Sequential search to determine whether a target IP address exists in the blocklist.

    Defects Fixed:
        - Defect 3 (Line 18): Changed `return False` on match to `return True`.
          Root Cause: Inverted boolean logic caused blocked IPs to be treated as clean.
        - Defect 4 (Line 19-20): Removed premature `else: return False` inside the loop.
          Root Cause: Returning False on the first non-matching element aborted the search
          prematurely on iteration 0 for any IP not located at index 0.

    Boundary Behavior:
        An empty blocklist will immediately bypass the loop and return False correctly.
    """
    for i in range(len(blocklist)):
        if blocklist[i] == ip:
            return True  # Fix for Defect 3: True when target IP matches a blocklist entry
    return False  # Fix for Defect 4: False returned only after verifying entire blocklist


def find_signature(log: str, pattern: str) -> List[int]:
    """
    Brute-force string matching algorithm to find all starting indices of `pattern` in `log`.

    Defects Fixed:
        - Defect 5 (Line 27): Changed `range(n - m)` to `range(n - m + 1)`.
          Root Cause: In Python, `range(stop)` is non-inclusive. Stopping at `n - m` omitted
          the final valid alignment window `n - m`, missing patterns situated at the log's end.
        - Defect 6 & 7 (Line 31-33): Replaced unindented `if j == m - 1` with Python's `for...else`.
          Root Cause: When the inner loop mismatched on the last character of pattern (`j == m - 1`),
          it broke out with `j` still set to `m - 1`. The outer `if j == m - 1` falsely evaluated
          to True, recording false-positive detections. Using `for...else` guarantees `hits.append(i)`
          executes IF AND ONLY IF the inner loop finishes all iterations without breaking.

    Boundary Behavior:
        - If pattern is longer than log (m > n), returns [].
        - If pattern is empty (m == 0), returns [].
    """
    n, m = len(log), len(pattern)
    hits = []
    if m == 0 or n < m:
        return hits

    # Fix for Defect 5: range(n - m + 1) covers all possible alignments [0 .. n - m]
    for i in range(n - m + 1):
        for j in range(m):
            if log[i + j] != pattern[j]:
                break
        else:
            # Fix for Defects 6 & 7: for...else triggers only on clean completion (full match)
            hits.append(i)
    return hits


def closest_logins(events: List[Tuple[float, float]]) -> Tuple[Optional[Tuple[int, int]], float]:
    """
    Brute-force closest pair of 2D login coordinates (x, y) in kilometres.

    Defects Fixed:
        - Defect 8 (Line 38): Initialized `min_dist = float('inf')` instead of `0`.
          Root Cause: Starting at 0 prevented finding any pair since Euclidean distance >= 0.
        - Defect 9a (Line 44): Changed `if d > min_dist` to `if d < min_dist`.
          Root Cause: The `>` operator searched for the farthest pair (maximum distance) rather
          than the closest pair.
        - Defect 9b (Line 41): Changed inner loop range to `range(i + 1, len(events))`.
          Root Cause: Running `j` over all events evaluated self-pairs `(i, i)` with distance 0
          and duplicated symmetric comparisons `(i, j)` and `(j, i)`.

    Boundary Behavior:
        - If len(events) < 2, no valid pair exists; returns (None, float('inf')).
    """
    if len(events) < 2:
        return None, float('inf')

    min_dist = float('inf')  # Fix for Defect 8: Infinity allows smaller distances to be accepted
    pair: Optional[Tuple[int, int]] = None
    n = len(events)

    for i in range(n):
        # Fix for Defect 9b: i + 1 avoids self-comparison and symmetric duplicates
        for j in range(i + 1, n):
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 +
                          (events[i][1] - events[j][1]) ** 2)
            # Fix for Defect 9a: Strict inequality finds minimum distance
            if d < min_dist:
                min_dist = d
                pair = (i, j)

    return pair, min_dist


if __name__ == "__main__":
    print("=" * 70)
    print("SENTINELOPS SOC MODULE - CORRECTED CODE EXECUTION & VERIFICATION")
    print("=" * 70)

    # Specification Test Data
    test_alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    test_blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    test_queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    test_log, test_pattern = "FAILFAIXFAIL", "FAIL"
    test_events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]

    # 1. Verification of sort_alerts
    print("\n[1] Verified sort_alerts:")
    res_alerts = sort_alerts(test_alerts)
    print(f"  Result: {res_alerts}")
    assert res_alerts == [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)], "sort_alerts failed!"
    print("  ✓ PASS: Correctly sorted in descending order while preserving stability (A2 before A4).")

    # 2. Verification of is_blocked
    print("\n[2] Verified is_blocked:")
    for q in test_queries:
        res = is_blocked(test_blocklist, q)
        expected = q in test_blocklist
        print(f"  IP: {q:<12} -> Blocked: {res} (Expected: {expected})")
        assert res == expected, f"is_blocked failed for {q}!"
    print("  ✓ PASS: All queries match expected threat intelligence lookup.")

    # 3. Verification of find_signature
    print("\n[3] Verified find_signature:")
    res_hits = find_signature(test_log, test_pattern)
    print(f"  Log: '{test_log}', Pattern: '{test_pattern}' -> Hits: {res_hits}")
    assert res_hits == [0, 8], "find_signature failed!"
    print("  ✓ PASS: Accurately detected matches at [0, 8], rejected 'FAIX' at index 4.")

    # 4. Verification of closest_logins
    print("\n[4] Verified closest_logins:")
    res_pair, res_dist = closest_logins(test_events)
    print(f"  Closest Pair: indices {res_pair} ({test_events[res_pair[0]]} and {test_events[res_pair[1]]})")
    print(f"  Distance: {res_dist:.5f} km")
    assert res_pair == (0, 5) or res_pair == (5, 0), "closest_logins pair failed!"
    assert math.isclose(res_dist, math.sqrt(2)), "closest_logins distance failed!"
    print("  ✓ PASS: Accurately identified closest pair (2,3)-(3,4) with distance sqrt(2) ~ 1.414 km.")

    print("\n" + "=" * 70)
    print("ALL CORRECTED FUNCTIONS PASSED SPECIFICATION BENCHMARK VERIFICATION!")
    print("=" * 70)
