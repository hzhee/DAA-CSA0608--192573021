# CO3 Assignment Combined Report

## Scope and Day 4 assumption
This repository addresses Q1 to Q7 from the supplied CO3 brief. The brief names a Day-4 challenge but provides no specific problem, so Q7 documents an original selected challenge: maximum contiguous sales-period gain. Replace it only if the faculty-issued Day-4 problem differs.

## Q1 Max Min and Binary Search
Max/Min divides the list until singleton base cases, then combines two pairs. `T(n)=2T(n/2)+2=Theta(n)`; the tournament method uses about `3n/2-2` comparisons, versus `2n-2` when max and min are found independently. Binary search eliminates half of an ordered list on each comparison: `T(n)=T(n/2)+1=Theta(log n)`. The code records successful and unsuccessful cases.

## Q2 Sorting decomposition
Merge Sort's fixed halves create a balanced tree and `Theta(n log n)` time with `Theta(n)` extra memory. Quick Sort's tree depends on the pivot: balanced partitions give `Theta(n log n)`; repeated first-pivot splits of `0:n-1` give `Theta(n^2)`. The output records partition sizes and recursion depth. Before choosing, inspect input size, stability requirement, memory budget, duplicate rate, existing order, and adversarial-input risk.

## Q3 Karatsuba
Karatsuba replaces four half-size multiplications with three: `T(n)=3T(n/2)+Theta(n)=Theta(n^log2(3))≈Theta(n^1.585)`. The experiment cross-checks the product with Python arithmetic and counts base multiplications. Its recursion and addition overhead means conventional multiplication can win on short inputs.

## Q4 Strassen
Strassen uses seven block products instead of eight: `T(n)=7T(n/2)+Theta(n^2)=Theta(n^2.807)`. The supplied sample yields `[[50,38],[38,34]]` by both algorithms. Padding to the next power of two, temporary matrices, additions, cache behavior, and numerical sensitivity can make conventional blocked multiplication preferable for small or irregular matrices.

## Q5 Closest Pair
The D and C method splits x-sorted points, computes each side, then examines the narrow boundary strip in y order. Its recurrence is `2T(n/2)+Theta(n)=Theta(n log n)`, rather than brute force `Theta(n^2)`. Geometry limits each strip point to at most seven subsequent candidates.

## Q6 Advanced investigations
Median of Medians selects a robust pivot from five-element groups and guarantees `Theta(n)` worst-case selection; random QuickSelect is expected linear but can have bad partitions. Meet in the Middle turns `2^n` subset enumeration into roughly `2^(n/2)` work and storage for each half, exposing a time-memory trade-off.

## Q7 Design challenge
Student A proposal: return the best gain and interval from left and right segments. Student B proposal: explicitly compute maximum suffix and prefix around a boundary. The joint design retains both, combines three candidates, and has `T(n)=2T(n/2)+Theta(n)=Theta(n log n)`. Baseline Kadane's algorithm is linear and would be preferable for this specific static problem; the challenge demonstrates when a valid D and C decomposition is not necessarily the best engineering choice.

## Contribution record
| Question | Student A primary contribution | Student B primary contribution | Shared work |
|---|---|---|---|
| Q1 | Max/Min decomposition and comparison math; Binary experiments | Binary elimination proof; Max/Min experiments | design, implementation, tests |
| Q2 | Quick Sort partition investigation | Merge Sort comparison and recursion analysis | pivot strategy and experiments |
| Q3 | Karatsuba derivation and recurrence | crossover experiment plan and overhead analysis | code and conclusion |
| Q4 | timing/engineering analysis | algebraic correctness and padding explanation | verification |
| Q5 | D and C decomposition | comparative evidence plan | code and strip reasoning |
| Q6 | Median of Medians | Meet in the Middle | cross-explanations |
| Q7 | recurrence validation | test/baseline validation | initial proposals and final design |

**Important:** replace the generic Student A / Student B labels with the two students' actual names and update this record to truthfully reflect work completed before submitting.
