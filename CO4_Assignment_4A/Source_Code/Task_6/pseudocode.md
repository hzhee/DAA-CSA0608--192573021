# Task 6 - Energy-Aware Weighted Interval Scheduling

State: after sorting by nondecreasing finish time, `DP[i]` is the maximum energy-saving value obtainable from the first `i` jobs. Let `p(i)` be the number of earlier jobs whose finish time is no later than job `i`'s start. The recurrence is `DP[0] = 0` and `DP[i] = MAX(DP[i-1], value[i] + DP[p(i)])`.

```text
ALGORITHM EnergyAwareSchedule(Jobs)
INPUT:
    Jobs[1..n]: records (jobID, start, finish, energySavingValue), start < finish
OUTPUT:
    SelectedJobs: a non-overlapping job sequence
    MaximumSaving: maximum total energy-saving value
BEGIN
    SORT Jobs by increasing finish time, then start time, then jobID
    FOR i <- 1 TO n DO
        p[i] <- number of jobs before i with finish time <= Jobs[i].start
    END FOR

    DP[0] <- 0
    FOR i <- 1 TO n DO
        Take <- Jobs[i].energySavingValue + DP[p[i]]
        Skip <- DP[i-1]
        DP[i] <- MAX(Take, Skip)
    END FOR

    SelectedJobs <- empty sequence
    i <- n
    WHILE i > 0 DO
        IF Jobs[i].energySavingValue + DP[p[i]] > DP[i-1] THEN
            PREPEND Jobs[i] to SelectedJobs
            i <- p[i]
        ELSE
            i <- i-1
        END IF
    END WHILE

    RETURN (SelectedJobs, DP[n])
END
```

Using `finish <= start` makes touching endpoints compatible. Predecessor counts can be found with binary search. The recurrence checks both compatible inclusion and exclusion, so a high-value job can be rejected when a compatible combination has a greater total.
