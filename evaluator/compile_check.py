import subprocess
import os

def compile_driver(source_path: str, build_dir: str = "./build") -> dict:
    os.makedirs(build_dir, exist_ok=True)
    output_file = os.path.join(build_dir, "driver.ko")
    
    compile_cmd = ["gcc", "-Wall", "-Wextra", "-o", output_file, source_path]
    result = subprocess.run(compile_cmd, capture_output=True, text=True)
    
    success = result.returncode == 0
    errors = result.stderr.splitlines()
    warnings = [line for line in errors if "warning:" in line]
    error_msgs = [line for line in errors if "error:" in line]
    
    return {
        "compiled": success,
        "warnings_count": len(warnings),
        "errors_count": len(error_msgs),
        "stderr": errors
    }

# Example test
if __name__ == "__main__":
    result = compile_driver("../generated_code/char_driver.c")
    print(result)
