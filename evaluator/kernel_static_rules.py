import re

def check_kernel_patterns(code: str) -> dict:
    issues = {
        "missing_error_checks": 0,
        "magic_numbers": 0,
        "missing_kfree": 0,
        "goto_usage": 0,
    }

    lines = code.splitlines()

    for line in lines:
        if re.search(r'[^=!<>]=[^=]', line) and 'if' in line and '==' not in line: #checks for suspicious use of relational operators
            issues["missing_error_checks"] += 1
        if re.search(r'\b\d{3,}\b', line): # checks for unclear mentions of large numbers without context
            issues["magic_numbers"] += 1
        if 'kmalloc' in line and 'kfree' not in code:
            issues["missing_kfree"] += 1
        if 'goto' in line:
            issues["goto_usage"] += 1

    total_penalties = sum(issues.values())
    penalty_score = max(0, 1.0 - 0.05 * total_penalties)  # deduct 5% per issue

    return {
        "pattern_warnings": issues,
        "kernel_score": round(penalty_score * 100, 2)
    }
