# Brute_Force_String_Matching_Pseudocode

================================================================================
ALGORITHM: ATTACK SIGNATURE SCANNING (STRING MATCHING)
MODULE: SentinelOps SOC Telemetry Pipeline
================================================================================

1. ORIGINAL BUGGY ALGORITHM (As written by junior developer):
--------------------------------------------------------------------------------
ALGORITHM FindSignature_Buggy(log[0..n-1], pattern[0..m-1]):
    hits ← empty list
    for i ← 0 to n - m - 1 do                           // DEFECT 5: Omits final valid index (n - m)!
        for j ← 0 to m - 1 do
            if log[i + j] ≠ pattern[j] then
                break
        if j == m - 1 then                              // DEFECT 6 & 7: Check outside inner loop fires
            hits.append(i)                              // when loop breaks on last character (false positive)!
    return hits


2. CORRECTED BRUTE-FORCE STRING MATCHING:
--------------------------------------------------------------------------------
ALGORITHM FindSignature_Corrected(log[0..n-1], pattern[0..m-1]):
    Input:  log string of length n, pattern string of length m
    Output: list of all 0-based starting indices where pattern occurs in log

    hits ← empty list
    if m == 0 or n < m then
        return hits

    // FIX 5: Loop bounds 0 to n - m inclusive (range(n - m + 1) in Python)
    for i ← 0 to n - m do
        matched ← true
        for j ← 0 to m - 1 do
            if log[i + j] ≠ pattern[j] then
                matched ← false
                break
        // FIX 6 & 7: Validated match flag ensures only non-breaking complete matches are appended
        if matched then
            hits.append(i)

    return hits


3. PRODUCTION OPTIMISED ALGORITHM: KNUTH-MORRIS-PRATT (KMP):
--------------------------------------------------------------------------------
ALGORITHM Compute_LPS(pattern[0..m-1]):
    Input:  pattern string of length m
    Output: LPS array of length m (Longest Proper Prefix which is also Suffix)

    LPS ← array of size m initialized to 0
    length ← 0
    i ← 1

    while i < m do
        if pattern[i] == pattern[length] then
            length ← length + 1
            LPS[i] ← length
            i ← i + 1
        else
            if length ≠ 0 then
                length ← LPS[length - 1]
            else
                LPS[i] ← 0
                i ← i + 1
    return LPS

ALGORITHM FindSignature_KMP(log[0..n-1], pattern[0..m-1]):
    Input:  log string of length n, pattern string of length m
    Output: list of all starting positions where pattern occurs in log

    hits ← empty list
    if m == 0 or n < m then return hits

    LPS ← Compute_LPS(pattern)
    i ← 0  // pointer in log
    j ← 0  // pointer in pattern

    while i < n do
        if log[i] == pattern[j] then
            i ← i + 1
            j ← j + 1

        if j == m then
            hits.append(i - j)          // Complete match found
            j ← LPS[j - 1]              // Shift pattern using LPS
        else if i < n and log[i] ≠ pattern[j] then
            if j ≠ 0 then
                j ← LPS[j - 1]          // Advance pattern without backtracking log pointer i
            else
                i ← i + 1               // Advance log pointer
    return hits


4. COMPLEXITY ANALYSIS SUMMARY:
--------------------------------------------------------------------------------
+--------------------------+-------------------+-------------------+-------------------+---------------+
| Algorithm                | Best Case (Ω)     | Average Case (Θ)  | Worst Case (O)    | Space (Aux)   |
+--------------------------+-------------------+-------------------+-------------------+---------------+
| Corrected Brute Force    | Ω(n)              | Θ(n + m)          | O((n - m + 1) · m)| O(1)          |
| Optimised KMP            | Ω(n)              | Θ(n + m)          | O(n + m)          | O(m)          |
+--------------------------+-------------------+-------------------+-------------------+---------------+

* Key Advantage of KMP in SOC Pipelines:
  - Deterministic linear time guarantee: attacker cannot craft adversarial repetitive payloads
    (e.g., "AAAA...AAB") to cause algorithmic complexity attacks or CPU denial of service.
  - Zero redundant comparisons: the text stream pointer i never regresses.
================================================================================


# Closest_Pair_Pseudocode

================================================================================
ALGORITHM: CLUSTERED LOGIN DETECTION (CLOSEST PAIR OF 2D POINTS)
MODULE: SentinelOps SOC Telemetry Pipeline
================================================================================

