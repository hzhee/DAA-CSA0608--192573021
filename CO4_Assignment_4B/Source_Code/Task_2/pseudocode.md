```text
ALGORITHM FractionalKnapsack(Items, Capacity)
    SORT items by decreasing value/weight ratio
    Remaining <- Capacity; Total <- 0; Selected <- empty
    FOR each Item in sorted order DO
        Amount <- MIN(Item.weight, Remaining)
        Fraction <- Amount / Item.weight
        APPEND (Item.ID, Fraction) to Selected
        Total <- Total + Fraction * Item.value
        Remaining <- Remaining - Amount
        IF Remaining = 0 THEN EXIT FOR
    END FOR
    RETURN Selected, Total
END

ALGORITHM ZeroOneKnapsack(Items[1..n], Capacity)
    DP[0..n, 0..Capacity] <- 0
    FOR i <- 1 TO n DO
        FOR w <- 0 TO Capacity DO
            DP[i,w] <- DP[i-1,w]
            IF Items[i].weight <= w THEN
                DP[i,w] <- MAX(DP[i,w], Items[i].value + DP[i-1,w-Items[i].weight])
            END IF
        END FOR
    END FOR
    Backtrack from (n, Capacity); include item i when DP[i,w] > DP[i-1,w]
    RETURN DP[n,Capacity], selected item IDs
END
```
