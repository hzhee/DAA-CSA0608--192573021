# CO3 Case Study Report

## Divide and Conquer Engine for KartIQ

**Course:** CSA06 Design and Analysis of Algorithms  
**Assessment:** CO3 Case Study  
**Student:** HRUZHEECAYSHAN T K

KartIQ processes about 10,000,000 orders daily, ranks 100,000 sellers, serves timestamp lookups, and refreshes recommendation scores. This report selects divide-and-conquer designs that preserve audit semantics and meet the stated production workloads. The outcome is stable Merge Sort for nightly consolidation, guarded Quick Sort for score refreshes, first-occurrence Binary Search for support, and a hybrid Strassen implementation for sufficiently large dense matrix products.

## Part a Understand the Case

| Module | Computational requirement | Critical issue | Consequence of a poor choice |
|---|---|---|---|
| Nightly order consolidation | Sort 10,000,000 `(timestamp, order ID)` records | Equal timestamps must retain arrival order; RAM may be insufficient | An unstable sort breaks audit reconciliation; a slow sort misses the nightly deadline |
| Live seller leaderboard | Re-sort 100,000 changing scores frequently | Inputs are often nearly sorted; first pivot makes unbalanced partitions | Quadratic work causes a visible freeze in sale events |
| Order lookup | Locate the first matching timestamp in the consolidated data | Data must be sorted; duplicates need the first record | Linear scan takes seconds; ordinary binary search can return a later duplicate |
| Recommendation scores | Multiply two dense 1,024 x 1,024 matrices | Arithmetic cost, temporary storage, cache/overhead | Conventional cubic work delays recommendation refreshes |

## Part b Module 1 Merge Sort

**Design.** Divide the order list into two halves, recursively sort each half, then combine two sorted halves. During merge, choose the left item on equal timestamps (`<=`). Because each half already preserves arrival order, that one rule makes the entire sort stable.

**Execution trace.**

```text
[(105,O1),(102,O2),(105,O3),(101,O4),(102,O5),(103,O6)]
merge [(102,O2)] + [(105,O3)] -> [(102,O2),(105,O3)]
merge [(105,O1)] + [(102,O2),(105,O3)] -> [(102,O2),(105,O1),(105,O3)]
merge [(102,O5)] + [(103,O6)] -> [(102,O5),(103,O6)]
merge [(101,O4)] + [(102,O5),(103,O6)] -> [(101,O4),(102,O5),(103,O6)]
final merge -> [(101,O4),(102,O2),(102,O5),(103,O6),(105,O1),(105,O3)]
```

The two `102` records remain `O2, O5`; the two `105` records remain `O1, O3`. This verifies stability.

**Recurrence and workload calculation.** `T(n) = 2T(n/2) + Θ(n)`, with `T(1)=Θ(1)`. By the Master Theorem, `T(n)=Θ(n log₂n)`. For `n=10,000,000`, `n log₂n ≈ 232,534,967`; the worst-case merge-comparison bound is about 232.5 million (precisely bounded by `n⌈log₂n⌉ - 2^⌈log₂n⌉ + 1`). Extra space is `Θ(n)` for the merge buffer plus a `Θ(log n)` call stack. If RAM cannot hold the data and buffer, use stable external merge sort: sort RAM-sized runs and perform a multiway disk merge; sequential I/O makes this practical.

## Part c Module 2 Quick Sort

**Partition trace.** A clear first-pivot trace on `[42,17,63,8,55,29]` uses pivot `42`. Scanning and swapping values `<=42` produces `[17,8,29,42,55,63]`, so `42` is placed at index 3, with all left values no larger and all right values larger. The executable implementation instead uses median-of-three to avoid systematic bad pivots.

**Why the current code freezes.** With a first-element pivot on a nearly sorted ascending list, the pivot is the minimum every time: partitions have sizes `0` and `n-1`. The recurrence is `T(n)=T(n-1)+Θ(n)=Θ(n²)`, requiring `100000×99999/2 = 4,999,950,000` comparisons in the fully ordered case. Balanced partitions follow `T(n)=2T(n/2)+Θ(n)=Θ(n log₂n)`, about `1,660,964` comparison-scale operations for 100,000 values.

