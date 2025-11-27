import os
import tempfile
import subprocess
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db
from models import ActionLog
from services.github_client import GitHubClient
from services import fixers

router = APIRouter()

class FixAndPRPayload(BaseModel):
    directory: str
    branch: str
    pr_title: str
    pr_body: str | None = None

@router.post("/fix-and-pr")
def fix_and_pr(payload: FixAndPRPayload, db: Session = Depends(get_db)):
    gh = GitHubClient()
    branch = payload.branch

    # Create branch
    branch_info = gh.create_branch(branch)
    print("Branch info:", branch_info)

    # Clone repo locally into a temp folder
    repo_root = tempfile.mkdtemp(prefix="repo_clone_")
    subprocess.run(["git", "clone", gh.repo_url, repo_root], check=True)

    files = gh.list_py_files(payload.directory)
    print("Files found:", [f.path for f in files])

    changed = 0
    for f in files:
        text = gh.fetch_file_text(f.path)

        # Step 1: AI refactor with Ollama (sanitized)
        new_text = fixers.ai_refactor_with_ollama(text)

        # Step 2: Guarantee a header comment so every run produces a change
        if not new_text.startswith("# AI refactor applied"):
            new_text = "# AI refactor applied\n" + new_text

        # Step 3: Commit if different
        if new_text.strip() != text.strip():
            gh.upsert_file(
                path=f.path,
                content=new_text,
                branch=branch,
                message=f"AI refactor + style fix on {f.path}",
            )
            changed += 1

            # Step 4: Run Black per file
            file_path = os.path.join(repo_root, f.path)
            fixers.run_black_file(file_path)

            # Step 5: Run pytest inside repo root
            success, output = fixers.run_pytest(repo_root)
            print("Pytest output:", output)
            if not success:
                print("Tests failed, re‑prompting Ollama...")
                new_text = fixers.ai_refactor_with_ollama(new_text, feedback=output)
                gh.upsert_file(
                    path=f.path,
                    content=new_text,
                    branch=branch,
                    message=f"AI bug fix after test failure on {f.path}",
                )
                fixers.run_black_file(file_path)
                success, output = fixers.run_pytest(repo_root)
                print("Final test result:", success, output)

    # Step 6: Create PR only if changes were made
    if changed > 0:
        pr = gh.create_pr(branch=branch, title=payload.pr_title, body=payload.pr_body or "")
    else:
        pr = {"error": "No changes detected, PR not created"}

    db.add(ActionLog(action="pr", details=str({"changed": changed, "pr": pr})))
    db.commit()

    return {"changed_files": changed, "pr": pr}
