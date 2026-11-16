"""
SentinelOps SOC Alert-Triage Module - Test Datasets & Benchmark Generators
========================================================================
Provides standard specification test data, edge/boundary cases, and synthetic
generators for performance benchmarking (1,000 to 8,000+ events).
"""

import random
from typing import List, Tuple, Dict, Any, Optional

# =====================================================================
# 1. SPECIFICATION TEST DATASETS (FROM ASSIGNMENT PDF)
# =====================================================================

SPEC_ALERTS = [("A1", 3), ("A2", 9), ("A3", 5), ("A4", 9), ("A5", 1)]
SPEC_BLOCKLIST = ["10.0.0.5", "10.0.0.9", "172.16.4.2"]
SPEC_QUERIES = ["10.0.0.9", "10.0.0.5", "8.8.8.8"]
SPEC_LOG = "FAILFAIXFAIL"
SPEC_PATTERN = "FAIL"
SPEC_EVENTS = [(2, 3), (12, 30), (40, 50), (5, 1), (12, 10), (3, 4)]  # (x, y) in km

# Expected Ground Truth Outputs for Spec Data
EXPECTED_SORT_ALERTS = [("A2", 9), ("A4", 9), ("A3", 5), ("A1", 3), ("A5", 1)]
EXPECTED_IS_BLOCKED = {"10.0.0.9": True, "10.0.0.5": True, "8.8.8.8": False}
EXPECTED_FIND_SIGNATURE = [0, 8]
EXPECTED_CLOSEST_PAIR_INDICES = (0, 5)  # (2, 3) and (3, 4)
EXPECTED_CLOSEST_PAIR_DISTANCE = 1.4142135623730951  # sqrt(2)


# =====================================================================
# 2. BOUNDARY AND EDGE TEST CASES
# =====================================================================

BOUNDARY_CASES = {
    "sort_alerts": {
        "empty": [],
        "single_element": [("A1", 10)],
        "already_sorted": [("A1", 9), ("A2", 8), ("A3", 7), ("A4", 6)],
        "reverse_sorted": [("A1", 1), ("A2", 2), ("A3", 3), ("A4", 4)],
        "all_equal_severities": [("A1", 5), ("A2", 5), ("A3", 5), ("A4", 5)],
        "negative_severities": [("A1", -2), ("A2", 4), ("A3", 0), ("A4", -5)],
    },
    "is_blocked": {
        "empty_blocklist": ([], "192.168.1.1"),
        "single_match": (["192.168.1.1"], "192.168.1.1"),
        "single_mismatch": (["192.168.1.1"], "10.0.0.1"),
        "match_at_head": (["10.0.0.1", "10.0.0.2", "10.0.0.3"], "10.0.0.1"),
        "match_at_tail": (["10.0.0.1", "10.0.0.2", "10.0.0.3"], "10.0.0.3"),
    },
    "find_signature": {
        "pattern_at_end": ("SERVER_STATUS_FAIL", "FAIL"),
        "pattern_longer_than_log": ("ERR", "CRITICAL_ERROR_PAYLOAD"),
        "pattern_equals_log": ("EXPLOIT", "EXPLOIT"),
        "pattern_not_found": ("SAFE_TRANSACTION_PAYLOAD", "MALWARE"),
        "pattern_len_1": ("ALERT_B_EVENT", "B"),
        "repetitive_worst_case": ("A" * 1000 + "B", "A" * 50 + "B"),
        "empty_pattern": ("LOG_LINE", ""),
        "empty_log": ("", "FAIL"),
    },
    "closest_logins": {
        "empty_events": [],
        "single_event": [(15.0, 25.0)],
        "two_events": [(0.0, 0.0), (3.0, 4.0)],
        "collocated_events": [(10.0, 10.0), (20.0, 20.0), (10.0, 10.0)],
        "collinear_horizontal": [(1.0, 5.0), (3.0, 5.0), (7.0, 5.0), (12.0, 5.0)],
        "negative_coordinates": [(-10.0, -20.0), (-9.0, -18.0), (50.0, 50.0)],
    }
}


# =====================================================================
# 3. SYNTHETIC BENCHMARK DATASET GENERATORS
# =====================================================================

def generate_random_alerts(n: int, seed: int = 42) -> List[Tuple[str, int]]:
    """Generate n alerts with uniformly random severity scores between 1 and 10."""
    rng = random.Random(seed)
    return [(f"ALT_{i:06d}", rng.randint(1, 10)) for i in range(n)]


def generate_nearly_sorted_alerts(n: int, swap_count: Optional[int] = None, seed: int = 42) -> List[Tuple[str, int]]:
    """
    Generate n alerts sorted descending by severity, with a small number of random swaps (perturbations).
    Represents realistic production streams where alerts arrive nearly ordered.
    """
    rng = random.Random(seed)
    # Start with perfectly sorted descending list
    severities = sorted([rng.randint(1, 100) for _ in range(n)], reverse=True)
    alerts = [(f"ALT_{i:06d}", severities[i]) for i in range(n)]

    if swap_count is None:
        swap_count = max(1, int(0.02 * n))  # 2% perturbed elements

    for _ in range(swap_count):
        idx1 = rng.randint(0, n - 1)
        idx2 = rng.randint(max(0, idx1 - 5), min(n - 1, idx1 + 5))
        alerts[idx1], alerts[idx2] = alerts[idx2], alerts[idx1]

    return alerts


def generate_login_events(n: int, bounds: float = 1000.0, seed: int = 42) -> List[Tuple[float, float]]:
    """
    Generate n 2D login coordinates (x, y) uniformly distributed in [0, bounds] x [0, bounds] (km).
    Uses a fixed random seed for 100% reproducible scientific benchmarking.
    """
    rng = random.Random(seed)
    # Round to 3 decimal places to simulate realistic GPS telemetry (meter accuracy)
    return [(round(rng.uniform(0.0, bounds), 3), round(rng.uniform(0.0, bounds), 3)) for _ in range(n)]


def generate_blocklist_data(m_blocked: int, q_queries: int, seed: int = 42) -> Tuple[List[str], List[str]]:
    """Generate a blocklist of M IP addresses and Q query IPs."""
    rng = random.Random(seed)

    def random_ip():
        return f"{rng.randint(1, 223)}.{rng.randint(0, 255)}.{rng.randint(0, 255)}.{rng.randint(1, 254)}"

    blocklist = [random_ip() for _ in range(m_blocked)]
    # Half queries from blocklist (hits), half new random IPs (misses)
    queries = []
    for i in range(q_queries):
        if i % 2 == 0 and blocklist:
            queries.append(rng.choice(blocklist))
        else:
            queries.append(random_ip())

    return blocklist, queries
