import subprocess
import os

def run_black_file(file_path: str):
    """
    Run Black formatter on a single file.
    If Black fails (invalid Python), log the error instead of crashing.
    """
    try:
        subprocess.run(["black", file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"⚠️ Black failed on {file_path}: {e}")

def sanitize_output(raw_output: str) -> str:
    """
    Strip Ollama's raw output of markdown fences, prose, and hidden characters.
    Ensures only valid Python code remains.
    """
    lines = raw_output.splitlines()
    code_lines = []
    for line in lines:
        if line.strip().startswith("```"):
            continue
        if line.strip().lower().startswith("here") or "corrected" in line.lower():
            continue
        if line.strip().startswith("*") or line.strip().startswith("This "):
            continue
        code_lines.append(line)
    clean = "\n".join(code_lines).strip()
    clean = clean.encode("utf-8", "ignore").decode()  # remove hidden chars
    while "\n\n\n" in clean:
        clean = clean.replace("\n\n\n", "\n\n")       # normalize whitespace
    return clean

def ai_refactor_with_ollama(code: str, feedback: str | None = None) -> str:
    """
    Use Ollama locally to refactor/fix code.
    IMPORTANT: Force Ollama to output ONLY valid Python code.
    Then sanitize the output to strip prose/markdown.
    """
    if feedback:
        prompt = (
            f"Fix this Python code based on the following test failures.\n"
            f"Return ONLY valid Python code. Do not include explanations, comments, or markdown fences.\n\n"
            f"{feedback}\n\nCode:\n{code}"
        )
    else:
        prompt = (
            f"Refactor and fix any bugs in this Python code.\n"
            f"Return ONLY valid Python code. Do not include explanations, comments, or markdown fences.\n\n{code}"
        )

    result = subprocess.run(
        ["ollama", "run", "codellama"],
        input=prompt.encode(),
        capture_output=True,
    )
    raw_output = result.stdout.decode()
    print("Ollama raw output:\n", raw_output)

    return sanitize_output(raw_output)

def run_pytest(repo_root: str) -> tuple[bool, str]:
    """
    Run pytest inside the repo root, explicitly targeting the tests/ folder.
    """
    tests_path = os.path.join(repo_root, "tests")
    if os.path.exists(tests_path):
        cmd = ["pytest", "tests", "-q"]
    else:
        cmd = ["pytest", "-q"]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=repo_root,
    )
    success = result.returncode == 0
    return success, result.stdout + result.stderr
