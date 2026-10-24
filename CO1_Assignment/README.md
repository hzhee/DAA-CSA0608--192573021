# CO1 Assignment - Student Record Search Strategy

This submission designs, implements, tests, and compares three ways to locate a student by unique registration number:

1. Iterative linear search.
2. Recursive binary search over a sorted index.
3. Hash-index lookup.

## Run

```bash
cd Task_8_Implementation_Testing/Source_Code
python3 -m unittest -v test_student_search.py
python3 run_experiments.py
```

The experiment deterministically generates equivalent unsorted datasets of 1,000, 10,000, 100,000, and 1,000,000 records. It writes reproducible measurements to `Task_9_Experimental_Performance/performance_results.csv` and updates the evidence graphics in `Report/`.

## Structure

Each `Task_*` folder maps directly to an assessed task. `Report/Analysis/Complete_Report.md` is the complete technical report; `Report/Tables_and_Graphs/` contains the generated comparison chart and `Report/*_Screenshots/` contains generated source/output evidence.
