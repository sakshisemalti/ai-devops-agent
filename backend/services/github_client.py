import base64
import os
from typing import Optional
from github import Github

class GitHubClient:
    def __init__(self, token: Optional[str] = None, repo_full_name: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo_full_name = repo_full_name or os.getenv("GITHUB_REPO")
        if not self.token or not self.repo_full_name:
            raise ValueError("GITHUB_TOKEN and GITHUB_REPO must be set")

        self.client = Github(self.token)
        self.repo = self.client.get_repo(self.repo_full_name)

        # ✅ Add repo_url for cloning
        self.repo_url = f"https://github.com/{self.repo_full_name}.git"

    def create_branch(self, new_branch: str, from_branch: Optional[str] = None):
        base_branch = from_branch or self.repo.default_branch
        sb = self.repo.get_branch(base_branch)
        try:
            self.repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=sb.commit.sha)
            return {"status": "created", "branch": new_branch}
        except Exception as e:
            return {"status": "exists", "branch": new_branch, "error": str(e)}

    def upsert_file(self, path: str, content: str, branch: str, message: str):
        try:
            existing = self.repo.get_contents(path, ref=branch)
            self.repo.update_file(
                path=path,
                message=message,
                content=content,
                sha=existing.sha,
                branch=branch,
            )
            return {"status": "updated", "path": path}
        except Exception:
            self.repo.create_file(
                path=path,
                message=message,
                content=content,
                branch=branch,
            )
            return {"status": "created", "path": path}

    def create_pr(self, branch: str, title: str, body: str = ""):
        base = self.repo.default_branch
        try:
            pr = self.repo.create_pull(title=title, body=body, head=branch, base=base)
            return {"number": pr.number, "url": pr.html_url}
        except Exception as e:
            return {"error": str(e), "branch": branch}

    def list_py_files(self, directory: str = "", ref: Optional[str] = None):
        ref = ref or self.repo.default_branch
        files = []
        stack = [directory.strip("/")] if directory else ["."]
        while stack:
            dir_path = stack.pop()
            try:
                contents = self.repo.get_contents(dir_path, ref=ref)
            except Exception:
                continue
            for c in contents:
                if c.type == "dir":
                    stack.append(c.path)
                elif c.type == "file" and c.path.endswith(".py"):
                    files.append(c)
        return files

    def fetch_file_text(self, path: str, ref: Optional[str] = None):
        ref = ref or self.repo.default_branch
        f = self.repo.get_contents(path, ref=ref)
        return base64.b64decode(f.content).decode("utf-8")
