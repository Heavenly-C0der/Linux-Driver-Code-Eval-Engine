def compute_overall_score(metrics: dict) -> float:
    weights = {
        "compilation": 0.4,
        "security": 0.25,
        "code_quality": 0.2,
        "performance": 0.1,
        "advanced": 0.05
    }

    # Dummy values for missing components
    security = metrics.get("security", {"buffer_safety": 0.8, "input_validation": 0.7})
    performance = metrics.get("performance", {"efficiency": 0.8})
    advanced = metrics.get("advanced", {"debug_support": 0.0})

    total = (
        weights["compilation"] * (1.0 if metrics["compilation"]["compiled"] else 0.0) +
        weights["security"] * (sum(security.values()) / len(security)) +
        weights["code_quality"] * (sum(metrics["code_quality"].values()) / len(metrics["code_quality"])) +
        weights["performance"] * (sum(performance.values()) / len(performance)) +
        weights["advanced"] * (sum(advanced.values()) / len(advanced))
    )

    return round(total * 100, 2)
