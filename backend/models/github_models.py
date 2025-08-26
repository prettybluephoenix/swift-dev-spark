"""
Pydantic models for GitHub integration
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class GitHubFile(BaseModel):
    filename: str
    additions: int = 0
    deletions: int = 0
    changes: int = 0
    status: str  # "added", "modified", "removed"

class GitHubCommit(BaseModel):
    sha: str
    message: str
    author: str
    author_email: str
    date: datetime
    url: str

class GitHubActivity(BaseModel):
    id: str
    commit_sha: str
    commit_message: str
    repository: str
    commit_url: str
    commit_date: datetime
    changed_files: List[str] = Field(default_factory=list)
    learning_signals: List[str] = Field(default_factory=list)
    content_generated: bool = False
    processed_at: Optional[datetime] = None
    created_at: datetime

class RepositoryStats(BaseModel):
    name: str
    commits_count: int
    languages: Dict[str, int]
    last_activity: datetime
    primary_language: Optional[str] = None

class GitHubAnalytics(BaseModel):
    total_commits: int
    repositories: List[RepositoryStats]
    most_active_days: List[str]
    coding_streak: int
    learning_topics: List[str]