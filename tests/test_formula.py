import json
import unittest

from src.materials_triage.formula import (
    METHODOLOGY_VERSION,
    analyze_formula,
    canonical_formula,
    parse_formula,
    rank_candidates,
)


class FormulaTests(unittest.TestCase):
    def test_parse_parentheses_decimals_and_hydrate(self):
        self.assertEqual(parse_formula("Ca3(PO4)2"), {"Ca": 3.0, "P": 2.0, "O": 8.0})
        self.assertEqual(
            parse_formula("LiNi0.8Mn0.1Co0.1O2"),
            {"Li": 1.0, "Ni": 0.8, "Mn": 0.1, "Co": 0.1, "O": 2.0},
        )
        self.assertEqual(parse_formula("CuSO4·5H2O"), {"Cu": 1.0, "S": 1.0, "O": 9.0, "H": 10.0})

    def test_mass_and_atomic_fraction_balance(self):
        result = analyze_formula("Fe2O3")
        self.assertAlmostEqual(sum(result["mass_fractions"].values()), 1.0, places=5)
        self.assertAlmostEqual(sum(result["atomic_fractions"].values()), 1.0, places=5)
        self.assertEqual(result["validation_level"], "composition-only")

    def test_score_is_explainable_and_objective_specific(self):
        battery = analyze_formula("LiFePO4", objective="battery")
        low_risk = analyze_formula("LiFePO4", objective="low-supply-risk")
        self.assertNotEqual(battery["triage_score"], low_risk["triage_score"])
        self.assertTrue(battery["score_breakdown"])
        self.assertIn("Li", battery["supply_watchlist_elements"])
        self.assertEqual(battery["methodology_version"], METHODOLOGY_VERSION)

    def test_safety_review_is_not_hidden(self):
        result = analyze_formula("PbO", objective="catalysis")
        self.assertEqual(result["safety_review_elements"], ["Pb"])
        self.assertIn("safety-review-required", result["flags"])

    def test_canonical_formula_is_deterministic(self):
        composition = parse_formula("LiFePO4")
        self.assertEqual(canonical_formula(composition), "FeLiO4P")

    def test_rank_report_is_stable_and_json_safe(self):
        report = rank_candidates(["Au", "LiFePO4", "Fe2O3"], objective="battery")
        self.assertEqual(report["candidate_count"], 3)
        self.assertEqual(report["candidates"][0]["formula"], "LiFePO4")
        json.dumps(report, ensure_ascii=False)

    def test_rejects_unknown_and_unbalanced_syntax(self):
        for formula in ("Xx2O", "Ca3(PO4", "Fe0O", "CuSO4·"):
            with self.subTest(formula=formula), self.assertRaises(ValueError):
                parse_formula(formula)


if __name__ == "__main__":
    unittest.main()
