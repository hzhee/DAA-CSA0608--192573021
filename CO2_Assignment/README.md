# CO2 Assignment – Design and Analysis of Algorithms
## Brute-Force and Exhaustive-Search Techniques

| Field       | Details                                       |
|-------------|-----------------------------------------------|
| **Student** | HRUZHEECAYSHAN T K                            |
| **Reg No**  | 192573021                                     |
| **Subject** | Design and Analysis of Algorithms (DAA-CSA0608) |
| **Course Outcome** | CO2 – Apply Brute Force technique to solve sorting, searching, Closest-Pair and Convex-Hull problems |
| **Total Marks** | 50                                        |

---

## Repository Structure

```
CO2_Assignment/
│
├── Combined_Pseudocode_All_Questions.pdf   ← All 7 pseudocodes in ONE PDF
│
├── Q1_Sorting_Algorithms/
│   ├── Pseudocode/
│   │   ├── pseudocode.md          ← Selection, Bubble, Insertion Sort pseudocode
│   │   └── pseudocode.pdf         ← PDF version
│   ├── Implementation_Code/
│   │   └── sorting.py             ← Python implementation with comparison counting
│   └── Output_Screenshots/
│       └── output.txt             ← Execution output with all experimental results
│
├── Q2_Sequential_Search/
│   ├── Pseudocode/
│   │   ├── pseudocode.md
│   │   └── pseudocode.pdf
│   ├── Implementation_Code/
│   │   └── sequential_search.py
│   └── Output_Screenshots/
│       └── output.txt
│
├── Q3_Brute_Force_String_Matching/
│   ├── Pseudocode/
│   │   ├── pseudocode.md
│   │   └── pseudocode.pdf
│   ├── Implementation_Code/
│   │   └── string_matching.py
│   └── Output_Screenshots/
│       └── output.txt
│
├── Q4_Brute_Force_Closest_Pair/
│   ├── Pseudocode/
│   │   ├── pseudocode.md
│   │   └── pseudocode.pdf
│   ├── Implementation_Code/
│   │   └── closest_pair.py
│   └── Output_Screenshots/
│       └── output.txt
│
├── Q5_Brute_Force_Convex_Hull/
│   ├── Pseudocode/
│   │   ├── pseudocode.md
│   │   └── pseudocode.pdf
│   ├── Implementation_Code/
│   │   └── convex_hull.py
│   └── Output_Screenshots/
│       └── output.txt
│
├── Q6_Exhaustive_Search/
│   ├── Pseudocode/
│   │   ├── pseudocode.md
│   │   └── pseudocode.pdf
│   ├── Implementation_Code/
│   │   └── exhaustive_search.py
│   └── Output_Screenshots/
│       └── output.txt
│
├── Q7_Day4_Design_Challenge/
│   ├── Pseudocode/
│   │   ├── pseudocode.md
│   │   └── pseudocode.pdf
│   ├── Implementation_Code/
│   │   └── design_challenge.py
│   └── Output_Screenshots/
│       └── output.txt
│
└── Final_Report/
    └── CO2_Assignment_Report.md   ← Complete analysis report
```

---

## Questions Covered

| Q  | Topic                              | Marks | Algorithm(s)                              |
|----|------------------------------------|-------|-------------------------------------------|
| Q1 | Sorting Under Different Data Conditions | 6 | Selection Sort, Bubble Sort, Insertion Sort |
| Q2 | Sequential Search Engineering Choice   | 4 | Sequential Search                          |
| Q3 | Brute-Force String Matching            | 6 | Brute-Force String Matching               |
| Q4 | Brute-Force Closest Pair               | 6 | O(n²) Closest Pair                        |
| Q5 | Brute-Force Convex Hull                | 7 | O(n³) Cross-Product Hull                  |
| Q6 | Exhaustive Search (Knapsack)           | 8 | 2^n Subset Enumeration                    |
| Q7 | Day-4 Design Challenge                 | 13| Diagnose→Redesign→Validate (B&B)          |
| **Total** |                               | **50** |                                       |

---

## How to Run Each Implementation

```bash
# Q1 – Sorting Algorithms
python3 CO2_Assignment/Q1_Sorting_Algorithms/Implementation_Code/sorting.py

# Q2 – Sequential Search
python3 CO2_Assignment/Q2_Sequential_Search/Implementation_Code/sequential_search.py

# Q3 – String Matching
python3 CO2_Assignment/Q3_Brute_Force_String_Matching/Implementation_Code/string_matching.py

# Q4 – Closest Pair
python3 CO2_Assignment/Q4_Brute_Force_Closest_Pair/Implementation_Code/closest_pair.py

# Q5 – Convex Hull
python3 CO2_Assignment/Q5_Brute_Force_Convex_Hull/Implementation_Code/convex_hull.py

# Q6 – Exhaustive Search
python3 CO2_Assignment/Q6_Exhaustive_Search/Implementation_Code/exhaustive_search.py

# Q7 – Design Challenge
python3 CO2_Assignment/Q7_Day4_Design_Challenge/Implementation_Code/design_challenge.py
```

**Requirements:** Python 3.x (standard library only — no external packages needed)

---

## Key Results Summary

### Q1 – Sorting (n=1000)

| Algorithm      | Random     | Sorted | Reverse    | Nearly Sorted |
|----------------|-----------|--------|-----------|---------------|
| Selection Sort | 499,500   | 499,500| 499,500   | 499,500       |
| Bubble Sort    | ~498,713  | 999    | 499,500   | ~492,594      |
| Insertion Sort | ~245,031  | 999    | 499,500   | ~56,360       |

**Recommendation:** Insertion Sort — best for nearly-sorted emergency dispatch data.

### Q2 – Sequential Search Boundary
- Appropriate: n ≤ 500, search frequency ≤ 100/day
- Switch to binary search: n > 1,000 or frequency > 100/day

### Q3 – String Matching Cases
- Best case: n − m + 1 comparisons (O(n)) — first char mismatch
- Worst case: (n − m + 1) × m comparisons (O(mn)) — near-match pattern

### Q4 – Closest Pair Growth
- Comparisons = n(n-1)/2; doubles → 4× growth (confirmed O(n²))

### Q5 – Convex Hull Growth
- Edge checks ≈ n(n-1)(n-2); doubles → 8× growth (confirmed O(n³))

### Q6 – Exhaustive Search Deployment
- Maximum deployable n = **22 packages** within 5-second response time

### Q7 – Branch-and-Bound vs Exhaustive
- n=20: 1,048,576 exhaustive → ~5,000–50,000 B&B nodes (**>95% reduction**)
- Deployment boundary extended from n≤22 → n≤35+

---

## Evidence Checklist

- [x] Pseudocode for each question (Q1–Q7) — `.md` + `.pdf` per question
- [x] Combined single PDF with all pseudocodes
- [x] Source code for each question (Python)
- [x] Execution output for each question (`output.txt`)
- [x] Complexity analysis and mathematical derivations
- [x] Test datasets designed deliberately (best/worst/average cases)
- [x] Performance comparison tables
- [x] Experimental results with comparison counts
- [x] Observations and recommendations
- [x] Day-4 Design Challenge (Q7) — all 6 sections A–F
- [x] Final Report (`CO2_Assignment_Report.md`)
