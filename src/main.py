
import json
from pathlib import Path

from validation import validate_product
from workflow import generate_tasks


def load_product_config():
    project_dir = Path(__file__).resolve().parent.parent
    config_path = project_dir / "config" / "product.json"

    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_report(product, tasks, warnings):
    project_dir = Path(__file__).resolve().parent.parent
    output_dir = project_dir / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    report_path = output_dir / "product_workflow_report.md"

    lines = [
        "# AI 产品孵化工作流报告",
        "",
        f"## 项目名称：{product['project_name']}",
        "",
        f"- 产品类别：{product['product_category']}",
        "",
        "## 一、产品规格",
        ""
    ]

    facts = product.get("confirmed_facts", {})

    for key, value in facts.items():
        lines.append(f"- {key}: {value}")

    lines.extend(["", "## 二、待确认事项", ""])

    pending = product.get("pending_decisions", [])

    if pending:
        for item in pending:
            lines.append(f"- [ ] {item}")
    else:
        lines.append("- 暂无")

    lines.extend(["", "## 三、检查提醒", ""])

    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- 暂无")

    lines.extend(["", "## 四、产品孵化任务清单", ""])

    for index, task in enumerate(tasks, start=1):
        lines.append(f"### {index}. {task['name']}")
        lines.append("")
        lines.append(f"- 任务说明：{task['description']}")
        lines.append(f"- 当前状态：{task['status']}")
        lines.append("")

    with open(report_path, "w", encoding="utf-8") as file:
        file.write("\n".join(lines))

    return report_path


def main():
    product = load_product_config()

    print("=" * 45)
    print("AI 产品孵化工作流")
    print("=" * 45)
    print("项目名称：", product["project_name"])
    print("产品类别：", product["product_category"])

    errors, warnings = validate_product(product)

    print("\n【一、产品资料检查】")

    if errors:
        for error in errors:
            print("错误：", error)

        print("\n请先修复错误，暂不生成报告。")
        return

    print("规格检查通过，未发现错误。")

    if warnings:
        print("\n【待处理提醒】")
        for warning in warnings:
            print("-", warning)

    tasks = generate_tasks(product)

    print("\n【二、任务清单】")

    for index, task in enumerate(tasks, start=1):
        print(f"{index}. {task['name']}")

    report_path = save_report(product, tasks, warnings)

    print("\n报告已生成！")
    print("保存位置：", report_path)


if __name__ == "__main__":
    main()
