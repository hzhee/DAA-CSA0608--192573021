# CO3 Assessment KartIQ Divide and Conquer Case Study

This directory is a complete submission for the CSA06 CO3 case study. It is deliberately separate from the existing CO1 and CO2 material.

## Contents

- `Module_1_Merge_Sort` - stable consolidation program, pseudocode reference, report evidence.
- `Module_2_Quick_Sort` - median-of-three Quick Sort program and partition evidence.
- `Module_3_Binary_Search` - first-occurrence timestamp lookup.
- `Module_4_Strassen_Matrix_Multiplication` - Strassen program with conventional verification.
- `Combined_Pseudocode.md` - all four algorithms in one hand-in file.
- `Combined_Case_Study_Report.md` - complete responses to parts a through f.
- `Final_Design_and_Analysis/Graphs` - generated complexity comparison charts.
- `Supporting_Files/generate_artifacts.py` - reproduces outputs, source snapshots and charts.

## Run

Run any module directly with Python 3, for example:

```bash
python3 Module_1_Merge_Sort/Source_Code/merge_sort.py
python3 Module_2_Quick_Sort/Source_Code/quick_sort.py
python3 Module_3_Binary_Search/Source_Code/binary_search.py
python3 Module_4_Strassen_Matrix_Multiplication/Source_Code/strassen.py
```

To regenerate captured evidence and graphs, install `matplotlib` and `pygments`, then run:

```bash
python3 Supporting_Files/generate_artifacts.py
```

## Input datasets and tests

All prescribed sample datasets are embedded in the runnable programs so that each demonstration is self-contained. The generated output captures form the execution evidence. Source snapshots are created as PNGs for report submission.
