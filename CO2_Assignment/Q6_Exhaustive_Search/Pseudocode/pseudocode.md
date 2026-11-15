# Q6 – Exhaustive Search: Humanitarian Airlift Planning Pseudocode
## 0/1 Knapsack via Exhaustive Enumeration
### Student: HRUZHEECAYSHAN T K | Reg No: 192573021 | CO2 Assignment

---

## Problem Context

A helicopter has a strict **payload limit W = 8 kg**. Select packages to **maximise humanitarian value** without exceeding weight.

| Package ID | Name           | Weight | Value |
|-----------|----------------|--------|-------|
| 1         | Medical Kits   | 2 kg   | 6     |
| 2         | Food Packs     | 3 kg   | 7     |
| 3         | Water Supplies | 4 kg   | 8     |
| 4         | Shelter Tarps  | 5 kg   | 9     |
| 5         | First Aid      | 1 kg   | 3     |

---

## Candidate Representation

Each candidate solution is a **binary vector** of length n:
```
x = [x₁, x₂, ..., xₙ]   where xᵢ ∈ {0, 1}
xᵢ = 1 → package i selected
xᵢ = 0 → package i excluded
```
Total candidates = **2ⁿ subsets** (including empty set)

---

## Algorithm: ExhaustiveKnapsack

```
ALGORITHM ExhaustiveKnapsack(packages[0..n-1], W)
// Enumerate ALL 2^n subsets; return feasible one with maximum value
// Input : n packages with (weight, value), capacity W
// Output: best_subset, best_value, combos_examined

  best_value      ← 0
  best_subset     ← ∅
  combos_examined ← 0

  FOR mask ← 0 TO (2ⁿ − 1) DO
      combos_examined ← combos_examined + 1
      current_weight  ← 0
      current_value   ← 0
      current_subset  ← []

      FOR i ← 0 TO n-1 DO
          IF BIT(mask, i) = 1 THEN       // Package i is selected
              current_weight ← current_weight + packages[i].weight
              current_value  ← current_value  + packages[i].value
              APPEND i TO current_subset
          END IF
      END FOR

      // Feasibility check
      IF current_weight ≤ W THEN
          IF current_value > best_value THEN
              best_value  ← current_value
              best_subset ← current_subset
          END IF
      END IF
  END FOR

  RETURN best_subset, best_value, combos_examined
```

**Step-by-Step Logic:**
1. Represent each subset as an integer **mask** from 0 to 2ⁿ−1.
2. Bit `i` of mask = 1 means package `i` is included in this candidate.
3. For each mask: decode the subset → compute total weight and value.
4. **Feasibility check:** `total_weight ≤ W`.
5. If feasible and value > current best: update best.
6. After all 2ⁿ subsets evaluated: return the best feasible solution.

---

## Correctness Verification (Small Instance, manual check)

**Packages:** P1(w=2,v=6), P2(w=3,v=7), P3(w=4,v=8) | **W = 5**

| Subset      | Weight | Value | Feasible | Note        |
|-------------|--------|-------|----------|-------------|
| {}          | 0      | 0     | ✓        |             |
| {P1}        | 2      | 6     | ✓        |             |
| {P2}        | 3      | 7     | ✓        |             |
| {P3}        | 4      | 8     | ✓        |             |
| **{P1,P2}** | **5**  | **13**| **✓**    | **OPTIMAL** |
| {P1,P3}     | 6      | 14    | ✗        | Overweight  |
| {P2,P3}     | 7      | 15    | ✗        | Overweight  |
| {P1,P2,P3}  | 9      | 21    | ✗        | Overweight  |

**Result: {P1, P2}, value = 13** ← independently verified ✓

---

## Exponential Growth Analysis

**Prediction:** T(n) = 2ⁿ combinations

| n  | Candidates     | Ratio    |
|----|---------------|----------|
| 5  | 32            | 2x/item  |
| 10 | 1,024         | 2x/item  |
| 15 | 32,768        | 2x/item  |
| 20 | 1,048,576     | 2x/item  |
| 25 | 33,554,432    | 2x/item  |
| 30 | 1,073,741,824 | 2x/item  |

**Why one extra package causes dramatic growth:**
Adding one package to n packages **doubles** the solution space. Every existing subset can now **include or exclude** the new package — binary branching at each step gives 2ⁿ growth. Going from n=25 to n=26 adds **33 million** new candidates.

---

## Deployment Decision

**Fixed response time: 5 seconds** (justified: emergency humanitarian context)

| n  | Subsets    | Time (est. Python ~1M/sec) | Decision    |
|----|-----------|---------------------------|-------------|
| 20 | 1,048,576 | ~1 sec                    | ✓ DEPLOY    |
| 22 | 4,194,304 | ~4 sec                    | ✓ BORDERLINE|
| 23 | 8,388,608 | ~8 sec                    | ✗ TOO SLOW  |
| 25 | 33,554,432| ~33 sec                   | ✗ REJECT    |

**Deployment boundary: n ≤ 22 packages** for 5-second response guarantee.
For n > 22: use **Dynamic Programming** (O(nW)) or **Branch-and-Bound**.
