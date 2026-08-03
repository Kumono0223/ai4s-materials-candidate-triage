from pathlib import Path
import unittest


class WebDemoTests(unittest.TestCase):
    def setUp(self):
        self.html = (Path(__file__).parents[1] / "web" / "index.html").read_text(encoding="utf-8")

    def test_demo_is_self_contained_and_truthful(self):
        for marker in (
            "Materials Candidate Triage",
            "不上传数据",
            "真实性能",
            "composition-only",
            "供应风险关注表",
            "下载可复现 JSON",
        ):
            self.assertIn(marker, self.html)
        self.assertNotIn("<script src=", self.html)
        self.assertNotIn("<link rel=\"stylesheet\"", self.html)
        self.assertNotIn("fetch(", self.html)
        self.assertNotIn("XMLHttpRequest", self.html)

    def test_demo_exposes_same_method_and_parser_scope(self):
        self.assertIn("2026.08-composition-v2", self.html)
        self.assertIn("LiNi0.8Mn0.1Co0.1O2", self.html)
        self.assertIn("CuSO4·5H2O", self.html)
        self.assertIn("low-supply-risk", self.html)
        self.assertIn("normalised_mixing_entropy", self.html)


if __name__ == "__main__":
    unittest.main()
