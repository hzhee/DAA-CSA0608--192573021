# Q1 – Sorting Algorithms Pseudocode
## Selection Sort, Bubble Sort, Insertion Sort
### Student: HRUZHEECAYSHAN T K | Reg No: 192573021 | CO2 Assignment

---

## 1. Selection Sort Pseudocode

```
ALGORITHM SelectionSort(A[0..n-1])
// Sorts array A by finding minimum and placing it
// Input: Array A of n comparable elements
// Output: Array A sorted in non-decreasing order
// comparison_count = 0

FOR i ← 0 TO n-2 DO
    min_idx ← i
    FOR j ← i+1 TO n-1 DO
        comparison_count ← comparison_count + 1
        IF A[j] < A[min_idx] THEN
            min_idx ← j
        END IF
    END FOR
    IF min_idx ≠ i THEN
        SWAP(A[i], A[min_idx])
    END IF
END FOR
RETURN A, comparison_count
```

**Step-by-Step Logic:**
1. Start from index 0. Assume element at index 0 is minimum.
2. Scan the remaining unsorted portion (index 1 to n-1).
3. Each comparison checks if current element is smaller than current minimum.
4. After full scan, swap minimum with first unsorted element.
5. Repeat from next index. After n-1 passes, array is sorted.

**Complexity:**
- Best Case: O(n²) – always makes n(n-1)/2 comparisons regardless of input.
- Worst Case: O(n²)
- Average Case: O(n²)
- Space: O(1) – in-place

---

## 2. Bubble Sort Pseudocode

```
ALGORITHM BubbleSort(A[0..n-1])
// Sorts array A by repeatedly swapping adjacent out-of-order elements
// Input: Array A of n comparable elements
// Output: Array A sorted in non-decreasing order
// comparison_count = 0

FOR i ← 0 TO n-2 DO
    swapped ← FALSE
    FOR j ← 0 TO n-2-i DO
        comparison_count ← comparison_count + 1
        IF A[j] > A[j+1] THEN
            SWAP(A[j], A[j+1])
            swapped ← TRUE
        END IF
    END FOR
    IF NOT swapped THEN
        BREAK          // Early termination optimisation
    END IF
END FOR
RETURN A, comparison_count
```

**Step-by-Step Logic:**
1. In each pass, compare adjacent pairs from index 0 to n-2-i.
2. If left element > right element, swap them (bubble larger element right).
3. After each pass, the largest unsorted element is at its correct position.
4. If no swaps occur in a pass, array is sorted → early termination.
5. Worst case: n-1 passes needed.

**Complexity:**
- Best Case: O(n) – already sorted, one pass with no swaps (with optimisation)
- Worst Case: O(n²) – reverse sorted input
- Average Case: O(n²)
- Space: O(1) – in-place

---

## 3. Insertion Sort Pseudocode

```
ALGORITHM InsertionSort(A[0..n-1])
// Sorts array A by inserting each element into its correct position
// Input: Array A of n comparable elements
// Output: Array A sorted in non-decreasing order
// comparison_count = 0

FOR i ← 1 TO n-1 DO
    key ← A[i]
    j ← i - 1
    WHILE j ≥ 0 AND A[j] > key DO
        comparison_count ← comparison_count + 1
        A[j+1] ← A[j]
        j ← j - 1
    END WHILE
    IF j ≥ 0 THEN
        comparison_count ← comparison_count + 1   // Final comparison that failed
    END IF
    A[j+1] ← key
END FOR
RETURN A, comparison_count
```

**Step-by-Step Logic:**
1. Consider first element as sorted sub-array.
2. Pick next element (key) from unsorted portion.
3. Compare key with elements in sorted portion (right to left).
4. Shift all elements greater than key one position to the right.
5. Insert key at correct position.
6. Repeat until all elements processed.

**Complexity:**
- Best Case: O(n) – already sorted, one comparison per element
- Worst Case: O(n²) – reverse sorted, maximum shifts
- Average Case: O(n²)
- Space: O(1) – in-place

---

## Complexity Comparison Summary

| Algorithm      | Best Case | Average Case | Worst Case | Stable? | Adaptive? |
|----------------|-----------|--------------|------------|---------|-----------|
| Selection Sort | O(n²)     | O(n²)        | O(n²)      | No      | No        |
| Bubble Sort    | O(n)      | O(n²)        | O(n²)      | Yes     | Yes       |
| Insertion Sort | O(n)      | O(n²)        | O(n²)      | Yes     | Yes       |

**Mathematical Derivation (Comparison Count):**
- Selection Sort: Σ(i=0 to n-2) (n-1-i) = n(n-1)/2 ≈ n²/2
- Bubble Sort Worst: Σ(i=0 to n-2) (n-1-i) = n(n-1)/2 ≈ n²/2
- Insertion Sort Worst: Σ(i=1 to n-1) i = n(n-1)/2 ≈ n²/2
