```text
ALGORITHM HeldKarp(Cost, Hub)
    Stops <- every location except Hub
    DP[{j}, j] <- Cost[Hub,j] for each stop j
    FOR subset size s <- 2 TO number of Stops DO
        FOR each subset S of size s DO
            FOR each j in S DO
                DP[S,j] <- MIN over i in S-{j} of (DP[S-{j},i] + Cost[i,j])
                Parent[S,j] <- minimizing predecessor i
            END FOR
        END FOR
    END FOR
    Choose last j minimizing DP[AllStops,j] + Cost[j,Hub]
    Follow Parent pointers backward and add Hub at both ends
    RETURN optimal tour and cost
END
```
State meaning: `DP[S,j]` is the least cost from the hub, visiting exactly the set `S`, and ending at location `j`.
