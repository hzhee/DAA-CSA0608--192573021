# Task 3 - 0/1 Knapsack

State: `DP[i,w]` is the maximum value obtainable using only the first `i` items with total weight at most `w`.

For item `i` with weight `weight[i]` and value `value[i]`:

- If `weight[i] > w`, the item cannot fit: `DP[i,w] = DP[i-1,w]`.
- Otherwise choose the better of excluding it and including it once: `DP[i,w] = MAX(DP[i-1,w], value[i] + DP[i-1,w-weight[i]])`.
- Base states: `DP[0,w] = 0` for every capacity, and `DP[i,0] = 0` for every item count.

```text
ALGORITHM ZeroOneKnapsack(Items, Capacity)
INPUT:
    Items[1..n]: records (itemID, weight, value), with positive weight
    Capacity: non-negative maximum weight
OUTPUT:
    MaximumValue and SelectedItems
BEGIN
    CREATE DP[0..n, 0..Capacity]
    FOR w <- 0 TO Capacity DO
        DP[0,w] <- 0
    END FOR

    FOR i <- 1 TO n DO
        DP[i,0] <- 0
        FOR w <- 1 TO Capacity DO
            DP[i,w] <- DP[i-1,w]
            IF weight[i] <= w THEN
                IncludeValue <- value[i] + DP[i-1, w-weight[i]]
                DP[i,w] <- MAX(DP[i,w], IncludeValue)
            END IF
        END FOR
    END FOR

    SelectedItems <- empty sequence
    Remaining <- Capacity
    FOR i <- n DOWNTO 1 DO
        IF DP[i,Remaining] > DP[i-1,Remaining] THEN
            PREPEND itemID[i] to SelectedItems
            Remaining <- Remaining - weight[i]
        END IF
    END FOR

    RETURN (DP[n,Capacity], SelectedItems)
END
```

Each row depends only on the preceding row. Processing `i` in increasing order ensures those subproblem values exist before use. During reconstruction, a strict improvement over the previous row means item `i` was included; otherwise it was excluded.
