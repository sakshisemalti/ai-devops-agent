from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from db import Base


class RepoConnection(Base):
    __tablename__ = "repo_connections"
    id = Column(Integer, primary_key=True, index=True)
    repo_full_name = Column(String, unique=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class ActionLog(Base):
    __tablename__ = "action_logs"
    id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)  # e.g. "lint", "fix", "pr"
    details = Column(Text)  # JSON or text details
    created_at = Column(DateTime(timezone=True), server_default=func.now())