1. ORIGINAL BUGGY ALGORITHM (As written by junior developer):
--------------------------------------------------------------------------------
ALGORITHM ClosestLogins_Buggy(events[0..n-1]):
    min_dist ← 0                                        // DEFECT 8: Initialized to 0; no real distance can be < 0!
    pair ← null
    for i ← 0 to n - 1 do
        for j ← 0 to n - 1 do                           // Evaluates self-pairs (i == j) and symmetric duplicates (j, i)
            d ← sqrt((events[i].x - events[j].x)² +
                     (events[i].y - events[j].y)²)
            if d > min_dist then                        // DEFECT 9: Inequality finds MAXIMUM (farthest pair)!
                min_dist ← d
                pair ← (i, j)
    return pair, min_dist


2. CORRECTED PAIRWISE BRUTE-FORCE ALGORITHM:
--------------------------------------------------------------------------------
ALGORITHM ClosestLogins_Corrected(events[0..n-1]):
    Input:  events array of n 2D coordinate tuples (x, y)
    Output: ((i, j), min_distance) of closest pair

    if n < 2 then
        return null, ∞

    min_dist ← ∞                                        // FIX 8: Initialized to infinity
    pair ← null

    for i ← 0 to n - 1 do
        for j ← i + 1 to n - 1 do                       // FIX 9b: Evaluates only distinct pairs i < j (n(n-1)/2 pairs)
            d ← sqrt((events[i].x - events[j].x)² +
                     (events[i].y - events[j].y)²)
            if d < min_dist then                        // FIX 9a: Strict minimization (<)
                min_dist ← d
                pair ← (i, j)

    return pair, min_dist


3. PRODUCTION OPTIMISED ALGORITHMS:
--------------------------------------------------------------------------------
A. Geometric Sweep-Line Pruning with Squared Distances:
-------------------------------------------------------
ALGORITHM ClosestLogins_SweepLine(events[0..n-1]):
    Input:  events array of n 2D coordinate tuples (x, y)
    Output: ((orig_i, orig_j), min_dist)

    if n < 2 then return null, ∞

    // Tag each event with its original index
    P ← [(events[k].x, events[k].y, k) for k ← 0 to n - 1]
    Sort P in ascending order of x-coordinate            // O(n log n)

    min_dist_sq ← ∞
    best_pair ← null

    for i ← 0 to n - 1 do
        for j ← i + 1 to n - 1 do
            dx ← P[j].x - P[i].x

            // Geometric Pruning: Since P is sorted by x, if dx² ≥ min_dist_sq,
            // no point k ≥ j can possibly be closer than current minimum!
            if dx * dx ≥ min_dist_sq then
                break                                   // Immediate break from inner loop!

            dy ← P[j].y - P[i].y
            d_sq ← dx * dx + dy * dy                    // Avoid expensive square root!
            if d_sq < min_dist_sq then
                min_dist_sq ← d_sq
                best_pair ← (min(P[i].idx, P[j].idx), max(P[i].idx, P[j].idx))

    return best_pair, sqrt(min_dist_sq)                 // Exactly 1 square root computation!


B. Optimal Divide-and-Conquer Closest Pair:
-------------------------------------------
ALGORITHM ClosestLogins_DivideAndConquer(P_sorted_by_x[0..n-1]):
    if n ≤ 3 then
        return Pairwise_Brute_Force(P_sorted_by_x)

    mid ← ⌊n / 2⌋
    mid_x ← P_sorted_by_x[mid].x

    (pair_L, δ_L²) ← ClosestLogins_DivideAndConquer(P_sorted_by_x[0..mid-1])
    (pair_R, δ_R²) ← ClosestLogins_DivideAndConquer(P_sorted_by_x[mid..n-1])

    δ² ← min(δ_L², δ_R²)
    best_pair ← pair corresponding to min(δ_L², δ_R²)

    // Extract vertical strip of width 2δ around mid_x
    Strip ← [point in P_sorted_by_x where (point.x - mid_x)² < δ²]
    Sort Strip by y-coordinate                          // Or maintain sorted y during merge

    for i ← 0 to len(Strip) - 1 do
        for j ← i + 1 to min(i + 7, len(Strip) - 1) do   // Geometrically at most 7 points!
            if (Strip[j].y - Strip[i].y)² ≥ δ² then break
            d_sq ← DistSquared(Strip[i], Strip[j])
            if d_sq < δ² then
                δ² ← d_sq
                best_pair ← (Strip[i].idx, Strip[j].idx)

    return best_pair, δ²


