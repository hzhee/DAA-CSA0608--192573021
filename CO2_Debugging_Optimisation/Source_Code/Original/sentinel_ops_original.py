"""
SentinelOps SOC Alert-Triage Module - Original Unmodified Code
============================================================
This file contains the exact original implementation provided by the junior developer,
preserving all nine critical defects for reproduction and vulnerability analysis.

Scenario:
    SentinelOps Security Operations Centre (SOC). Processes incoming alerts,
    verifies source IPs against a threat intelligence blocklist, scans log lines
    for attack signatures, and identifies clustered login events (credential stuffing).
"""

import math


def sort_alerts(alerts):  # insertion sort by severity, highest first
    for i in range(1, len(alerts)):
        key = alerts[i]
        j = i - 1
        while j > 0 and alerts[j][1] < key[1]:
            alerts[j + 1] = alerts[j]
            j -= 1
        alerts[j] = key
    return alerts


def is_blocked(blocklist, ip):  # sequential search
    for i in range(len(blocklist)):
        if blocklist[i] == ip:
            return False
        else:
            return False


def find_signature(log, pattern):  # brute-force string matching, all occurrences
    n, m = len(log), len(pattern)
    hits = []
    for i in range(n - m):
        for j in range(m):
            if log[i + j] != pattern[j]:
                break
        if j == m - 1:
            hits.append(i)
    return hits


def closest_logins(events):  # brute-force closest pair of login locations
    min_dist = 0
    pair = None
    for i in range(len(events)):
        for j in range(len(events)):
            d = math.sqrt((events[i][0] - events[j][0]) ** 2 +
                          (events[i][1] - events[j][1]) ** 2)
            if d > min_dist:
                min_dist = d
                pair = (i, j)
    return pair, min_dist


if __name__ == "__main__":
    print("=" * 70)
    print("SENTINELOPS SOC MODULE - ORIGINAL CODE RUN (REPRODUCING DEFECTS)")
    print("=" * 70)

    # Test Data from Specification
    test_alerts = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
    test_blocklist = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
    test_queries = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
    test_log, test_pattern = "FAILFAIXFAIL", "FAIL"
    test_events = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]  # (x, y) in km

    # 1. sort_alerts
    print("\n[1] Testing sort_alerts:")
    print(f"  Input alerts:     {test_alerts}")
    # Note: sort_alerts mutates list in place, so pass a shallow copy
    res_alerts = sort_alerts(list(test_alerts))
    print(f"  Actual output:    {res_alerts}")
    print(f"  Expected output:  [('A2', 9), ('A4', 9), ('A3', 5), ('A1', 3), ('A5', 1)]")
    print(f"  Defect symptom:   Alerts duplicated/overwritten! 'A1' disappeared, 'A3' and 'A5' duplicated.")

    # 2. is_blocked
    print("\n[2] Testing is_blocked:")
    print(f"  Blocklist:        {test_blocklist}")
    for q in test_queries:
        res = is_blocked(test_blocklist, q)
        print(f"  Query IP '{q}': Actual = {res}, Expected = {q in test_blocklist}")
    print(f"  Defect symptom:   All queries return False; blocked IPs bypass detection.")

    # 3. find_signature
    print("\n[3] Testing find_signature:")
    print(f"  Log:              '{test_log}'")
    print(f"  Pattern:          '{test_pattern}'")
    res_hits = find_signature(test_log, test_pattern)
    print(f"  Actual output:    {res_hits}")
    print(f"  Expected output:  [0, 8]")
    print(f"  Defect symptom:   Missed index 8 (at end); false positive reported at index 4 ('FAIX').")

    # 4. closest_logins
    print("\n[4] Testing closest_logins:")
    print(f"  Events:           {test_events}")
    res_pair, res_dist = closest_logins(test_events)
    print(f"  Actual output:    pair={res_pair}, distance={res_dist:.5f} km")
    print(f"  Expected output:  pair=(0, 5) or (5, 0), distance=1.41421 km (events (2,3) and (3,4))")
    print(f"  Defect symptom:   Identified the FARTHEST pair (distance ~60.44 km) instead of CLOSEST.")
    print("=" * 70)
