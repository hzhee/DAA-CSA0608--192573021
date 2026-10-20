"""Formula and boundary tests for the executable audit."""
import sys
import unittest
from pathlib import Path

# Permit execution from either Source_Code or the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from scalability_audit import m1_comparisons, m2_audits, s2_comparisons_upper_bound


class ScalabilityAuditTests(unittest.TestCase):
    def test_m1_pair_formula_matches_enumeration(self):
        for n in range(1, 20):
            enumerated = sum(1 for i in range(n - 1) for _j in range(i + 1, n))
            self.assertEqual(m1_comparisons(n), enumerated)

    def test_m2_formula_matches_the_loop(self):
        for n in range(1, 100):
            i, observed = 1, 0
            while i < n:
                observed += i
                i *= 2
            self.assertEqual(m2_audits(n), observed)

    def test_required_m2_verification_value(self):
        self.assertEqual(m2_audits(1_024), 1_023)

    def test_s2_power_of_two_closed_form(self):
        self.assertEqual(s2_comparisons_upper_bound(1), 1)
        self.assertEqual(s2_comparisons_upper_bound(1_024), 11)


if __name__ == "__main__":
    unittest.main(verbosity=2)
