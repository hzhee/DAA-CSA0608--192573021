```text
ALGORITHM WordWrap(Words, Width)
INPUT: ordered words Words[1..n], positive maximum line width Width
OUTPUT: minimum total penalty and a line partition
STATE: DP[i] is the minimum penalty for words 1 through i; DP[0] = 0
BEGIN
    VALIDATE that every word is non-empty and no word exceeds Width
    FOR i <- 1 TO n DO
        DP[i] <- INFINITY
        Used <- 0
        FOR j <- i DOWNTO 1 DO
            Used <- Used + LENGTH(Words[j])
            IF i > j THEN
                Used <- Used + 1
            END IF
            IF Used > Width THEN
                EXIT FOR
            END IF
            Unused <- Width - Used
            IF i = n THEN
                LinePenalty <- 0
            ELSE
                LinePenalty <- Unused * Unused
            END IF
            Candidate <- DP[j - 1] + LinePenalty
            IF Candidate < DP[i] THEN
                DP[i] <- Candidate
                Previous[i] <- j - 1
            END IF
        END FOR
    END FOR
    Reconstruct lines by following Previous from n to 0
    RETURN DP[n] and reconstructed lines
END
```
