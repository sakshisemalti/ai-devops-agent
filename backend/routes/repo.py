import os
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from db import get_db
from models import RepoConnection
from services.github_client import GitHubClient

router = APIRouter()


class ConnectPayload(BaseModel):
    repo_full_name: str  # e.g., "username/repo"


@router.post("/connect")
def connect_repo(payload: ConnectPayload, db: Session = Depends(get_db)):
    # Save repo connection in DB
    existing = (
        db.query(RepoConnection)
        .filter_by(repo_full_name=payload.repo_full_name)
        .first()
    )
    if not existing:
        rc = RepoConnection(repo_full_name=payload.repo_full_name)
        db.add(rc)
        db.commit()

    # Also set environment variable for immediate use
    os.environ["GITHUB_REPO"] = payload.repo_full_name

    return {"status": "connected", "repo": payload.repo_full_name}


@router.get("/files")
def list_repo_files(directory: str = "", ref: str | None = None):
    try:
        gh = GitHubClient()
        # Use "." for root directory
        dir_arg = directory.strip("/") if directory else "."
        files = gh.list_py_files(dir_arg, ref)
        return {"count": len(files), "files": [{"path": f.path} for f in files]}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to list files: {str(e)}")
