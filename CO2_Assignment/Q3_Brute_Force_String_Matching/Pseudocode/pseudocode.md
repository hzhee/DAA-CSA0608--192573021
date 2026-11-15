# Q3 – Brute-Force String Matching Pseudocode
## Engineering the Behaviour of Brute-Force String Matching
### Student: HRUZHEECAYSHAN T K | Reg No: 192573021 | CO2 Assignment

---

## Algorithm: BruteForceStringMatch

```
ALGORITHM BruteForceStringMatch(text[0..n-1], pattern[0..m-1])
// Find first (or all) occurrence(s) of pattern in text
// Input : text of length n, pattern of length m
// Output: index of first match (-1 if not found), comparison count

  comparisons ← 0
  FOR i ← 0 TO n-m DO
      j ← 0
      WHILE j < m AND text[i+j] = pattern[j] DO
          comparisons ← comparisons + 1
          j ← j + 1
      END WHILE
      IF j < m THEN
          comparisons ← comparisons + 1   // The mismatching comparison
      END IF
      IF j = m THEN
          RETURN i, comparisons           // Match found at position i
      END IF
  END FOR
  RETURN -1, comparisons                  // Not found
```

**Step-by-Step Logic:**
1. Align the pattern starting at position `i = 0` in the text.
2. Compare `pattern[0]` with `text[i]`, then `pattern[1]` with `text[i+1]`, etc.
3. If ALL `m` characters match → pattern found at index `i`. Return and stop.
4. If a mismatch occurs at position `j` → shift pattern right by 1 (`i ← i+1`).
5. Repeat for all valid alignment positions: `i = 0` to `n-m`.
6. If no match found after all positions → return -1.

---

## Engineering the Three Cases

### BEST CASE — 1 comparison per alignment
**Design:** First character of pattern does NOT appear anywhere in text.

```
Text:    "CCCCCCCCCCCCCCC"   (n=15, all 'C')
Pattern: "BCCCC"             (m=5, starts with 'B')
```
- Each alignment fails on the FIRST character: 1 comparison per alignment.
- Total comparisons = n - m + 1 = 11 → **O(n)**

### WORST CASE — m comparisons per alignment
**Design:** Near-matching text; mismatch only on LAST pattern character.

```
Text:    "AAAAAAAAAAAAB"    (12 A's then B)
Pattern: "AAAAB"            (4 A's then B)
```
- Each alignment matches all but last character: m comparisons per shift.
- Total comparisons = (n-m+1) × m → **O(mn)**

### AVERAGE CASE — ~1 comparison per alignment
- Over a large alphabet (26+ chars), probability of matching first char ≈ 1/|Σ|
- Expected comparisons per alignment ≈ 1 + 1/(|Σ|-1) ≈ 1
- Total ≈ n - m + 1 → **O(n)**

---

## Complexity Summary

| Case         | Comparisons           | Big-O  |
|--------------|-----------------------|--------|
| Best Case    | n - m + 1             | O(n)   |
| Average Case | ≈ n - m + 1           | O(n)   |
| Worst Case   | (n - m + 1) × m       | O(mn)  |

**Key Observation:** The worst case only arises with deliberately crafted
near-matching patterns. Real-world text (ASCII logs) uses a large alphabet,
making mismatch on first character the typical outcome → Average ≈ O(n).

**Recommendation for security log screening:**
- For one-time scans: Brute-Force is acceptable (average O(n)).
- For high-frequency scanning of large logs: use **KMP** (O(n+m)) which
  preprocesses the pattern to avoid redundant comparisons.
