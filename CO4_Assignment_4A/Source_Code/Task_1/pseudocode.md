# Task 1 - Algorithm Design Review

## Diagnosis

The proposal leaves several decisions undefined: package and capacity inputs are not described; “arrange packages” has no ordering criterion; “best” has no measurable meaning; feasibility is not tested against remaining capacity; partial packages are not handled; remaining capacity is not updated; and neither the stopping rule nor the returned selection/value is specified.

## Repaired pseudocode

```text
ALGORITHM FractionalKnapsack(Items, Capacity)
INPUT:
    Items: collection of (itemID, weight, value), with weight > 0 and value >= 0
    Capacity: non-negative maximum total weight
OUTPUT:
    Selected: item IDs and the fraction taken from each
    TotalValue: maximum value attainable at the given capacity
BEGIN
    SORT Items by decreasing value / weight ratio
        (break equal-ratio ties by increasing itemID)
    Remaining <- Capacity
    TotalValue <- 0
    Selected <- empty sequence

    FOR each Item in sorted Items DO
        IF Remaining = 0 THEN
            EXIT FOR
        END IF

        WeightTaken <- MIN(Item.weight, Remaining)
        FractionTaken <- WeightTaken / Item.weight
        ValueGained <- FractionTaken * Item.value
        APPEND (Item.itemID, FractionTaken) to Selected
        TotalValue <- TotalValue + ValueGained
        Remaining <- Remaining - WeightTaken
    END FOR

    RETURN (Selected, TotalValue)
END
```

## Design defence (73 words)

This is pseudocode because it names the inputs, outputs, state, decisions, loop, and return value in language-independent terms. It specifies the greedy rule as decreasing value per unit weight, defines the feasibility calculation, and shows how a final package may be taken fractionally. It does not rely on a programming-language syntax or data structure implementation. A programmer can translate each operation directly while choosing a suitable concrete representation for the item collection.
