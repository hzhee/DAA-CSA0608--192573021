#!/usr/bin/env python3
"""Task 6: energy-aware weighted interval scheduling (Day-4 challenge)."""

from bisect import bisect_right
from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Job:
    job_id: str
    start: int
    finish: int
    value: int


def weighted_schedule(jobs: Iterable[Job]):
    jobs = list(jobs)
    if any(job.start >= job.finish or job.value < 0 for job in jobs):
        raise ValueError("each job must have start < finish and non-negative value")

    ordered = sorted(jobs, key=lambda job: (job.finish, job.start, job.job_id))
    finishes = [job.finish for job in ordered]
    predecessor_count = [bisect_right(finishes, job.start, 0, i) for i, job in enumerate(ordered)]
    dp = [0] * (len(ordered) + 1)
    decisions = []
    for i, job in enumerate(ordered, start=1):
        p = predecessor_count[i - 1]
        take = job.value + dp[p]
        skip = dp[i - 1]
        dp[i] = max(take, skip)
        decisions.append((job, p, take, skip, dp[i]))

    selected = []
    i = len(ordered)
    while i > 0:
        job = ordered[i - 1]
        p = predecessor_count[i - 1]
        if job.value + dp[p] > dp[i - 1]:
            selected.append(job)
            i = p
        else:
            i -= 1
    selected.reverse()
    return ordered, predecessor_count, dp, decisions, selected


def greedy_by_value(jobs):
    selected = []
    for job in sorted(jobs, key=lambda item: (-item.value, item.finish, item.job_id)):
        if all(job.finish <= prior.start or prior.finish <= job.start for prior in selected):
            selected.append(job)
    return selected


def total_value(jobs):
    return sum(job.value for job in jobs)


def brute_force_optimum(jobs):
    best = 0
    for mask in range(1 << len(jobs)):
        chosen = [jobs[i] for i in range(len(jobs)) if mask & (1 << i)]
        ordered = sorted(chosen, key=lambda job: (job.start, job.finish, job.job_id))
        if all(left.finish <= right.start for left, right in zip(ordered, ordered[1:])):
            best = max(best, total_value(chosen))
    return best, 1 << len(jobs)


def show_case(label, jobs):
    ordered, predecessors, dp, decisions, selected = weighted_schedule(jobs)
    print(f"\n{label}")
    print("i | job (start-finish, value) | p(i) | previous job | take | skip | best")
    for i, (job, p, take, skip, best) in enumerate(decisions, start=1):
        pred_id = "0" if p == 0 else ordered[p - 1].job_id
        print(f"{i} | {job.job_id} ({job.start}-{job.finish}, {job.value}) | {p:>4} | {pred_id:>13} | {take:>4} | {skip:>4} | {best:>4}")
    print("DP:", dp)
    print("Selected:", ", ".join(job.job_id for job in selected) or "none", "->", total_value(selected))
    return selected


def main():
    supplied = [Job("J1", 1, 3, 20), Job("J2", 2, 5, 50), Job("J3", 4, 6, 30), Job("J4", 6, 8, 40),
                Job("J5", 5, 9, 60), Job("J6", 8, 10, 30), Job("J7", 9, 11, 50), Job("J8", 11, 13, 40)]
    chosen = show_case("GIVEN EIGHT-JOB INSTANCE", supplied)
    assert total_value(chosen) == 200
    assert [job.job_id for job in chosen] == ["J2", "J5", "J7", "J8"]

    adversarial = [Job("A", 1, 10, 100), Job("B", 1, 4, 60), Job("C", 4, 7, 60),
                   Job("D", 7, 10, 60), Job("E", 10, 12, 20)]
    dp_chosen = show_case("ADVERSARIAL: one high-value interval blocks a chain", adversarial)
    greedy_chosen = greedy_by_value(adversarial)
    print("Highest-value-first greedy:", ", ".join(job.job_id for job in greedy_chosen), "->", total_value(greedy_chosen))
    checked_optimum, subset_count = brute_force_optimum(adversarial)
    print(f"Independent exhaustive check: {checked_optimum} across {subset_count} subsets")
    assert total_value(dp_chosen) == 200
    assert [job.job_id for job in dp_chosen] == ["B", "C", "D", "E"]
    assert total_value(greedy_chosen) == 120
    assert checked_optimum == total_value(dp_chosen) == 200
    assert weighted_schedule([])[2] == [0]
    touching = [Job("X", 1, 2, 5), Job("Y", 2, 3, 6)]
    assert total_value(weighted_schedule(touching)[4]) == 11
    print("Tests passed: supplied schedule, adversarial set, empty set, touching endpoints.")


if __name__ == "__main__":
    main()
