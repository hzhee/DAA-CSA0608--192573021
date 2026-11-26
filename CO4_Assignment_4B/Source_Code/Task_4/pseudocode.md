```text
ALGORITHM AssemblyLineSchedule(a1, a2, t12, t21, entry1, entry2, exit1, exit2)
    F1[1] <- entry1 + a1[1]; F2[1] <- entry2 + a2[1]
    FOR station i <- 2 TO n DO
        Stay1 <- F1[i-1] + a1[i]
        TransferTo1 <- F2[i-1] + t21[i-1] + a1[i]
        F1[i] <- MIN(Stay1, TransferTo1); record predecessor line
        Stay2 <- F2[i-1] + a2[i]
        TransferTo2 <- F1[i-1] + t12[i-1] + a2[i]
        F2[i] <- MIN(Stay2, TransferTo2); record predecessor line
    END FOR
    Finish1 <- F1[n] + exit1; Finish2 <- F2[n] + exit2
    Choose the lower finish cost and backtrack predecessor lines
    RETURN minimum time, station-by-station route, transfer points
END
```
