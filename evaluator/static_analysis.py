import re

def remove_comments_and_strings(code: str) -> str:
    # Remove string literals
    code = re.sub(r'"(?:\\.|[^"\\])*"', '', code)  # removes "..."
    
    # Remove single-line comments
    code = re.sub(r'//.*', '', code)
    
    # Remove multi-line comments
    code = re.sub(r'/\*[\s\S]*?\*/', '', code)
    
    return code

def extract_variable_names(code: str) -> list:
    decls = []
    type_pattern = r'\b(?:int|char|float|double|long|short|unsigned)\b'

    # Match type lines: int x, y=5, *ptr, arr[10];
    lines = re.findall(rf'{type_pattern}[^;]*;', code)

    for line in lines:
        # Remove type keyword 
        line = re.sub(type_pattern, '', line).strip().rstrip(';')

        # Split by comma
        variables = [v.strip() for v in line.split(',')]

        for var in variables:
            # Remove pointer or array syntax and initialization
            var = re.sub(r'[*\[\]\s=].*$', '', var)
            if var:
                decls.append(var)

    return decls


def detect_unused_variables(code: str) -> int:
    clean_code = remove_comments_and_strings(code)

    # Remove loop headers (so we don't count loop vars)
    clean_code = re.sub(r'for\s*\(([^)]+)\)', '', clean_code)

    # Extract all declared variables (basic types, arrays, pointers, multiple vars)
    variable_names = extract_variable_names(code)

    # Count unused ones
    unused_count = 0
    for var in variable_names:
        usage_pattern = re.compile(rf'\b{re.escape(var)}\b')
        if len(usage_pattern.findall(clean_code)) <= 1:
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