**Improvement and trade-off.** Use a randomized or median-of-three pivot; this avoids the predictable first-pivot failure and normally produces balanced partitions. Add insertion-sort cutover for small partitions and recursion-depth protection (fall back to heap sort) for a production-grade introsort. Quick Sort remains in-place (`Θ(log n)` expected stack) and cache-friendly, but it is unstable. If stability is required, use Merge Sort; if changes are only a few known score updates, an indexed leaderboard or incremental maintenance may be superior.

## Part d Module 3 Binary Search

Binary Search is valid only because Module 1 produces nondecreasing timestamps. It discards half the candidate range after each comparison. To find the first duplicate, record a matching position and continue searching the left half instead of stopping.

The comparison recurrence is `T(n)=T(⌈n/2⌉)+1`, `T(1)=1`, hence `T(n)=Θ(log₂n)`. The maximum comparisons for 10,000,000 records is `⌈log₂(10,000,000+1)⌉ = 24`, versus up to 10,000,000 checks for linear search. The algorithm uses `Θ(1)` extra space iteratively. If the list is not sorted, either sort it first or maintain a timestamp index; searching unsorted data with binary search is incorrect.

## Part e Module 4 Strassen Method

For blocks of A and B, Strassen computes:

```text
M1=(A11+A22)(B11+B22)    M2=(A21+A22)B11
M3=A11(B12-B22)          M4=A22(B21-B11)
M5=(A11+A12)B22          M6=(A21-A11)(B11+B12)
M7=(A12-A22)(B21+B22)
C11=M1+M4-M5+M7; C12=M3+M5; C21=M2+M4; C22=M1+M3-M2+M6
```

For `A=[[1,7],[3,5]]`, `B=[[1,3],[7,5]]`: `M1=36, M2=8, M3=-2, M4=30, M5=40, M6=8, M7=24`. Reconstruction yields `C11=50, C12=38, C21=38, C22=34`, which agrees with conventional multiplication.

The recurrence is `T(n)=7T(n/2)+Θ(n²)`, so `T(n)=Θ(n^log₂7)=Θ(n^2.807)`. At `n=1024=2^10`, conventional multiplication uses `1024³=1,073,741,824` scalar multiplications; Strassen uses `7^10=282,475,249`, about 73.7% fewer multiplications. However, it performs many additions/subtractions, allocates temporary blocks, has worse numerical-error behavior, and may lose to optimized cache-blocked BLAS at modest sizes. Use a hybrid: pad non-power-of-two dimensions, recurse only above a benchmarked cutoff (often 64-256), and use conventional blocked multiplication below it.

## Part f Final Design and Justification

| Module | Final choice | Time | Extra memory | Main trade-off | Change the choice when |
|---|---|---|---|---|---|
| Orders | Stable external-capable Merge Sort | `Θ(n log n)` | `Θ(n)` RAM buffer; disk runs if needed | Predictable but not in-place | Memory is severely limited and audit stability is not required |
| Scores | Median-of-three introspective Quick Sort | Expected `Θ(n log n)`, bounded worst `Θ(n log n)` with fallback | `Θ(log n)` stack | Not stable; pivot overhead | Stable ties matter or only tiny deltas need updating |
| Lookup | Iterative first-occurrence Binary Search | `Θ(log n)` | `Θ(1)` | Requires maintained sorted order | The data is write-heavy; use a database/tree index |
| Recommendations | Hybrid Strassen plus blocked conventional base | `Θ(n^2.807)` asymptotically | `Θ(n²)` temporaries | More additions and implementation complexity | Benchmarks show optimized conventional multiplication wins |

The submitted programs execute the sample inputs, preserve the needed equal-timestamp ordering, return the first duplicate match, and cross-check the Strassen result against conventional multiplication. Reproducible captured outputs, source snapshots, datasets, and growth graphs are included with the modules.
