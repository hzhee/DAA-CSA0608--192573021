import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from student_search import (
    build_hash_index,
    build_sorted_index,
    hash_search,
    linear_search,
    make_records,
    recursive_binary_search,
)


class StudentSearchTests(unittest.TestCase):
    def setUp(self):
        self.records = make_records(101)
        self.target = self.records[50].registration_number
        self.missing = 99_999_999

    def test_all_algorithms_find_the_same_student(self):
        sorted_index = build_sorted_index(self.records)
        hash_index = build_hash_index(self.records)
        results = [
            linear_search(self.records, self.target),
            recursive_binary_search(sorted_index, self.target),
            hash_search(hash_index, self.target),
        ]
        self.assertTrue(all(result.student is not None for result in results))
        self.assertEqual({result.student.registration_number for result in results}, {self.target})

    def test_all_algorithms_report_absence(self):
        self.assertIsNone(linear_search(self.records, self.missing).student)
        self.assertIsNone(recursive_binary_search(build_sorted_index(self.records), self.missing).student)
        self.assertIsNone(hash_search(build_hash_index(self.records), self.missing).student)

    def test_linear_comparisons_reflect_position(self):
        self.assertEqual(linear_search(self.records, self.records[0].registration_number).comparisons, 1)
        self.assertEqual(linear_search(self.records, self.records[-1].registration_number).comparisons, 101)


if __name__ == "__main__":
    unittest.main(verbosity=2)
