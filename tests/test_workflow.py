
import unittest

from src.validation import validate_product
from src.workflow import generate_tasks


def make_test_product():
    """创建测试用的产品资料，避免修改真实配置文件。"""
    return {
        "project_name": "测试茶产品",
        "product_category": "tea",
        "confirmed_facts": {
            "sample_box_sachets": 9,
            "grams_per_sachet": 8,
            "total_net_weight_g": 72,
            "regular_pack_weight_g": 250
        },
        "pending_decisions": []
    }


class TestProductValidation(unittest.TestCase):

    def test_valid_product_has_no_errors(self):
        """正常的产品规格应该通过检查。"""
        product = make_test_product()

        errors, warnings = validate_product(product)

        self.assertEqual(errors, [])

    def test_wrong_total_weight_is_detected(self):
        """总重量不正确时，应该发现错误。"""
        product = make_test_product()
        product["confirmed_facts"]["total_net_weight_g"] = 70

        errors, warnings = validate_product(product)

        self.assertTrue(len(errors) > 0)
        self.assertTrue(any("重量不一致" in error for error in errors))

    def test_missing_project_name_is_detected(self):
        """项目名称为空时，应该发现错误。"""
        product = make_test_product()
        product["project_name"] = ""

        errors, warnings = validate_product(product)

        self.assertTrue(
            any("项目名称不能为空" in error for error in errors)
        )

    def test_pending_decisions_generate_warning(self):
        """有待确认事项时，应该生成提醒。"""
        product = make_test_product()
        product["pending_decisions"] = ["试饮装售价"]

        errors, warnings = validate_product(product)

        self.assertTrue(
            any("1 项信息待确认" in warning for warning in warnings)
        )


class TestWorkflow(unittest.TestCase):

    def test_tea_product_has_tea_specific_task(self):
        """茶产品应该包含茶产品专属任务。"""
        product = make_test_product()

        tasks = generate_tasks(product)
        task_names = [task["name"] for task in tasks]

        self.assertIn("茶产品规格与合规检查", task_names)

    def test_car_accessory_has_car_specific_task(self):
        """汽车用品应该包含汽车用品专属任务。"""
        product = make_test_product()
        product["product_category"] = "car_accessory"

        tasks = generate_tasks(product)
        task_names = [task["name"] for task in tasks]

        self.assertIn("汽车用品安全检查", task_names)
        self.assertNotIn("茶产品规格与合规检查", task_names)


if __name__ == "__main__":
    unittest.main()
