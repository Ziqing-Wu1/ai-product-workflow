
import unittest

from src.skill_loader import list_skills, load_skill


class TestSkillLoader(unittest.TestCase):

    def test_list_skills(self):
        skills = list_skills()

        self.assertIn("market_research", skills)
        self.assertIn("prd", skills)
        self.assertIn("marketing", skills)

    def test_load_marketing_skill(self):
        content = load_skill("marketing")

        self.assertTrue(content.strip())
        self.assertIn("营销", content)

    def test_unknown_skill(self):
        with self.assertRaises(ValueError):
            load_skill("unknown_skill")


if __name__ == "__main__":
    unittest.main()
