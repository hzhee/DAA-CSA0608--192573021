"""Student-registration search strategies used throughout the CO1 assignment."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Student:
    registration_number: int
    name: str


@dataclass(frozen=True)
class SearchResult:
    student: Optional[Student]
    comparisons: int


def make_records(size: int) -> list[Student]:
    """Create a deterministic, deliberately unsorted dataset of unique records."""
    if size < 1:
        raise ValueError("size must be positive")
    # A modular permutation produces unique IDs, while avoiding a pre-sorted input.
    return [Student((i * 37) % size + 10_000_000, f"Student {i:07d}") for i in range(size)]


def linear_search(records: list[Student], target: int) -> SearchResult:
    """Iterative sequential scan. One registration-number equality test per record."""
    for comparisons, student in enumerate(records, start=1):
        if student.registration_number == target:
            return SearchResult(student, comparisons)
    return SearchResult(None, len(records))


def build_sorted_index(records: list[Student]) -> list[Student]:
    """Preprocess records as a sorted registration-number index."""
    return sorted(records, key=lambda student: student.registration_number)


def recursive_binary_search(index: list[Student], target: int) -> SearchResult:
    """Recursive binary search over the sorted index."""
    def visit(low: int, high: int, comparisons: int) -> SearchResult:
        if low > high:
            return SearchResult(None, comparisons)
        middle = (low + high) // 2
        comparisons += 1
        value = index[middle].registration_number
        if value == target:
            return SearchResult(index[middle], comparisons)
        if target < value:
            return visit(low, middle - 1, comparisons)
        return visit(middle + 1, high, comparisons)

    return visit(0, len(index) - 1, 0)


def build_hash_index(records: list[Student]) -> dict[int, Student]:
    """Preprocess records into a direct registration-number hash index."""
    return {student.registration_number: student for student in records}


def hash_search(index: dict[int, Student], target: int) -> SearchResult:
    """Expected constant-time lookup; count one logical dictionary lookup."""
    return SearchResult(index.get(target), 1)
