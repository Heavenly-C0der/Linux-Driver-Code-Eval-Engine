import re

def detect_unused_variables(code: str) -> int:
    #  matches int x;, char *ptr;, etc.
    decl_pattern = re.compile(r'\b(?:int|char|float|double|long|short|unsigned)\s+[*]*\s*(\w+)\s*(=|;)', re.MULTILINE)
    matches = decl_pattern.findall(code)

    # Extract variable names
    variable_names = [m[0] for m in matches]

    # Count how many of these are not used elsewhere
    unused_count = 0
    for var in variable_names:
        # Escape variable name to use in regex
        usage_pattern = re.compile(rf'\b{re.escape(var)}\b')
        if len(usage_pattern.findall(code)) <= 1:  # 1 match = only the declaration
            unused_count += 1

    return unused_count


def analyze_code(source_path: str) -> dict:
    with open(source_path, 'r') as f:
        code = f.read()

    lines = code.splitlines()

    # === Style Compliance ===
    long_lines = sum(1 for line in lines if len(line) > 100)
    bad_indent = sum(1 for line in lines if re.match(r'^\S', line) and not line.startswith("#"))
    brace_on_same_line = sum(1 for line in lines if re.search(r'\)\s*{', line))  # preferred: newline

    total_lines = len(lines)
    style_penalty = 0.0
    if total_lines > 0:
        style_penalty = (0.1 * long_lines + 0.1 * bad_indent + 0.1 * brace_on_same_line) / total_lines

    style_compliance = max(0.0, 1.0 - style_penalty)

    # === Documentation ===
    doc_comments = re.findall(r'/\*\*.*?\*/', code, re.DOTALL)
    doc_ratio = len(doc_comments) / max(1, code.count("void") + code.count("int"))  # assume each function needs doc
    documentation = min(1.0, round(doc_ratio, 2))

    # === Maintainability ===
    magic_numbers = len(re.findall(r'\b\d{3,}\b', code))
    large_functions = len(re.findall(r'\b[a-zA-Z_]\w*\s+\**[a-zA-Z_]\w*\s*\([^)]*\)\s*{[^}]{100,}}', code, re.DOTALL))
    goto_usage = code.count("goto")

    maintainability = 1.0
    maintainability -= 0.1 * min(magic_numbers, 3)
    maintainability -= 0.1 * min(large_functions, 3)
    maintainability -= 0.1 * min(goto_usage, 2)
    unused_vars = detect_unused_variables(code)
    maintainability -= 0.05 * min(unused_vars, 4)
    maintainability = max(0.0, round(maintainability, 2))

    return {
        "style_compliance": round(style_compliance, 2),
        "documentation": round(documentation, 2),
        "maintainability": maintainability
    }

# Test
if __name__ == "__main__":
    result = analyze_code("D:\\coding\\Notebooks\\Projects\\H2LoopAI\\generated_code\\char_driver.c")
    print(result)
