# Task 4 - Word Break Defect and Repair

## Exact defect

The decision checks only whether `Text[j..i-1]` is in the dictionary. It also must require `DP[j] = TRUE`, which establishes that the prefix before the candidate word can already be segmented.

## Minimal repair

```text
ALGORITHM WordBreak(Text, Dictionary)
INPUT:
    Text: string of length n
    Dictionary: collection of valid words
OUTPUT:
    TRUE if Text can be completely segmented; otherwise FALSE
BEGIN
    DP[0] <- TRUE
    FOR i <- 1 TO n DO
        DP[i] <- FALSE
        FOR j <- 0 TO i-1 DO
            IF DP[j] = TRUE AND substring(Text, j, i) is in Dictionary THEN
                DP[i] <- TRUE
                BREAK
            END IF
        END FOR
    END FOR
    RETURN DP[n]
END
```

Only the condition is repaired: `DP[j] = TRUE AND ...`. A failing case is text `ab` with dictionary `{b}`; the faulty version marks position 2 true using `b` even though prefix `a` is not segmentable. A regression case is text `cat` with dictionary `{cat}`, which remains true from `DP[0]`.
