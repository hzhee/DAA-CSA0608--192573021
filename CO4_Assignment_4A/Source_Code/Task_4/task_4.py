#!/usr/bin/env python3
"""Task 4: expose and repair the missing-prefix condition in Word Break."""


def faulty_word_break_states(text, dictionary):
    dp = [False] * (len(text) + 1)
    dp[0] = True
    for end in range(1, len(text) + 1):
        for start in range(end):
            if text[start:end] in dictionary:
                dp[end] = True
                break
    return dp


def word_break(text, dictionary):
    dp = [False] * (len(text) + 1)
    parent = [None] * (len(text) + 1)
    dp[0] = True
    trace = []
    for end in range(1, len(text) + 1):
        for start in range(end):
            word = text[start:end]
            accepted = dp[start] and word in dictionary
            trace.append((end, start, word, dp[start], word in dictionary, accepted))
            if accepted:
                dp[end] = True
                parent[end] = start
                break

    if not dp[-1]:
        return False, [], dp, trace
    words = []
    end = len(text)
    while end > 0:
        start = parent[end]
        words.append(text[start:end])
        end = start
    words.reverse()
    return True, words, dp, trace


def main():
    text, dictionary = "ab", {"b"}
    faulty = faulty_word_break_states(text, dictionary)
    possible, words, corrected, trace = word_break(text, dictionary)
    print("TASK 4 - WORDBREAK DEFECT AND REPAIR")
    print("Failing input: text='ab'; dictionary={'b'}")
    print("end | start | substring | DP[start] | in dictionary | accepted after repair")
    for end, start, substring, prefix_ok, in_dictionary, accepted in trace:
        print(f"{end:>3} | {start:>5} | {substring!r:>9} | {str(prefix_ok):>9} | {str(in_dictionary):>13} | {accepted}")
    print("Faulty states:", faulty, "->", faulty[-1])
    print("Correct states:", corrected, "->", possible)
    print("The faulty rule marks DP[2] true from 'b' although DP[1] is false.")

    reg_text, reg_dictionary = "cat", {"cat"}
    reg_possible, reg_words, reg_dp, _ = word_break(reg_text, reg_dictionary)
    print(f"Regression: text='cat'; dictionary={{'cat'}} -> {reg_possible}, words={reg_words}, DP={reg_dp}")
    assert faulty[-1] is True and possible is False
    assert reg_possible is True and reg_words == ["cat"]
    assert word_break("", set())[0] is True
    print("Tests passed: false-positive counterexample, valid whole word, empty string.")


if __name__ == "__main__":
    main()
