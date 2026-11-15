# Module 2 Quick Sort Evidence

The legacy first pivot has `Θ(n²)` behavior on nearly sorted scores: approximately 4,999,950,000 comparisons for 100,000 ascending values. Median-of-three selection reduces the predictable failure risk; introspective fallback gives a hard `Θ(n log n)` bound. See the combined report for partition trace and trade-offs.
