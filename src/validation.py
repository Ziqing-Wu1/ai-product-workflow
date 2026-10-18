def validate_product(product):
    errors = []
    warnings = []

    # 1. 检查项目名称
    if not product.get("project_name"):
        errors.append("项目名称不能为空")

    # 2. 检查产品类别
    if not product.get("product_category"):
        errors.append("产品类别不能为空")

    # 3. 检查产品规格
    facts = product.get("confirmed_facts", {})

    sachets = facts.get("sample_box_sachets")
    grams = facts.get("grams_per_sachet")
    total_weight = facts.get("total_net_weight_g")

    if sachets is None or grams is None or total_weight is None:
        warnings.append("产品规格不完整，无法检查总重量")
    elif sachets * grams != total_weight:
        errors.append(
            f"重量不一致：{sachets} 泡 × "
            f"{grams} 克 = {sachets * grams} 克，"
            f"但配置中总净重为 {total_weight} 克"
        )

    # 4. 检查待确认事项
    pending = product.get("pending_decisions", [])

    if pending:
        warnings.append(
            f"还有 {len(pending)} 项信息待确认"
        )

    return errors, warnings