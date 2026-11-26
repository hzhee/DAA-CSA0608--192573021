# Task 2 - Job Sequencing with Deadlines

```text
ALGORITHM SequenceJobs(Jobs)
INPUT:
    Jobs: records (jobID, deadline, profit), each requiring one time slot
OUTPUT:
    Schedule: the job assigned to each occupied time slot
    TotalProfit: sum of profits in Schedule
BEGIN
    n <- number of Jobs
    H <- MIN(n, maximum deadline in Jobs), or 0 if Jobs is empty
    CREATE Slots[1..H], initially EMPTY
    TotalProfit <- 0
    SORT Jobs by decreasing profit; break ties by increasing jobID

    FOR each Job in sorted Jobs DO
        LatestSlot <- MIN(Job.deadline, H)
        FOR Slot <- LatestSlot DOWNTO 1 DO
            IF Slots[Slot] = EMPTY THEN
                Slots[Slot] <- Job
                TotalProfit <- TotalProfit + Job.profit
                EXIT FOR
            END IF
        END FOR
    END FOR

    RETURN (Slots, TotalProfit)
END
```

Greedy rule: consider higher-profit jobs first and place each in the latest free slot that does not exceed its deadline. The latest feasible slot preserves earlier slots for jobs that have fewer scheduling choices.
