from kernel_static_rules import check_kernel_patterns
from clang_tidy_runner import run_clang_tidy

def evaluate_code_file(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        code = f.read()

    # 1. Static Rule Checks
    kernel_result = check_kernel_patterns(code)

    # 2. clang-tidy scan
    clang_result = run_clang_tidy(file_path)

    # Combine both
    score = kernel_result["kernel_score"]
    warning_penalty = 0.02 * clang_result["clang_tidy_warnings"]
    final_score = max(0, score - (warning_penalty * 100))

    return {
        "static_analysis": kernel_result,
        "clang_tidy": clang_result,
        "final_code_score": round(final_score, 2)
    }

# Demo
if __name__ == "__main__":
    result = evaluate_code_file("../generated_code/char_driver.c")
    print(f"Final Code Score: {result['final_code_score']}/100")
    print("Pattern Issues:", result["static_analysis"]["pattern_warnings"])
    print("clang-tidy Warnings:", result["clang_tidy"]["clang_tidy_warnings"])
