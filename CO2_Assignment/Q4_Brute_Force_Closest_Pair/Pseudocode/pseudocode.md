# Q4 – Brute-Force Closest Pair of Points Pseudocode
## Drone Monitoring System: Find Two Closest Drones
### Student: HRUZHEECAYSHAN T K | Reg No: 192573021 | CO2 Assignment

---

## Algorithm: BruteForceClosestPair

```
ALGORITHM BruteForceClosestPair(P[0..n-1])
// Find the pair of points with minimum Euclidean distance
// Input : Array P of n points, each P[i] = (x_i, y_i)
// Output: Indices of closest pair, minimum distance, distance_calculations

  min_dist   ← INFINITY
  pair       ← (-1, -1)
  dist_calcs ← 0

  FOR i ← 0 TO n-2 DO
      FOR j ← i+1 TO n-1 DO
          dist_calcs ← dist_calcs + 1
          dx ← P[i].x - P[j].x
          dy ← P[i].y - P[j].y
          d  ← SQRT(dx² + dy²)       // Euclidean distance
          IF d < min_dist THEN
              min_dist ← d
              pair     ← (i, j)
          END IF
      END FOR
  END FOR
  RETURN pair, min_dist, dist_calcs
```

**Step-by-Step Logic:**
1. Initialise `min_dist = ∞` and `pair = (-1, -1)`.
2. Use two nested loops to consider every **distinct unordered pair** `(i, j)` where `i < j`.
   - Using `i < j` avoids checking `(i,j)` and `(j,i)` separately (same distance).
3. For each pair, compute Euclidean distance: `d = √((x_i−x_j)² + (y_i−y_j)²)`.
4. If `d < min_dist`, update `min_dist` and record the pair.
5. After ALL pairs examined, return the closest pair with its distance.

---

## Candidate Pair Representation

Each candidate is an **unordered pair** `{i, j}` with `i < j`:
- Total candidates = C(n,2) = n(n-1)/2
- For n=10: **45 pairs** | n=100: **4,950 pairs** | n=1000: **499,500 pairs**

**Optimisation note:** Compare d² instead of d to avoid sqrt during comparison:
```
d_sq = (x_i - x_j)² + (y_i - y_j)²
```
Only compute sqrt for the final minimum to get the actual distance value.

---

## Complexity Analysis

**Mathematical derivation:**

```
Distance calculations = Σ(i=0 to n-2) (n-1-i)
                      = (n-1) + (n-2) + ... + 1
                      = n(n-1)/2
                      ∈ Θ(n²)
```

| n      | Distance Calculations | Growth (when n doubles) |
|--------|----------------------|------------------------|
| 10     | 45                   | —                      |
| 50     | 1,225                | —                      |
| 100    | 4,950                | 4.0x                   |
| 200    | 19,900               | 4.0x                   |
| 500    | 124,750              | ~4.0x                  |
| 1,000  | 499,500              | ~4.0x                  |

When n doubles → distance calculations quadruple (**confirms O(n²)**)

---

## Test Datasets

**Dataset 1 – Boundary + Interior points:**
```
Points: (0,0), (10,0), (10,10), (0,10), (5,5), (3,3), (7,8), (1,9)
Expected: closest pair among interior points
```

**Dataset 2 – Dense random cluster (challenging):**
```
20 random points in [0,5]×[0,5] — many very close pairs
Tests worst-case scenario where min_dist updates frequently
```

---

## Limitation of Brute-Force

- O(n²) becomes impractical for large drone fleets (n > 100,000).
- At n = 100,000: ~5,000,000,000 calculations — infeasible in real-time.
- **Recommended improvement:** Divide-and-Conquer Closest Pair → O(n log n).
- Brute force is acceptable for n ≤ ~10,000 drone fleets.
