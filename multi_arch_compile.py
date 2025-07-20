import os
import subprocess

# Define targets
ARCH_CONFIGS = {
    "x86_64": {
        "arch": "x86_64",
        "cross_compile": "",  # native
        "kernel_headers": "/lib/modules/$(uname -r)/build"
    },
    "arm": {
        "arch": "arm",
        "cross_compile": "arm-linux-gnueabi-",
        "kernel_headers": "/path/to/arm/linux-headers"  # adjust
    },
    "riscv": {
        "arch": "riscv",
        "cross_compile": "riscv64-linux-gnu-",
        "kernel_headers": "/path/to/riscv/linux-headers"  # adjust
    }
}

DRIVER_DIR = "generated_code"
SRC_FILE = "char_driver.c"

def compile_driver(arch_name, config):
    print(f"\n=== Compiling for {arch_name.upper()} ===")

    env = os.environ.copy()
    env["ARCH"] = config["arch"]
    env["CROSS_COMPILE"] = config["cross_compile"]

    make_cmd = [
        "make", "-C", config["kernel_headers"],
        f"M={os.path.abspath(DRIVER_DIR)}", "modules"
    ]

    try:
        result = subprocess.run(make_cmd, env=env, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"[✓] {arch_name} build success!")
        else:
            print(f"[✗] {arch_name} build failed:")
            print(result.stderr)
    except Exception as e:
        print(f"[!] Error building for {arch_name}: {e}")

if __name__ == "__main__":
    for arch, config in ARCH_CONFIGS.items():
        compile_driver(arch, config)
