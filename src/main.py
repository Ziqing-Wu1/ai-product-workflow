
import json
from pathlib import Path

from src.validation import validate_product
from src.workflow import generate_tasks

try:
    from src.skill_loader import load_skill
except ModuleNotFoundError:
    # 兼容直接运行 python src/main.py 的情况
    from skill_loader import load_skill


# 项目根目录：ai-product-workflow
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 产品字段的中文名称
FIELD_NAMES = {
    "sample_box_sachets": "试饮装小袋数量",
    "grams_per_sachet": "每袋重量（克）",
    "total_net_weight_g": "试饮装总净重（克）",
    "regular_pack_weight_g": "正装重量（克）",
    "product_material": "产品材质",
    "product_size": "产品尺寸",
}

# 任务与 Skill 的对应关系
TASK_SKILLS = {
    "市场调研": "market_research",
    "可行性评估": "market_research",
    "产品需求文档": "prd",
    "营销内容": "marketing",
    "包装方案": "marketing",
}


def load_product_config():
    """读取产品配置文件。"""
    config_path = PROJECT_ROOT / "config" / "product.json"

    if not config_path.is_file():
        raise FileNotFoundError(
            f"找不到产品配置文件：{config_path}"
        )

    with config_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def get_task_guidance(task_name):
    """根据任务名称读取对应的 Skill 规则。"""
    skill_name = TASK_SKILLS.get(task_name)

    if not skill_name:
        return None

    return load_skill(skill_name)


def build_report(product, errors, warnings, tasks):
    """生成中文 Markdown 工作流报告。"""
    lines = [
        "# AI 产品孵化工作流报告",
        "",
        "## 一、项目基本信息",
        "",
        f"- 项目名称：{product.get('project_name', '未填写')}",
        f"- 产品类别：{product.get('product_category', '未填写')}",
        f"- 项目状态：{product.get('status', '未填写')}",
        "",
        "## 二、产品规格",
        "",
    ]

    facts = product.get("confirmed_facts", {})

    if isinstance(facts, dict) and facts:
        for key, value in facts.items():
            label = FIELD_NAMES.get(key, key)
            lines.append(f"- {label}：{value}")
    else:
        lines.append("- 暂无产品规格资料")

    lines.extend([
        "",
        "## 三、资料检查结果",
        "",
    ])

    if errors:
        lines.append("### 错误")
        lines.append("")
        for error in errors:
            lines.append(f"- ❌ {error}")
        lines.append("")
    else:
        lines.extend([
            "- ✅ 未发现已配置规则能够识别的错误",
            "",
        ])

    if warnings:
        lines.append("### 提醒")
        lines.append("")
        for warning in warnings:
            lines.append(f"- ⚠️ {warning}")
        lines.append("")
    else:
        lines.extend([
            "- 暂无提醒",
            "",
        ])

    lines.extend([
        "## 四、工作任务清单",
        "",
        "| 序号 | 任务 | 状态 | 对应 Skill |",
        "|---|---|---|---|",
    ])

    for index, task in enumerate(tasks, start=1):
        task_name = task.get("name", "未命名任务")
        status = task.get("status", "待完成")
        skill_name = TASK_SKILLS.get(task_name, "暂未关联")

        lines.append(
            f"| {index} | {task_name} | {status} | {skill_name} |"
        )

    lines.extend([
        "",
        "## 五、Skill 规则读取情况",
        "",
    ])

    used_skills = set()

    for task in tasks:
        skill_name = TASK_SKILLS.get(task.get("name", ""))

        if skill_name:
            used_skills.add(skill_name)

    if used_skills:
        for skill_name in sorted(used_skills):
            try:
                content = load_skill(skill_name)
                if content.strip():
                    lines.append(f"- ✅ `{skill_name}`：已成功读取规则文件")
                else:
                    lines.append(f"- ⚠️ `{skill_name}`：规则文件为空")
            except (FileNotFoundError, ValueError) as error:
                lines.append(f"- ❌ `{skill_name}`：读取失败（{error}）")
    else:
        lines.append("- 当前任务没有关联 Skill")


    lines.extend([
        "",
        "## 六、各任务的工作说明",
        "",
        "以下内容来自项目中的 Skill 规则文件，供后续执行任务时参考。",
        "",
    ])

    for index, task in enumerate(tasks, start=1):
        task_name = task.get("name", "未命名任务")
        description = task.get("description", "暂无任务描述")
        skill_name = TASK_SKILLS.get(task_name)

        lines.append(f"### 任务 {index}：{task_name}")
        lines.append("")
        lines.append(f"- 任务目标：{description}")
        lines.append("")

        if not skill_name:
            lines.append("当前任务暂未关联专属 Skill。")
            lines.append("")
            continue

        try:
            guidance = get_task_guidance(task_name)

            if guidance and guidance.strip():
                lines.append(f"**参考 Skill：`{skill_name}`**")
                lines.append("")
                lines.append(guidance.strip())
            else:
                lines.append("Skill 文件内容为空。")

        except (FileNotFoundError, ValueError) as error:
            lines.append(f"读取 Skill 失败：{error}")

        lines.append("")
        lines.append("---")
        lines.append("")

    lines.extend([
        "",
        "## 七、后续需要注意的事项",
        "",
        "- 工作任务目前由程序生成，尚未自动完成。",
        "- Skill 文件提供工作规则，读取文件不代表 AI 已执行规则。",
        "- 市场数据、成本、销量和产品功效等信息需要证据支持。",
        "- 尚未确认的信息应继续标记，不应当作已知事实。",
        "",
        "---",
        "",
        "本报告由 AI 产品孵化工作流原型生成。",
        "",
    ])

    return "\n".join(lines)


def save_report(report):
    """将报告保存到 outputs 文件夹。"""
    output_dir = PROJECT_ROOT / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "product_workflow_report.md"
    output_path.write_text(report, encoding="utf-8")

    return output_path


def main():
    """程序主入口。"""
    try:
        product = load_product_config()
        errors, warnings = validate_product(product)
        tasks = generate_tasks(product)

        report = build_report(product, errors, warnings, tasks)
        output_path = save_report(report)

        print("=" * 45)
        print("AI 产品孵化工作流运行完成")
        print("=" * 45)

        print(f"项目名称：{product.get('project_name', '未填写')}")
        print(f"生成任务数：{len(tasks)}")
        print(f"发现错误数：{len(errors)}")
        print(f"提醒事项数：{len(warnings)}")
        print(f"报告位置：{output_path}")

        if errors:
            print("\n请注意：发现资料错误，请检查生成的报告。")
        else:
            print("\n资料检查未发现已配置规则能够识别的错误。")

        print("\n注意：任务清单和报告已生成，但任务本身尚未自动执行。")

    except (FileNotFoundError, json.JSONDecodeError) as error:
        print(f"程序运行失败：{error}")


if __name__ == "__main__":
    main()