4. COMPLEXITY ANALYSIS SUMMARY:
--------------------------------------------------------------------------------
Let n = batch size of login events (e.g., 8,000 events/day).

+--------------------------+-------------------+-------------------+-------------------+---------------+
| Implementation           | Distance Evals    | Sqrt Operations   | Time Complexity   | Space (Aux)   |
+--------------------------+-------------------+-------------------+-------------------+---------------+
| Original Buggy           | n²                | n²                | Θ(n²)             | O(1)          |
| Corrected Brute Force    | n(n - 1) / 2      | n(n - 1) / 2      | Θ(n²)             | O(1)          |
| Optimised Sweep-Line     | O(n √n) avg       | Exactly 1         | O(n log n) avg    | O(n)          |
| Divide-and-Conquer       | O(n log n)        | Exactly 1         | Θ(n log n) worst  | O(n)          |
+--------------------------+-------------------+-------------------+-------------------+---------------+

* Numerical Comparison at n = 8,000:
  - Original Buggy:        64,000,000 distances, 64,000,000 sqrt operations.
  - Corrected Brute Force: 31,996,000 distances, 31,996,000 sqrt operations (~10.7 seconds).
  - Optimised Sweep-Line:  21,150 distances, 1 sqrt operation (~0.021 seconds, 502x speedup).
  - Divide-and-Conquer:    ~100,000 operations, 1 sqrt operation.
================================================================================


# Sequential_Search_Pseudocode

================================================================================
ALGORITHM: THREAT INTELLIGENCE BLOCKLIST SEARCH
MODULE: SentinelOps SOC Telemetry Pipeline
================================================================================

1. ORIGINAL BUGGY ALGORITHM (As written by junior developer):
--------------------------------------------------------------------------------
ALGORITHM IsBlocked_Buggy(blocklist[0..m-1], target_ip):
    Input:  blocklist, array of m blocked IP strings; target_ip, string
    Output: boolean indicating whether target_ip is blocked

    for i ← 0 to m - 1 do
        if blocklist[i] == target_ip then
            return false                                // DEFECT 3: Inverted boolean logic (returns false on match)!
        else
            return false                                // DEFECT 4: Premature return in loop aborts on index 0!


2. CORRECTED SEQUENTIAL SEARCH ALGORITHM:
--------------------------------------------------------------------------------
ALGORITHM IsBlocked_Corrected(blocklist[0..m-1], target_ip):
    Input:  blocklist, array of m blocked IP strings; target_ip, string
    Output: true if target_ip is in blocklist, false otherwise

    for i ← 0 to m - 1 do
        if blocklist[i] == target_ip then
            return true                                 // FIX 3: Return true upon finding exact match

    return false                                        // FIX 4: Return false only after all elements checked


3. PRODUCTION OPTIMISED ALGORITHM (HASH SET REGISTRY):
--------------------------------------------------------------------------------
ALGORITHM ThreatIntel_Registry_Build(blocklist[0..m-1]):
    Input:  blocklist, array of m IP strings
    Output: hash_set containing all blocked IPs

    H ← new HashSet()
    for each ip in blocklist do
        H.insert(ip)                                    // Preprocessed in O(m) time and O(m) space
    return H

ALGORITHM IsBlocked_Optimised(H, target_ip):
    Input:  H, pre-indexed HashSet of blocked IPs; target_ip, string
    Output: true if target_ip ∈ H, false otherwise

    return target_ip ∈ H                                // Instant O(1) average lookup via hashing


4. COMPLEXITY ANALYSIS SUMMARY:
--------------------------------------------------------------------------------
Let m = size of blocklist, Q = number of incoming queries (e.g., 50,000 alerts/day).

+--------------------------+-------------------+-------------------+-------------------+---------------+
| Implementation           | Single Query Time | Q Queries Time    | Worst Case Time   | Aux Space     |
+--------------------------+-------------------+-------------------+-------------------+---------------+
| Corrected Sequential     | Ω(1) Best         | Θ(Q · m)          | O(Q · m)          | O(1)          |
| Optimised Hash Set       | Θ(1) Average      | Θ(m + Q)          | O(m + Q)          | O(m)          |
+--------------------------+-------------------+-------------------+-------------------+---------------+

