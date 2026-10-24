# Experimental method

The benchmark is fully reproducible with Python 3 and no third-party dependencies. It uses deterministic, unique, deliberately unsorted registration numbers. At each input size (1,000, 10,000, 100,000, and 1,000,000), it executes 24 queries: 12 present records evenly distributed across the data and 12 absent values. `time.perf_counter_ns()` measures one search at a time; reported values are the per-query arithmetic mean in microseconds. Preprocessing is measured separately once per dataset.

The logical comparison counter increments once per registration-number decision in linear and binary search. A hash lookup is reported as one logical lookup; actual collisions are implementation-dependent, so its expected and worst-case bounds are stated separately in the analysis.
