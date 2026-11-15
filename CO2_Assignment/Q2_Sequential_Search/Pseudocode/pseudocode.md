# Q2 – Sequential Search Pseudocode
## When Is Sequential Search an Appropriate Engineering Choice?
### Student: HRUZHEECAYSHAN T K | Reg No: 192573021 | CO2 Assignment

---

## Sequential Search Pseudocode

```
ALGORITHM SequentialSearch(A[0..n-1], target)
// Searches for target in array A by checking each element
// Input: Array A of n elements, search target
// Output: Index of target if found, -1 if not found, comparison count

comparison_count ← 0
FOR i ← 0 TO n-1 DO
    comparison_count ← comparison_count + 1
    IF A[i] = target THEN
        RETURN i, comparison_count      // Successful search
    END IF
END FOR
RETURN -1, comparison_count             // Unsuccessful search
```

**Step-by-Step Logic:**
1. Start from the first element (index 0).
2. Compare current element with the target.
3. If equal, return the index and stop.
4. If not equal, move to the next element.
5. Repeat until found or entire array exhausted.
6. If not found, return -1.

---

## Analysis of Search Scenarios

### Successful Search at Position p:
```
comparison_count = p + 1   (positions are 0-indexed)
```

| Position | Comparisons | Fraction of n |
|----------|------------|---------------|
| First    | 1          | 1/n           |
| Middle   | n/2        | 50%           |
| Last     | n          | 100%          |

**Average successful search comparisons:**
= Σ(i=1 to n) [i × (1/n)] = (1/n) × n(n+1)/2 = (n+1)/2 ≈ n/2

### Unsuccessful Search:
```
comparison_count = n   (must check all elements)
```

---

## Engineering Decision Framework

```
FUNCTION isSequentialSearchAppropriate(n, search_frequency):
    // Heuristic analysis
    
    IF n <= 1000 AND search_frequency == "LOW" THEN
        RETURN "APPROPRIATE – overhead of sorting not justified"
    
    ELSE IF n <= 1000 AND search_frequency == "HIGH" THEN
        RETURN "MARGINAL – consider pre-sorting then binary search"
    
    ELSE IF n > 10000 AND search_frequency == "HIGH" THEN
        RETURN "INAPPROPRIATE – O(n) per search is too costly"
        RETURN "RECOMMEND: Sort once O(n log n), then binary search O(log n)"
    
    ELSE
        RETURN "EVALUATE based on update frequency vs search frequency"
    END IF
```

---

## Complexity Summary

| Scenario         | Comparisons | Complexity |
|-----------------|-------------|------------|
| Best Case        | 1           | O(1)       |
| Average (success)| (n+1)/2     | O(n)       |
| Worst Case       | n           | O(n)       |
| Unsuccessful     | n           | O(n)       |

**Key Engineering Insight:**
Sequential Search is O(n) per query. For n=10,000 items and 1,000 queries/day:
- Daily comparisons = 10,000 × 1,000 = 10,000,000 (ten million operations)
- Compare to binary search: 14 × 1,000 = 14,000 (with one-time sort cost)

**Deployment Boundary:**
- Reasonable for n ≤ 1,000 with infrequent queries
- Beyond n = 1,000 or with high frequency: use sorted list + binary search
