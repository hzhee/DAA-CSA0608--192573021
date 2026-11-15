"""
Q3 – Brute-Force String Matching: Engineering the Behaviour
Student: HRUZHEECAYSHAN T K | Reg No: 192573021
CO2 Assignment – Design and Analysis of Algorithms
"""


def brute_force_string_match(text, pattern, find_all=False):
    """
    Brute-Force string matching with comparison counting.
    Returns list of match positions and total comparison count.
    """
    n = len(text)
    m = len(pattern)
    comparisons = 0
    matches = []

    for i in range(n - m + 1):
        j = 0
        while j < m:
            comparisons += 1
            if text[i + j] == pattern[j]:
                j += 1
            else:
                break
        if j == m:
            matches.append(i)
            if not find_all:
                return matches, comparisons

    return matches, comparisons


def run_experiments():
    print("=" * 70)
    print("Q3 – BRUTE-FORCE STRING MATCHING: ENGINEERING THE BEHAVIOUR")
    print("Student: HRUZHEECAYSHAN T K | Reg No: 192573021")
    print("=" * 70)

    # ── EXPERIMENT 1: Best Case ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 1: BEST CASE – 1 comparison per alignment")
    print("─" * 70)
    print("Design: First char of pattern never appears in text.")
    text    = "CCCCCCCCCCCCCCCCCCCC"  # n=20
    pattern = "BCCCC"                  # m=5, starts with 'B' (not in text)
    matches, comps = brute_force_string_match(text, pattern, find_all=True)
    theory = len(text) - len(pattern) + 1
    print(f"\n  Text:        '{text}'  (n={len(text)})")
    print(f"  Pattern:     '{pattern}'  (m={len(pattern)})")
    print(f"  Matches:     {matches if matches else 'None'}")
    print(f"  Comparisons: {comps}")
    print(f"  Theory:      n-m+1 = {theory}")
    print(f"  Verification: {'✓ EXACT MATCH' if comps == theory else f'Got {comps}'}")

    # ── EXPERIMENT 2: Worst Case ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 2: WORST CASE – m comparisons per alignment")
    print("─" * 70)
    print("Design: Nearly-matching text; mismatch only at last pattern char.")
    n, m = 20, 5
    text    = "A" * (n - 1) + "B"    # 'AAAAAAAAAAAAAAAAAAB'
    pattern = "A" * (m - 1) + "B"    # 'AAAAB'
    matches, comps = brute_force_string_match(text, pattern, find_all=True)
    alignments = n - m + 1
    theory_wc  = alignments * m
    print(f"\n  Text:        '{text}'  (n={n})")
    print(f"  Pattern:     '{pattern}'  (m={m})")
    print(f"  Alignments:  n-m+1 = {alignments}")
    print(f"  Matches:     {matches}")
    print(f"  Comparisons: {comps}")
    print(f"  Theory (worst): (n-m+1)*m = {alignments}*{m} = {alignments*m}")
    print(f"  Verification: {'✓ CLOSE' if abs(comps - theory_wc) <= alignments else f'Got {comps}'}")

    # ── EXPERIMENT 3: Average Case ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 3: AVERAGE CASE – Random text and pattern")
    print("─" * 70)
    import random
    random.seed(42)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    n, m = 100, 5
    text    = ''.join(random.choices(alphabet, k=n))
    pattern = ''.join(random.choices(alphabet, k=m))
    matches, comps = brute_force_string_match(text, pattern, find_all=True)
    alignments = n - m + 1
    theory_avg = alignments  # ~1 comp per alignment over large alphabet
    print(f"\n  Text (first 50): '{text[:50]}...'  (n={n})")
    print(f"  Pattern:          '{pattern}'  (m={m})")
    print(f"  Matches at:       {matches}")
    print(f"  Comparisons:      {comps}")
    print(f"  Theory (avg):     ~n-m+1 = {theory_avg} (1 comp/alignment avg)")

    # ── EXPERIMENT 4: Multiple occurrences ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 4: Multiple Occurrences")
    print("─" * 70)
    text    = "ABCABCABCABCABC"
    pattern = "ABC"
    matches, comps = brute_force_string_match(text, pattern, find_all=True)
    print(f"\n  Text:        '{text}'  (n={len(text)})")
    print(f"  Pattern:     '{pattern}'  (m={len(pattern)})")
    print(f"  Matches at:  {matches}  ({len(matches)} occurrences)")
    print(f"  Comparisons: {comps}")

    # ── EXPERIMENT 5: Comparison count vs text length ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 5: Comparison Count vs Text Length")
    print("─" * 70)
    print(f"\n  Pattern: 'AAAAB' (worst-case design)")
    print(f"\n  {'n':>8} | {'Best (1/align)':>16} | {'Worst (m/align)':>16} | {'Actual':>10}")
    print(f"  {'─'*8}─|─{'─'*16}─|─{'─'*16}─|─{'─'*10}")
    m = 5
    for n in [20, 50, 100, 200, 500]:
        text_bc = "C" * n
        patt_bc = "B" + "C" * (m - 1)
        _, bc = brute_force_string_match(text_bc, patt_bc)

        text_wc = "A" * (n - 1) + "B"
        patt_wc = "A" * (m - 1) + "B"
        _, wc = brute_force_string_match(text_wc, patt_wc)

        theory_bc = n - m + 1
        theory_wc = (n - m + 1) * m
        print(f"  {n:>8} | {theory_bc:>16} | {theory_wc:>16} | {wc:>10}")

    # ── EXPERIMENT 6: Security log simulation ──
    print("\n" + "─" * 70)
    print("EXPERIMENT 6: Security Log Screening Simulation")
    print("─" * 70)
    log_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 "
    signatures = ["ERROR404", "ROOTACCESS", "MALWARE"]
    log = ''.join(random.choices(log_chars, k=500))
    # Plant one signature
    plant_pos = 250
    log = log[:plant_pos] + "ERROR404" + log[plant_pos + 8:]

    print(f"\n  Log length: {len(log)} characters")
    print(f"\n  {'Signature':>12} | {'Found At':>10} | {'Comparisons':>12}")
    print(f"  {'─'*12}─|─{'─'*10}─|─{'─'*12}")
    for sig in signatures:
        matches, comps = brute_force_string_match(log, sig)
        pos = matches[0] if matches else -1
        print(f"  {sig:>12} | {pos:>10} | {comps:>12}")

    print("""
  COMPLEXITY ANALYSIS SUMMARY:
  ┌─────────────────┬────────────────────────────────────┐
  │ Case            │ Comparisons                        │
  ├─────────────────┼────────────────────────────────────┤
  │ Best            │ n - m + 1  ≈ O(n)                  │
  │ Average         │ ≈ n - m + 1  (large alphabet)      │
  │ Worst           │ (n-m+1) × m  ≈ O(mn)               │
  └─────────────────┴────────────────────────────────────┘

  OBSERVATION: The worst case (O(mn)) only occurs with deliberately
  constructed near-match patterns. For real ASCII logs (large alphabet),
  average case ≈ O(n) because mismatches occur on the first comparison.
  For high-frequency log screening, KMP (O(n+m)) would be preferred.
    """)


if __name__ == "__main__":
    run_experiments()
