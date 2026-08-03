import json
import unittest

from src.materials_triage.formula import analyze_formula, parse_formula


class FormulaTests(unittest.TestCase):
    def test_parse_and_mass_balance(self):
        composition = parse_formula("Fe2O3")
        self.assertEqual(composition, {"Fe": 2.0, "O": 3.0})
        result = analyze_formula("Fe2O3")
        self.assertAlmostEqual(sum(result["mass_fractions"].values()), 1.0, places=5)

    def test_tags_and_json(self):
        result = analyze_formula("LiFePO4")
        self.assertIn("lithium-containing", result["tags"])
        json.dumps(result, ensure_ascii=False)

    def test_reject_unknown_element(self):
        with self.assertRaises(ValueError):
            parse_formula("Xx2O")


if __name__ == "__main__":
    unittest.main()

