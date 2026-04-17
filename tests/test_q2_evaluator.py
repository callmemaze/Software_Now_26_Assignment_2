import unittest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../src")))
import evaluator  # rename if needed


class TestEvaluator(unittest.TestCase):

    def run_eval(self, expr):
        with open("temp_input.txt", "w", encoding="utf-8") as f:
            f.write(expr + "\n")

        return evaluator.evaluate_file("temp_input.txt")[0]

    # ---------------- BASIC OPERATIONS ----------------
    def test_addition(self):
        r = self.run_eval("3 + 5")
        self.assertEqual(r["result"], 8)

    def test_precedence(self):
        r = self.run_eval("2 + 3 * 4")
        self.assertEqual(r["result"], 14)

    # ---------------- BRACKETS ----------------
    def test_parentheses(self):
        r = self.run_eval("(10 - 2) * 3")
        self.assertEqual(r["result"], 24)

    # ---------------- UNARY ----------------
    def test_unary(self):
        r = self.run_eval("-(3 + 4)")
        self.assertEqual(r["result"], -7)

    def test_double_neg(self):
        r = self.run_eval("--5")
        self.assertEqual(r["result"], 5)

    # ---------------- IMPLICIT MULTIPLICATION ----------------
    def test_implicit_mul(self):
        r = self.run_eval("2(3+4)")
        self.assertEqual(r["result"], 14)

    # ---------------- DIVISION ----------------
    def test_division(self):
        r = self.run_eval("10 / 2")
        self.assertEqual(r["result"], 5)

    def test_div_zero(self):
        r = self.run_eval("1 / 0")
        self.assertIn("ERROR", str(r["result"]))

    # ---------------- INVALID INPUT ----------------
    def test_invalid(self):
        r = self.run_eval("3 @ 5")
        self.assertIn("ERROR", str(r["tree"]))


if __name__ == "__main__":
    unittest.main()