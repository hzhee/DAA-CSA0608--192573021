# CO4 Assignment 4A — Greedy Algorithms and Dynamic Programming

**Student:** HRUZHEECAYSHAN T K  
**Register number:** 192573021  
**Course:** DAA-CSA0608

This directory contains the six solutions required by the CO4 Assignment 4A brief. Task 6 is the compulsory Day-4 Design Challenge. The language-independent pseudocode is kept separately from the Python implementation.

## Repository structure

```text
CO4_Assignment_4A/
├── Source_Code/
│   ├── Task_1/  Fractional knapsack
│   ├── Task_2/  Unit-time job sequencing with deadlines
│   ├── Task_3/  0/1 knapsack
│   ├── Task_4/  Word Break defect diagnosis and repair
│   ├── Task_5/  Dijkstra, Bellman-Ford, and Floyd-Warshall
│   └── Task_6/  Energy-aware weighted interval scheduling
├── Report/
│   └── CO4_Assignment_4A_Report.pdf
└── README.md
```

Each task folder has `task_N.py`, a language-independent `pseudocode.md`, and an `Output/` folder with captured program output (`output.txt`) and a PNG execution capture (`output.png`).

## Run the programs

Run from this directory with Python 3:

```bash
python3 Source_Code/Task_1/task_1.py
python3 Source_Code/Task_2/task_2.py
python3 Source_Code/Task_3/task_3.py
python3 Source_Code/Task_4/task_4.py
python3 Source_Code/Task_5/task_5.py
python3 Source_Code/Task_6/task_6.py
```

To execute all six programs and refresh their output files and PNG captures:

```bash
python3 Source_Code/generate_outputs.py
```

The implementations use only Python's standard library. The report contains each task's analysis, pseudocode, complete source, manual trace, calculations, tests, output captures, results, and complexity discussion.

All six programs were executed to generate the checked-in output files and screenshots. Task 6 also compares the dynamic-programming result against all 32 subsets of its adversarial five-job instance.
