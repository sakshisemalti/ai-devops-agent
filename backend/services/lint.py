import subprocess
import json
from pathlib import Path


def run_linter(target_path: str):
    """
    Run flake8 on the given path and return parsed report.
    """
    path = Path(target_path)
    if not path.exists():
        return {"error": f"Path not found: {target_path}"}

    try:
        result = subprocess.run(
            ["flake8", str(path)],
            capture_output=True,
            text=True,
            check=False,
        )
        output = result.stdout.strip()
        issues = []
        # flake8 format: filename:line:col: code message
        for line in output.splitlines():
            parts = line.split(" ", 1)
            location, message = parts if len(parts) == 2 else (line, "")
            issues.append({"location": location, "message": message})
        return {"issues": issues, "raw": output}
    except Exception as e:
        return {"error": str(e)}


def auto_format(target_path: str):
    """
    Run black to auto-format Python files.
    """
    path = Path(target_path)
    if not path.exists():
        return {"error": f"Path not found: {target_path}"}

    try:
        result = subprocess.run(
            ["black", str(path), "--quiet"],
            capture_output=True,
            text=True,
            check=False,
        )
        return {"status": "formatted", "stderr": result.stderr}
    except Exception as e:
        return {"error": str(e)}
