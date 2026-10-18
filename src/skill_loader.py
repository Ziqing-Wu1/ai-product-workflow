
from pathlib import Path

# 找到项目根目录
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# 登记项目支持的 Skill
SKILL_NAMES = {
    "market_research": "市场调研",
    "prd": "产品需求文档",
    "marketing": "营销内容",
}


def list_skills():
    """列出项目中实际存在的 Skill。"""
    available_skills = []

    for skill_name in SKILL_NAMES:
        skill_path = (
            PROJECT_ROOT / "skills" / skill_name / "SKILL.md"
        )

        if skill_path.is_file():
            available_skills.append(skill_name)

    return available_skills


def load_skill(skill_name):
    """读取指定 Skill 的说明文件。"""
    if skill_name not in SKILL_NAMES:
        raise ValueError(f"不支持的 Skill：{skill_name}")

    skill_path = (
        PROJECT_ROOT / "skills" / skill_name / "SKILL.md"
    )

    if not skill_path.is_file():
        raise FileNotFoundError(
            f"找不到 Skill 文件：{skill_path}"
        )

    return skill_path.read_text(encoding="utf-8")
