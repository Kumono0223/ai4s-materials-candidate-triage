from pathlib import Path
import unittest


class WebDemoTests(unittest.TestCase):
    def test_demo_is_self_contained_and_truthful(self):
        html = (Path(__file__).parents[1] / "web" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Materials Candidate Triage", html)
        self.assertIn("不上传数据", html)
        self.assertIn("真实性能必须", html)
        self.assertNotIn("<script src=", html)
        self.assertNotIn("<link rel=\"stylesheet\"", html)


if __name__ == "__main__":
    unittest.main()
