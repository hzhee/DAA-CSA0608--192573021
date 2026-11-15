# Combined Pseudocode

## Module 1 Stable Merge Sort

```text
MERGE_SORT(A)
  if length(A) <= 1: return A
  mid = floor(length(A) / 2)
  L = MERGE_SORT(A[0..mid-1]); R = MERGE_SORT(A[mid..end])
  return MERGE(L, R)

MERGE(L, R)
  result = empty list; i = j = 0
  while i < length(L) and j < length(R)
    if L[i].timestamp <= R[j].timestamp   // equality takes left item
      append L[i]; i = i + 1
    else append R[j]; j = j + 1
  append remaining L and R to result
  return result
```

## Module 2 Quick Sort with Median of Three Pivot

```text
QUICK_SORT(A, low, high)
  if low < high
    p = PARTITION(A, low, high)
    QUICK_SORT(A, low, p - 1)
    QUICK_SORT(A, p + 1, high)

PARTITION(A, low, high)
  pivotIndex = median index of A[low], A[floor((low+high)/2)], A[high]
  swap A[pivotIndex], A[high]; pivot = A[high]; i = low
  for j = low to high - 1
    if A[j] <= pivot: swap A[i], A[j]; i = i + 1
  swap A[i], A[high]
  return i
```

## Module 3 First Occurrence Binary Search

```text
FIRST_TIMESTAMP(A, target)
  low = 0; high = length(A) - 1; answer = -1
  while low <= high
    mid = low + floor((high - low) / 2)
    if A[mid].timestamp >= target
      if A[mid].timestamp = target: answer = mid
      high = mid - 1             // retain a candidate, seek earlier one
    else low = mid + 1
  return answer
```

## Module 4 Strassen Matrix Multiplication

```text
STRASSEN(A, B)
  if size(A) <= cutoff: return CONVENTIONAL_MULTIPLY(A, B)
  split A into A11,A12,A21,A22 and B into B11,B12,B21,B22
  M1 = S(A11+A22, B11+B22); M2 = S(A21+A22, B11)
  M3 = S(A11, B12-B22);     M4 = S(A22, B21-B11)
  M5 = S(A11+A12, B22);     M6 = S(A21-A11, B11+B12)
  M7 = S(A12-A22, B21+B22)
  C11 = M1+M4-M5+M7; C12 = M3+M5
  C21 = M2+M4;       C22 = M1+M3-M2+M6
  return combine(C11,C12,C21,C22)
```
