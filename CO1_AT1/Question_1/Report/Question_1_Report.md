# CO1 Assessment Tool 1 - Question 1

## ShopSphere scalability audit

**Assumption for part (g):** the leading work term is counted as basic operations. The supplied machine rate is 10 basic operations per second, and the nightly limit is 600 seconds. Logarithms are base 2.

## (a) Input size and basic operations

| Module | Input size | Dominant basic operation and location | Growth |
|---|---:|---|---|
| M1 | `n` products | Compare the title and seller of pair `(i, j)` in the inner loop | One comparison per unordered pair: quadratic |
| M2 | `n` requests | `Audit(Request[j])` in the inner loop | The window sizes are `1, 2, 4, ...`; their sum is linear |
| M3/S1 | `n` catalogue entries | Compare a product key with the current sequential entry | Up to one comparison per entry: linear |
| M3/S2 | `n` sorted index entries | Compare the key with the middle entry | One comparison per level; half the search space is discarded: logarithmic |
| M4 | `n` customer-product records | Merge/combination work after recursive subproblems | Current design creates four half-size calls; redesigned design creates two |
| M5 | `n` sales records | Per-level sort/merge work | `n log n` work per recurrence level over `log n` levels |

## (b) Iterative modules

### M1 - duplicate-listing detector

For each `i`, the inner loop executes `n - 1 - i` comparisons. Therefore

```text
C(n) = sum(i=0 to n-2) (n - 1 - i)
     = (n - 1) + (n - 2) + ... + 1
     = n(n - 1)/2.
```

Thus M1 takes `Theta(n^2)` time and `Theta(1)` auxiliary space: its loop indices and one comparison result do not grow with `n`.

### M2 - API rate limiter

Let `k = ceil(log2 n)`. The outer loop audits windows of sizes `1, 2, 4, ..., 2^(k-1)`, so

```text
A(n) = 1 + 2 + 4 + ... + 2^(k-1)
     = 2^k - 1
     = 2^ceil(log2 n) - 1.
```

This is at least `n - 1` and below `2n - 1`, hence it is `Theta(n)`, not `Theta(n log n)`. For `n = 1,024`, `A(1024) = 2^10 - 1 = 1,023` audit operations. Auxiliary space is `Theta(1)`.

## (c) S2 recurrence by backward substitution

For `n = 2^k`, repeatedly substitute the recurrence:

```text
T(n)       = T(n/2) + 1
           = T(n/4) + 1 + 1
           = T(n/8) + 1 + 1 + 1
           = ...
           = T(n/2^k) + k
           = T(1) + k
           = 1 + log2 n.
```

So S2 performs exactly `log2 n + 1` comparisons when `n` is a power of two; for arbitrary `n`, its worst-case upper bound is `ceil(log2 n) + 1`. Its time is `Theta(log n)`. An iterative binary search uses `Theta(1)` auxiliary space; a recursive implementation uses `Theta(log n)` call-stack space.

## (d) Master Theorem

### M4 recommendation engine

| Design | `a` | `b` | `f(n)` | `n^(log_b a)` | Case and bound |
|---|---:|---:|---|---|---|
| Current | 4 | 2 | `n` | `n^2` | Case 1: `f(n) = O(n^(2-1))`; `Theta(n^2)` |
| Redesigned | 2 | 2 | `n` | `n` | Case 2: equal terms; `Theta(n log n)` |

When `n` doubles, the current `Theta(n^2)` work is multiplied by about 4. The redesigned `Theta(n log n)` work is multiplied by `2(log2 n + 1)/log2 n`, only slightly more than 2 for large `n`.

### M5 sales analytics engine

Here `a = 2`, `b = 2`, `n^(log_b a) = n`, and `f(n) = n log n`. The three elementary forms do not directly apply because `f(n)` is neither polynomially smaller/larger than `n` nor exactly `Theta(n)`. The extended Case 2 (`f(n) = Theta(n log^1 n)`) yields:

```text
T(n) = Theta(n log^(1+1) n) = Theta(n log^2 n).
```

## (e) Best, average, and worst search cases

| Search | Best case | Average case | Worst case |
|---|---|---|---|
| S1 sequential | First entry: 1 comparison | Existing key, uniformly located: `(n + 1)/2` | Last entry or absent key: `n` |
| S2 binary | Middle entry: 1 comparison | `Theta(log n)` | Deepest successful/unsuccessful path: at most `ceil(log2 n) + 1` |

If S1 has probability `p` of an existing product (uniformly distributed when present), and an absent product scans all `n` entries, then

```text
E[C] = p(n + 1)/2 + (1 - p)n.
```

For `n = 1,000,000` and `p = 0.5`, `E[C] = 0.5(500,000.5) + 0.5(1,000,000) = 750,000.25` comparisons.

## (f) Formal asymptotic proof for the report generator

Let `f(n) = 3n^2 + 10n log2 n + 50`. For `n >= 2`, `log2 n <= n`, and `50 <= 25n^2`; therefore

```text
f(n) <= 3n^2 + 10n^2 + 25n^2 = 38n^2.
```

Choose `c2 = 38` and `n0 = 2`; this proves `f(n) = O(n^2)`. Also, for every `n >= 1`, `f(n) >= 3n^2`. Choose `c1 = 3` and `n0 = 1`; this proves `f(n) = Omega(n^2)`. Together, `f(n) = Theta(n^2)`.

It is not `O(n)`: if `f(n) <= cn` for some positive `c` and all sufficiently large `n`, then `3n^2 <= cn`, so `n <= c/3`. Choosing any `n > max(n0, c/3)` contradicts the claim.

## (g) Scalability decision at one million products

| Module | Estimated operations | Estimated runtime | 10-minute result | Recommendation |
|---|---:|---:|---|---|
| M1 | `499,999,500,000` | `49,999,950,000 s` (about 1,585 years) | Fail | Replace all-pairs comparison with a hash map keyed by `(title, seller)`; expected `Theta(n)` time and `Theta(n)` space. |
| M2 | `1,048,575` | `104,857.5 s` (29.13 hours) | Fail | Batch or cap request-window audits; the current code is already asymptotically linear but too slow at the stated rate. |
| S2 | at most `21` | at most `2.1 s` | Pass | Keep sorted-index binary search. |
| M4 current | `1,000,000,000,000` | `100,000,000,000 s` (about 3,171 years) | Fail | Remove replicated partitions, yielding the proposed `Theta(n log n)` recurrence. |
| M4 redesign | about `19,931,568.57` | about `1,993,156.86 s` (23.07 days) | Fail | It is an essential asymptotic improvement but still misses this unusually low throughput target; use more hardware and/or reduce the per-record work. |
| M5 | about `397,267,425.63` | about `39,726,742.56 s` (459.80 days) | Fail | Avoid sorting from scratch at every recursive level; use a single merge-sort-style `Theta(n log n)` pipeline or maintain incremental aggregates. |

The executable program in `../Source_Code/scalability_audit.py` reproduces these estimates without impractical looping. Its unit tests verify the M1 and M2 closed forms (including the required `n = 1,024` check); the captured terminal result is in `../Source_Code/verified_output.txt`.
