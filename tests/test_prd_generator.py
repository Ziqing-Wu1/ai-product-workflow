
import unittest

from src.prd_generator import generate_prd


class TestPrdGenerator(unittest.TestCase):

    def setUp(self):
        """准备一份测试用产品资料。"""
        self.product = {
            "project_name": "测试茶产品",
            "product_category": "tea",
            "status": "draft",
            "confirmed_facts": {
                "sample_box_sachets": 9,
                "grams_per_sachet": 8,
                "total_net_weight_g": 72
            },
            "pending_decisions": [
                "试饮装售价",
                "品牌名称"
            ]
        }

    def test_prd_contains_project_name(self):
        """检查 PRD 是否包含项目名称。"""
        content = generate_prd(self.product)

        self.assertIn("测试茶产品", content)

    def test_prd_contains_confirmed_facts(self):
        """检查已确认的产品资料是否写入 PRD。"""
        content = generate_prd(self.product)

        self.assertIn("sample_box_sachets", content)
        self.assertIn("72", content)

    def test_prd_contains_pending_decisions(self):
        """检查待确认事项是否写入 PRD。"""
        content = generate_prd(self.product)

        self.assertIn("试饮装售价", content)
        self.assertIn("品牌名称", content)

    def test_prd_marks_unconfirmed_content(self):
        """检查未确认的信息是否明确标记。"""
        content = generate_prd(self.product)

        self.assertIn("待调研", content)
        self.assertIn("待验证", content)

    def test_prd_contains_acceptance_criteria(self):
        """检查 PRD 是否包含验收标准。"""
        content = generate_prd(self.product)

        self.assertIn("验收标准", content)


if __name__ == "__main__":
    unittest.main()
