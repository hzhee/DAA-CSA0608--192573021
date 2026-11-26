#!/usr/bin/env python3
"""Task 2: maximize profit by sequencing unit-time jobs before deadlines."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class Job:
    job_id: str
    deadline: int
    profit: int


def schedule_jobs(jobs: Iterable[Job]):
    jobs = list(jobs)
    if any(job.deadline < 1 or job.profit < 0 for job in jobs):
        raise ValueError("deadlines must be positive and profits non-negative")

    horizon = min(max((job.deadline for job in jobs), default=0), len(jobs))
    slots = [None] * (horizon + 1)
    decisions = []
    ordered = sorted(jobs, key=lambda job: (-job.profit, job.job_id))
    for job in ordered:
        checked = []
        placed = None
        for slot in range(min(job.deadline, horizon), 0, -1):
            checked.append(slot)
            if slots[slot] is None:
                slots[slot] = job
                placed = slot
                break
        decisions.append((job, checked, placed))
    total_profit = sum(job.profit for job in slots if job is not None)
    return slots, ordered, decisions, total_profit


def show_case(label, jobs):
    slots, ordered, decisions, total = schedule_jobs(jobs)
    print(f"\n{label}")
    print("Processing order:", " -> ".join(f"{job.job_id}(p={job.profit}, d={job.deadline})" for job in ordered))
    print("Job | checked slots | decision")
    for job, checked, placed in decisions:
        result = f"placed at {placed}" if placed is not None else "rejected; no free feasible slot"
        print(f"{job.job_id:>3} | {str(checked):>13} | {result}")
    schedule = [(slot, job.job_id) for slot, job in enumerate(slots) if slot and job is not None]
    print("Final schedule:", " ".join(f"slot {slot}={job_id}" for slot, job_id in schedule) or "empty")
    print("Total profit:", total)
    return slots, total


def main():
    given = [Job("A", 2, 80), Job("B", 1, 35), Job("C", 2, 60), Job("D", 3, 40), Job("E", 1, 25)]
    _, total = show_case("GIVEN INSTANCE", given)
    assert total == 180

    changed = [Job("A", 2, 80), Job("B", 1, 90), Job("C", 2, 60), Job("D", 3, 40), Job("E", 1, 25)]
    _, changed_total = show_case("CHALLENGE: change B profit from 35 to 90", changed)
    assert changed_total == 210
    assert schedule_jobs([])[3] == 0
    print("\nTests passed: supplied instance, modified-profit case, empty job set.")


if __name__ == "__main__":
    main()