* For SentinelOps with m = 10,000 and Q = 50,000:
  Sequential Search: 50,000 × 10,000 = 500,000,000 string comparisons!
  Hash Set Lookup:   10,000 (build) + 50,000 (lookups) = 60,000 operations (~8,300x speedup).
================================================================================


# Sorting_Pseudocode

================================================================================
ALGORITHM: ALERT TRIAGE SEVERITY SORTING (INSERTION SORT)
MODULE: SentinelOps SOC Telemetry Pipeline
================================================================================

1. ORIGINAL BUGGY ALGORITHM (As written by junior developer):
--------------------------------------------------------------------------------
ALGORITHM SortAlerts_Buggy(alerts[0..n-1]):
    Input:  alerts, an array of n tuples (alert_id, severity)
    Output: alerts sorted in descending order of severity

    for i ← 1 to n - 1 do
        key ← alerts[i]
        j ← i - 1
        while j > 0 and alerts[j].severity < key.severity do    // DEFECT 1: j > 0 skips index 0!
            alerts[j + 1] ← alerts[j]
            j ← j - 1
        alerts[j] ← key                                         // DEFECT 2: Overwrites index j instead of j+1!
    return alerts


2. CORRECTED STABLE ALGORITHM (Systematically Debugged):
--------------------------------------------------------------------------------
ALGORITHM SortAlerts_Corrected(alerts[0..n-1]):
    Input:  alerts, an array of n tuples (alert_id, severity)
    Output: alerts stably sorted in descending order of severity (highest first)

    if n ≤ 1 then
        return alerts

    for i ← 1 to n - 1 do
        key ← alerts[i]
        j ← i - 1
        // FIX 1: j ≥ 0 ensures element at index 0 is compared and shifted if needed
        // Strict inequality (<) ensures stability: equal elements are NEVER shifted,
        // preserving earlier arrival order.
        while j ≥ 0 and alerts[j].severity < key.severity do
            alerts[j + 1] ← alerts[j]
            j ← j - 1
        // FIX 2: key is placed at j + 1, into the vacant slot left by the right shifts
        alerts[j + 1] ← key
    return alerts

Loop Invariant:
    At the start of each iteration i, subarray alerts[0..i-1] contains the original
    first i elements stably sorted in non-increasing order of severity.


3. PRODUCTION OPTIMISED ALGORITHMS:
--------------------------------------------------------------------------------
A. Adaptive Fast-Path Insertion Sort (For nearly-sorted alert streams):
-----------------------------------------------------------------------
ALGORITHM SortAlerts_Adaptive(alerts[0..n-1]):
    if n ≤ 1 then return alerts

    // Fast-path: O(n) scan to detect if already sorted
    is_sorted ← true
    for k ← 0 to n - 2 do
        if alerts[k].severity < alerts[k + 1].severity then
            is_sorted ← false
            break
    if is_sorted then
        return alerts

    // In-place stable insertion sort
    for i ← 1 to n - 1 do
        key ← alerts[i]
        j ← i - 1
        while j ≥ 0 and alerts[j].severity < key.severity do
            alerts[j + 1] ← alerts[j]
            j ← j - 1
        alerts[j + 1] ← key
    return alerts

B. Production Timsort (Standard Python C-level sort):
------------------------------------------------------
ALGORITHM SortAlerts_Timsort(alerts[0..n-1]):
    return Sort(alerts, key = λ(x): x.severity, reverse = true)
    // Exploits natural monotonic runs in alert telemetry; guarantees O(n log n) worst-case
    // and O(n) on presorted telemetry while guaranteeing stability.


4. COMPLEXITY ANALYSIS SUMMARY:
--------------------------------------------------------------------------------
+--------------------------+-------------------+-------------------+-------------------+---------------+
| Metric                   | Best Case (Ω)     | Average Case (Θ)  | Worst Case (O)    | Space (Aux)   |
+--------------------------+-------------------+-------------------+-------------------+---------------+
| Corrected Insertion Sort | Ω(n) (Presorted)  | Θ(n²)             | O(n²) (Ascending) | O(1) in-place |
| Adaptive Insertion Sort  | Ω(n)              | Θ(n + d)          | O(n²)             | O(1) in-place |
| Production Timsort       | Ω(n)              | Θ(n log n)        | O(n log n)        | O(n)          |
+--------------------------+-------------------+-------------------+-------------------+---------------+
* Where d is the number of inversions in the incoming alert stream.
================================================================================
