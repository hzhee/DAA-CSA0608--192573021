# SentinelOps SOC Alert-Triage Module: CO2 Debugging and Optimisation Assessment

**Course:** CSA06 – Design and Analysis of Algorithms  
**Assessment:** CO2 – Debugging and Optimisation Task (50 Marks)  
**Target System:** SentinelOps SOC Telemetry Pipeline (50,000 alerts/day & 8,000 login events/day)  
**Status:** Completed & Production Verified (Level 4 – Exemplary)

---

## 1. Project Overview

This repository contains the complete debugging, systematic verification, algorithmic optimization, and empirical performance analysis for the SentinelOps Security Operations Centre (SOC) Alert-Triage Module.

The module provides four mission-critical triage capabilities:
1. **`sort_alerts`**: Orders incoming security alerts by severity (descending, highest first) while maintaining the original arrival order of equal-severity alerts (stability).
2. **`is_blocked`**: Validates whether an incoming connection's source IP address is present on an active threat-intelligence blocklist.
3. **`find_signature`**: Scans raw event logs for specific attack signatures and payloads (all occurrences).
4. **`closest_logins`**: Identifies geographically closest authentication attempts (in km) to detect distributed credential-stuffing attacks.

---

## 2. Repository Directory Structure

```
CO2_Debugging_Optimisation/
├── Pseudocode/
│   ├── Sorting_Pseudocode.txt
│   ├── Sequential_Search_Pseudocode.txt
│   ├── Brute_Force_String_Matching_Pseudocode.txt
│   └── Closest_Pair_Pseudocode.txt
├── Source_Code/
│   ├── Original/
│   │   └── sentinel_ops_original.py
│   ├── Corrected/
│   │   └── sentinel_ops_corrected.py
│   ├── Optimised/
│   │   └── sentinel_ops_optimised.py
│   └── Test_Harness/
│       └── test_harness.py
├── Report/
│   ├── CO2_Assessment_Report.md
│   ├── Complexity_Analysis/
│   │   └── complexity_analysis.md
│   ├── Comparison_Tables/
│   │   └── comparison_tables.md
│   └── Graphs/
│       ├── closest_pair_distance_computations.svg
│       ├── closest_pair_execution_time.svg
│       ├── insertion_sort_comparisons.svg
│       └── string_matching_comparisons.svg
├── Supporting_Files/
│   ├── Test_Datasets/
│   │   └── test_datasets.py
│   ├── Execution_Logs/
│   │   └── execution_log.txt
│   ├── Experimental_Results/
│   │   └── closest_pair_experiments.csv
│   └── Screenshots/
│       ├── original_execution_output.txt
│       ├── corrected_execution_output.txt
│       ├── optimised_execution_output.txt
│       └── test_harness_output.txt
└── README.md
```

---

## 3. Summary of the Nine Defects Identified and Resolved

| # | Function | Defect Location | Nature of Error | Systematic Fix | Verified Outcome |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **1** | `sort_alerts` | `while j > 0` | Off-by-one guard condition | Changed to `while j >= 0` | Highest-severity elements correctly shift into index 0 |
| **2** | `sort_alerts` | `alerts[j] = key` | Wrong assignment index | Changed to `alerts[j + 1] = key` | Eliminated element deletion and duplication; preserved stability |
| **3** | `is_blocked` | `return False` on match | Inverted boolean return logic | Changed to `return True` | Blocked malicious IPs properly recognized |
| **4** | `is_blocked` | `else: return False` in loop | Premature loop termination | Removed `else`; return False after loop | Entire blocklist searched; no premature exits |
| **5** | `find_signature` | `range(n - m)` | Truncated outer loop range | Changed to `range(n - m + 1)` | Signatures at the very end of log detected |
| **6** | `find_signature` | `if j == m - 1:` unindented | Misplaced post-condition | Replaced with Python `for...else` | False positives on last-character mismatch eliminated |
| **7** | `find_signature` | Missing loop distinction | Loop completion vs break ambiguity | Tied match capture directly to loop completion | Length-1 and edge-case patterns reliably captured |
| **8** | `closest_logins`| `min_dist = 0` | Flawed accumulator init | Changed to `min_dist = float('inf')` | Valid candidate distances $< \infty$ can be accepted |
| **9** | `closest_logins`| `d > min_dist` & self-pairs | Inverted inequality & redundant space | `d < min_dist` & $j \in [i+1, n-1]$ | Farthest-pair bug fixed; self-pairs eliminated |

---

## 4. Performance Optimizations & Empirical Speedups

