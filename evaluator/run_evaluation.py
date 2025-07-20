import json
from compile_check import compile_driver
from static_analysis import analyze_code
from score_metrics import compute_overall_score
from code_evaluation_engine import evaluate_code_file


def evaluate_driver(file_path: str, output_path: str = "../results/char_driver_score.json"):
    # 1. Compilation check
    compile_metrics = compile_driver(file_path)

    # 2. Basic code quality static analysis
    code_quality = analyze_code(file_path)

    # 3. Advanced kernel static + clang-tidy
    code_evaluation = evaluate_code_file(file_path)

    # 4. Aggregate metrics
    full_metrics = {
        "compilation": compile_metrics,
        "code_quality": code_quality,
        "static_analysis": code_evaluation["static_analysis"],
        "clang_tidy": {
            "warnings": code_evaluation["clang_tidy"]["clang_tidy_warnings"]
        },
        "security": {
            "buffer_safety": 0.9,
            "input_validation": 0.7
        },
        "performance": {
            "efficiency": 0.8
        },
        "advanced": {
            "debug_support": 0.0
        }
    }

    # 5. Calculate overall score
    full_metrics["overall_score"] = compute_overall_score(full_metrics)

    # 6. Save output
    with open(output_path, 'w') as f:
        json.dump(full_metrics, f, indent=4)

    # 7. Print summary
    print(f" Evaluation complete. Score: {full_metrics['overall_score']}/100")
    print("Static Analysis Issues:", code_evaluation["static_analysis"]["pattern_warnings"])
    print("clang-tidy Warnings:", code_evaluation["clang_tidy"]["clang_tidy_warnings"])


if __name__ == "__main__":
    evaluate_driver("../generated_code/char_driver.c")
