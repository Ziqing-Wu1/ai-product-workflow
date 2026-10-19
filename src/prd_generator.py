
from pathlib import Path

from src.skill_loader import load_skill


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def generate_prd(product):
    """根据产品配置生成 PRD 初稿。"""

    project_name = product.get("project_name", "未命名项目")
    category = product.get("product_category", "未填写")
    facts = product.get("confirmed_facts", {})
    pending = product.get("pending_decisions", [])

    skill_content = load_skill("prd")

    lines = [
        f"# 产品需求文档（PRD）：{project_name}",
        "",
        "## 1. 文档说明",
        "",
        "- 文档版本：V0.1",
        "- 文档状态：初稿，待确认",
        "- 生成方式：根据产品配置和 PRD Skill 模板生成",
        "",
        "## 2. 产品基本信息",
        "",
        f"- 产品名称：{project_name}",
        f"- 产品类别：{category}",
        "",
        "## 3. 已确认的产品资料",
        "",
    ]

    if facts:
        for key, value in facts.items():
            lines.append(f"- {key}：{value}")
    else:
        lines.append("- 暂无已确认的产品规格资料")

    lines.extend([
        "",
        "## 4. 需求与方案",
        "",
        "以下内容需要结合市场调研和用户需求进一步确认。",
        "",
        "- 目标用户：待调研",
        "- 用户痛点：待调研",
        "- 核心卖点：待验证",
        "- 产品功能与体验：待设计",
        "- 成本与定价：待评估",
        "",
        "## 5. 待确认事项",
        "",
    ])

    if pending:
        for item in pending:
            lines.append(f"- [ ] {item}")
    else:
        lines.append("- [ ] 暂无记录，但仍需人工检查资料完整性")

    lines.extend([
        "",
        "## 6. 验收标准",
        "",
        "- [ ] 已确认产品名称和产品类别",
        "- [ ] 产品规格有明确记录",
        "- [ ] 目标用户和用户需求有依据",
        "- [ ] 定价与成本经过评估",
        "- [ ] 风险与待确认事项已记录",
        "",
        "## 7. PRD Skill 规则",
        "",
        skill_content.strip(),
        "",
        "---",
        "",
        "注意：本文件是规则驱动的 PRD 初稿，不代表已经完成市场调研或可行性验证。",
        "",
    ])

    return "\n".join(lines)


def save_prd(content):
    """保存 PRD 文件。"""

    output_dir = PROJECT_ROOT / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / "product_prd.md"
    output_path.write_text(content, encoding="utf-8")

    return output_path
