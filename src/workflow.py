
def generate_tasks(product):
    """根据产品类别生成孵化任务清单。"""

    category = product.get("product_category", "")
    tasks = []

    # 所有产品都需要完成的任务
    tasks.append({
        "name": "市场调研",
        "description": "研究目标用户、竞品、价格和市场需求",
        "status": "待完成"
    })

    tasks.append({
        "name": "可行性评估",
        "description": "评估成本、预算、供应链和主要风险",
        "status": "待完成"
    })

    tasks.append({
        "name": "产品需求文档",
        "description": "整理产品规格、目标用户和核心卖点",
        "status": "待完成"
    })

    # 根据产品类别添加专属任务
    if category == "tea":
        tasks.append({
            "name": "茶产品规格与合规检查",
            "description": "检查净含量、配料、标签、保质期等事项",
            "status": "待完成"
        })

    elif category == "car_accessory":
        tasks.append({
            "name": "汽车用品安全检查",
            "description": "检查材料、气味、安装方式和驾驶视线影响",
            "status": "待完成"
        })

    # 所有产品都需要的后续任务
    tasks.append({
        "name": "包装方案",
        "description": "设计包装结构、视觉方向和成本预算",
        "status": "待完成"
    })

    tasks.append({
        "name": "营销内容",
        "description": "制定平台内容、产品文案和图片需求",
        "status": "待完成"
    })

    tasks.append({
        "name": "质量检查与交付",
        "description": "检查信息一致性、待确认事项和最终交付物",
        "status": "待完成"
    })

    return tasks
