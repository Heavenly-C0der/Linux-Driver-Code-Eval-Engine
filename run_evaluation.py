import re
import json
from compile_check import compile_driver
from static_analysis import analyze_code
from score_metrics import compute_overall_score
from code_evaluation_engine import evaluate_code_file


def evaluate_security(code: str) -> dict:
    buffer_unsafe_funcs = ['strcpy', 'strcat', 'gets', 'sprintf', 'memcpy']
    input_validations = len(re.findall(r'if\s*\(.*copy_from_user.*\)', code))
    buffer_issues = sum(code.count(func) for func in buffer_unsafe_funcs)

    buffer_safety = max(0.0, 1.0 - 0.2 * buffer_issues)
    input_validation = min(1.0, 0.3 + 0.2 * input_validations)

    return {
        "buffer_safety": round(buffer_safety, 2),
        "input_validation": round(input_validation, 2)
    }


def evaluate_performance(code: str) -> dict:
    nested_loops = len(re.findall(r'for\s*\(.*\)\s*{\s*for\s*\(', code))
    excessive_logging = code.count("printk")
    penalty = 0.2 * nested_loops + 0.1 * max(0, excessive_logging - 5)
    efficiency = max(0.0, 1.0 - penalty)

    return {
        "efficiency": round(efficiency, 2)
    }


def evaluate_driver(file_path: str, output_path: str = "D:\\coding\\Notebooks\\Projects\\H2LoopAI\\results\\char_driver_score.json"):
    #  Compilation check
    compile_metrics = compile_driver(file_path)

    # Basic code quality static analysis
    code_quality = analyze_code(file_path)

    #  Advanced kernel static + clang-tidy
    code_evaluation = evaluate_code_file(file_path)

    with open(file_path, 'r') as f:
        code_text = f.read()

    #Security and Performance Analysis
    security_metrics = evaluate_security(code_text)
    performance_metrics = evaluate_performance(code_text)

    # Aggregate all metrics
    full_metrics = {
        "compilation": compile_metrics,
        "code_quality": code_quality,
        "static_analysis": code_evaluation["static_analysis"],
        "clang_tidy": {
            "warnings": code_evaluation["clang_tidy"]["clang_tidy_warnings"]
        },
        "security": security_metrics,
        "performance": performance_metrics,
        "advanced": {
            "debug_support": 0.0
        }
    }

    # Calculate overall score
    full_metrics["overall_score"] = compute_overall_score(full_metrics)

    # Save output
    with open(output_path, 'w') as f:
        json.dump(full_metrics, f, indent=4)

    #  summary
    print(f" Evaluation complete. Score: {full_metrics['overall_score']}/100")
    print("Static Analysis Issues:", code_evaluation["static_analysis"]["pattern_warnings"])
    print("clang-tidy Warnings:", code_evaluation["clang_tidy"]["clang_tidy_warnings"])


if __name__ == "__main__":
    evaluate_driver("D:\\coding\\Notebooks\\Projects\\H2LoopAI\\generated_code\\char_driver.c")
