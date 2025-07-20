# Linux Device Driver Coding Model Evaluation System

This project benchmarks AI-generated Linux device driver code using automated scoring, static analysis, and compilation checks.

### 🚀 Features
- Compilation success & error detection
- Static analysis for kernel programming patterns
- `clang-tidy` style & bug checks
- Scoring rubric based on correctness, security, code quality, performance

### 🧠 Use Case
Use this to evaluate how well LLMs like GPT or Code Llama can write Linux kernel device drivers.

---

## 📂 Folder Structure

```plaintext
generated_code/       → LLM-generated .c driver files
evaluator/            → Evaluation scripts
prompts/              → Sample prompts to test LLMs
results/              → Output score JSON
docs/                 → Documentation