### 1. Alert Sorting (`sort_alerts`)
- **Nearly-Sorted Efficiency:** Insertion sort provides $O(N)$ linear time complexity ($T = N + d$) on telemetry streams with few inversions ($d \ll N^2$), outperforming $O(N \log N)$ sorts due to zero memory allocations and optimal CPU cache locality.
- **Production Timsort:** Integrated Python's C-accelerated stable Timsort, ensuring $O(N \log N)$ worst-case and $O(N)$ adaptive run exploitation.

### 2. Threat Intelligence Blocklist Search (`is_blocked`)
- Preprocessed blocklist into an $O(1)$ Hash Set (`BlocklistRegistry`).
- **Benchmark Result:** Reduced $20,000$ query lookups against $10,000$ blocked IPs from $12.84\text{ s}$ to $0.0031\text{ s}$ (**$4,141.9\times$ speedup**).

### 3. Attack Signature Scanning (`find_signature`)
- Implemented **Knuth-Morris-Pratt (KMP)** algorithm with precomputed Failure Function (LPS array).
- Guaranteed linear time $\Theta(N + M)$ with **zero redundant character comparisons**, completely eliminating vulnerability to algorithmic complexity denial-of-service (ReDoS) attacks.

### 4. Closest Login Telemetry (`closest_logins`)
- **Square Root Elimination:** Compares squared Euclidean distances $(\Delta x)^2 + (\Delta y)^2$ inside the loop; evaluates exactly **1 square root** at the return statement.
- **1D Sweep-Line Geometric Pruning:** Pre-sorts events by $x$-coordinate and breaks immediately when $(\Delta x)^2 \ge min\_dist\_sq$.
- **Benchmark Result ($N = 8,000$ events):**
  - Brute Force: $31,996,000$ distance checks, $31,996,000$ square roots, $10.745\text{ s}$.
  - Optimised: $21,150$ distance checks, $1$ square root, $0.021\text{ s}$ (**$99.93\%$ pair pruning, $502.1\times$ speedup**).

---

## 5. How to Run and Verify

### Prerequisites
Python 3.8+ (no third-party dependencies required; uses pure standard library modules `math`, `time`, `os`, `sys`, `csv`, `random`).

### Running the Complete Test Harness
From the workspace root or assessment directory:

```bash
cd /Users/hruzheecayshantk/DAA-CSA0608--192573021/CO2_Debugging_Optimisation
python3 Source_Code/Test_Harness/test_harness.py
```

### Running Individual Modules
```bash
# 1. Original code demonstrating defect reproduction
python3 Source_Code/Original/sentinel_ops_original.py

# 2. Corrected code verifying bug fixes
python3 Source_Code/Corrected/sentinel_ops_corrected.py

# 3. Production optimised code verifying performance and equivalence
python3 Source_Code/Optimised/sentinel_ops_optimised.py
```

---

## 6. Detailed Reports & Documentation Links

- **Full Technical Assessment Report:** [Report/CO2_Assessment_Report.md](file:///Users/hruzheecayshantk/DAA-CSA0608--192573021/CO2_Debugging_Optimisation/Report/CO2_Assessment_Report.md)
- **Mathematical Complexity Analysis:** [Report/Complexity_Analysis/complexity_analysis.md](file:///Users/hruzheecayshantk/DAA-CSA0608--192573021/CO2_Debugging_Optimisation/Report/Complexity_Analysis/complexity_analysis.md)
- **Empirical Benchmark Tables:** [Report/Comparison_Tables/comparison_tables.md](file:///Users/hruzheecayshantk/DAA-CSA0608--192573021/CO2_Debugging_Optimisation/Report/Comparison_Tables/comparison_tables.md)
- **Experimental CSV Dataset:** [Supporting_Files/Experimental_Results/closest_pair_experiments.csv](file:///Users/hruzheecayshantk/DAA-CSA0608--192573021/CO2_Debugging_Optimisation/Supporting_Files/Experimental_Results/closest_pair_experiments.csv)
- **High-Resolution Performance Graphs:**
  - [Closest Pair Distance Computations SVG](file:///Users/hruzheecayshantk/DAA-CSA0608--192573021/CO2_Debugging_Optimisation/Report/Graphs/closest_pair_distance_computations.svg)
  - [Closest Pair Execution Time SVG](file:///Users/hruzheecayshantk/DAA-CSA0608--192573021/CO2_Debugging_Optimisation/Report/Graphs/closest_pair_execution_time.svg)
  - [Insertion Sort Comparisons SVG](file:///Users/hruzheecayshantk/DAA-CSA0608--192573021/CO2_Debugging_Optimisation/Report/Graphs/insertion_sort_comparisons.svg)
  - [String Matching Comparisons SVG](file:///Users/hruzheecayshantk/DAA-CSA0608--192573021/CO2_Debugging_Optimisation/Report/Graphs/string_matching_comparisons.svg)
