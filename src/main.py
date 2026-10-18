
import json
from pathlib import Path

from validation import validate_product
from workflow import generate_tasks


# 将程序内部的英文字段转换为中文
FIELD_NAMES = {
    "sample_box_sachets": "试饮装小袋数量",
    "grams_per_sachet": "每袋重量（克）",
    "total_net_weight_g": "试饮装总净重（克）",
    "regular_pack_weight_g": "正装重量（克）"
}


def load_product_config():
    """读取产品配置文件。"""
    project_dir = Path(__file__).resolve().parent.parent
    config_path = project_dir / "config" / "product.json"

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_report(product, errors, warnings, tasks):
    """根据产品资料生成中文 Markdown 报告。"""
    lines = [
        "# AI 产品孵化工作流报告",
        "",
        "> 本报告由 Python 程序自动生成。",
        "",
        "## 一、项目基本信息",
        "",
        f"- 项目名称：{product.get('project_name', '未填写')}",
        f"- 产品类别：{product.get('product_category', '未填写')}",
        f"- 项目状态：{product.get('status', '未设置')}",
        "",
        "## 二、产品规格",
        ""
    ]

    facts = product.get("confirmed_facts", {})

    if facts:
        for key, value in facts.items():
            field_name = FIELD_NAMES.get(key, key)
            lines.append(f"- {field_name}：{value}")
    else:
        lines.append("- 暂无产品规格资料")

    # 产品资料检查结果
    lines.extend([
        "",
        "## 三、产品资料检查",
        ""
    ])

    if errors:
        lines.append("**检查结果：发现错误，需要修复。**")
        lines.append("")

        for error in errors:
            lines.append(f"- ❌ {error}")
    else:
        lines.append("**检查结果：未发现规则检查错误。**")

    if warnings:
        lines.append("")
        lines.append("### 提醒事项")
        lines.append("")

        for warning in warnings:
            lines.append(f"- ⚠️ {warning}")

    # 待确认事项
    lines.extend([
        "",
        "## 四、待确认事项",
        ""
    ])

    pending = product.get("pending_decisions", [])

    if pending:
        for item in pending:
            lines.append(f"- [ ] {item}")
    else:
        lines.append("- 暂无待确认事项")

    # 工作流任务
    lines.extend([
        "",
        "## 五、产品孵化任务清单",
        ""
    ])

    if tasks:
        for index, task in enumerate(tasks, start=1):
            lines.extend([
                f"### {index}. {task['name']}",
                "",
                f"- 任务说明：{task['description']}",
                f"- 当前状态：{task['status']}",
                ""
            ])
    else:
        lines.append("- 暂无任务")

    lines.extend([
        "",
        "## 六、后续建议",
        ""
    ])

    if errors:
        lines.append("1. 优先修复产品资料中的错误。")
        lines.append("2. 重新运行程序，检查错误是否消除。")
    elif pending:
        lines.append("1. 优先确认尚未确定的产品信息。")
        lines.append("2. 再按任务清单推进后续工作。")
    else:
        lines.append("1. 按任务清单逐项推进。")
        lines.append("2. 完成每个阶段后，及时更新产品资料。")

    lines.extend([
        "",
        "---",
        "",
        "报告由 AI 产品孵化工作流原型生成。",
        ""
    ])

    return "\n".join(lines)


def save_report(report):
    """将报告保存到 outputs 文件夹。"""
    project_dir = Path(__file__).resolve().parent.parent
    output_dir = project_dir / "outputs"

    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "product_workflow_report.md"

    with open(report_path, "w", encoding="utf-8") as file:
        file.write(report)

    return report_path


def main():
    product = load_product_config()

    print("=" * 45)
    print("AI 产品孵化工作流")
    print("=" * 45)

    print("项目名称：", product.get("project_name", "未填写"))
    print("产品类别：", product.get("product_category", "未填写"))

    # 第一步：检查产品资料
    errors, warnings = validate_product(product)

    print("\n【一、产品资料检查】")

    if errors:
        for error in errors:
            print("错误：", error)
    else:
        print("未发现规则检查错误。")

    if warnings:
        print("\n提醒事项：")
        for warning in warnings:
            print("-", warning)

    # 第二步：生成任务清单
    tasks = generate_tasks(product)

    print("\n【二、产品孵化任务】")

    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task['name']}")

    # 第三步：生成并保存报告
    report = build_report(product, errors, warnings, tasks)
    report_path = save_report(report)

    print("\n【三、报告生成结果】")
    print("报告位置：", report_path)

    if errors:
        print("注意：报告已生成，但产品资料存在错误，请及时修复。")
    else:
        print("报告生成成功。")


if __name__ == "__main__":
    main()
