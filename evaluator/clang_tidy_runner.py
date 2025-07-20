import subprocess

def run_clang_tidy(file_path: str, checks: str = "readability-*,modernize-*") -> dict:
    try:
        result = subprocess.run(
            ["clang-tidy", file_path, f"--checks={checks}", "--"],
            capture_output=True, text=True
        )
        output = result.stdout + result.stderr
        warning_count = output.count("warning:")
        return {
            "clang_tidy_warnings": warning_count,
            "clang_tidy_output": output[:500]  # limit output shown
        }
    except FileNotFoundError:
        return {
            "error": "clang-tidy not installed or not in PATH.",
            "clang_tidy_warnings": -1,
            "clang_tidy_output": ""
        }
