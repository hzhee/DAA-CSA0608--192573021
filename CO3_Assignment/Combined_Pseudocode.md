# CO3 Assignment Combined Pseudocode Q1 to Q7

## Q1 Max Min and Binary Search
`MAXMIN(A,l,r): if l=r return (A[l],A[l]); split at m; combine min(left.min,right.min), max(left.max,right.max).`  
`BINARY(A,x): compare x with middle; retain only the ordered half that can contain x; stop on match or empty range.`

## Q2 Merge Sort and Quick Sort
`MERGE_SORT: divide in halves, recursively sort, merge two ordered lists.`  
`QUICK_SORT: select pivot, partition into <= pivot and > pivot, recursively sort partitions.`

## Q3 Karatsuba
`Split x=a*10^m+b and y=c*10^m+d; compute ac, bd, (a+b)(c+d); return ac*10^(2m)+((a+b)(c+d)-ac-bd)*10^m+bd.`

## Q4 Strassen
`Split A and B into quadrants; compute M1..M7; reconstruct C11=M1+M4-M5+M7, C12=M3+M5, C21=M2+M4, C22=M1+M3-M2+M6.`

## Q5 Closest Pair
`Sort by x; solve left/right halves; let d be smaller distance; inspect only the y-sorted strip within d of boundary, up to next seven points per point.`

## Q6 Advanced D and C
`MEDIAN_OF_MEDIANS: group in fives, recursively select median of group medians, partition and recurse in relevant side.`  
`MITM_SUBSET_SUM: split values, enumerate both half subset sums, seek complement target-leftSum in right sums.`

## Q7 Day 4 Selected Challenge Maximum Contiguous Gain
`MAX_GAIN: divide period at midpoint; return best left gain, best right gain, or best crossing gain formed by maximum suffix plus maximum prefix.`
