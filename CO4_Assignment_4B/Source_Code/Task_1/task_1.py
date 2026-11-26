#!/usr/bin/env python3
"""Task 1: instrumented word-wrap dynamic programming."""

from dataclasses import dataclass
from typing import Sequence


@dataclass(frozen=True)
class Line:
    start: int
    end: int
    words: tuple[str, ...]
    characters: int
    unused: int
    penalty: int


def word_wrap(words: Sequence[str], width: int):
    """Return minimum penalty, line reconstruction, and all prefix candidates."""
    words = list(words)
    if width <= 0:
        raise ValueError("line width must be positive")
    if any(not word or len(word) > width for word in words):
        raise ValueError("words must be non-empty and each word must fit the line width")

    n = len(words)
    dp = [0] + [float("inf")] * n
    previous = [-1] * (n + 1)
    candidates = [[] for _ in range(n + 1)]

    # Prefix character totals make each candidate line width O(1) to calculate.
    prefix = [0]
    for word in words:
        prefix.append(prefix[-1] + len(word))

    for end in range(1, n + 1):
        for start in range(end - 1, -1, -1):
            letters = prefix[end] - prefix[start]
            gaps = end - start - 1
            used = letters + gaps
            if used > width:
                break
            unused = width - used
            line_penalty = 0 if end == n else unused * unused
            total = dp[start] + line_penalty
            candidates[end].append((start, used, unused, line_penalty, total))
            if total < dp[end]:
                dp[end] = total
                previous[end] = start

    lines = []
    end = n
    while end > 0:
        start = previous[end]
        if start < 0:
            raise ValueError("no feasible layout")
        selected = tuple(words[start:end])
        used = sum(map(len, selected)) + len(selected) - 1
        unused = width - used
        lines.append(Line(start, end, selected, used, unused, 0 if end == n else unused * unused))
        end = start
    lines.reverse()
    return int(dp[n]), lines, candidates, len(words)


def show_case(words, width, label):
    cost, lines, candidates, n = word_wrap(words, width)
    print(f"\n{label}: width={width}")
    print("DP state: dp[i] is the minimum penalty for laying out words 1..i.")
    print("i | feasible predecessor j | used | unused | line penalty | dp[j]+penalty")
    for i in range(1, n + 1):
        for start, used, unused, penalty, total in reversed(candidates[i]):
            print(f"{i:>1} | {start:>23} | {used:>4} | {unused:>6} | {penalty:>12} | {total:>14}")
        print(f"dp[{i}] = {min(c[4] for c in candidates[i])}; predecessor = {min(candidates[i], key=lambda c: c[4])[0]}")
    print("Line | words | used characters | unused spaces | line penalty")
    for index, line in enumerate(lines, 1):
        print(f"{index:>4} | {' '.join(line.words)} | {line.characters:>15} | {line.unused:>13} | {line.penalty:>12}")
    print("Minimum total penalty:", cost)
    print("DP states evaluated:", n, "prefix states; candidate transitions:", sum(map(len, candidates)))
    return cost, lines


def main():
    words = "dynamic programming makes documents readable for everyone".split()
    widths = (16, 22, 28)
    predictions = {
        16: "Predict: line 1 ends after 'dynamic'; widening to 22 should combine the first two words. I expect the total penalty to fall.",
        22: "Predict: line 1 remains 'dynamic programming'; the added width should reduce its slack penalty, so total penalty should fall from width 16.",
        28: "Predict: the first line can absorb 'makes'; I expect at least one later line boundary to move and the total penalty to fall from width 22.",
    }
    print("TASK 1 - WORD WRAP DOCUMENT LAYOUT")
    print("Input words:", " ".join(words))
    print("Penalty rule: a non-final line contributes (unused spaces)^2; the final line contributes 0.")
    results = {}
    for width in widths:
        print("\nBEFORE RUNNING WIDTH", width)
        print(predictions[width])
        results[width] = show_case(words, width, "MODIFIED-WIDTH RUN")
    print("\nPREDICTION CHECK")
    for width in widths:
        cost, lines = results[width]
        print(f"width {width}: observed {len(lines)} lines; penalty {cost}; first line: {' '.join(lines[0].words) if lines else '(empty)'}")

    exact = word_wrap(["four", "fits"], 4)[0]
    assert exact == 0
    assert word_wrap([], 10)[0] == 0
    try:
        word_wrap(["toolong"], 6)
    except ValueError as error:
        print("Boundary test: over-width word rejected:", error)
    else:
        raise AssertionError("over-width word must be rejected")
    try:
        word_wrap(["word"], 0)
    except ValueError as error:
        print("Boundary test: zero width rejected:", error)
    else:
        raise AssertionError("zero width must be rejected")
    print("Boundary rationale: a word one character wider than W can cause an infinite reconstruction or impossible line unless it is rejected explicitly.")
    print("Tests passed: three width runs, exact-fit words, empty input, over-width word, zero width.")


if __name__ == "__main__":
    main()
