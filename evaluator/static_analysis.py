import re

def analyze_code(source_path: str) -> dict:
    with open(source_path, 'r') as f:
        code = f.read()

    metrics = {
        "style_compliance": 0.9,
        "documentation": 0.6 if "/**" not in code else 0.9,
        "maintainability": 0.75,
    }

    # Example rule: discourage use of magic numbers
    if re.search(r'\b\d{3,}\b', code):  # crude way to detect large literals
        metrics["maintainability"] -= 0.1

    return metrics

# Test
if __name__ == "__main__":
    result = analyze_code("../generated_code/char_driver.c")
    print(result)
