"""
GitHub Service - Repository analysis and commit tracking
"""

import os
import asyncio
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone, timedelta
from github import Github
from github.GithubException import GithubException
from models.github_models import GitHubActivity, GitHubCommit, RepositoryStats

class GitHubService:
    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN')
        self.github_username = os.getenv('GITHUB_USERNAME')
        self.github_client = None
        self.repositories = []
        
    async def initialize(self):
        """Initialize GitHub client"""
        try:
            if self.github_token:
                self.github_client = Github(self.github_token)
                print("✅ GitHub service initialized")
                return True
            else:
                print("⚠️ GitHub token not found, service will be limited")
                return False
        except Exception as e:
            print(f"❌ GitHub initialization failed: {e}")
            raise e
    
    async def health_check(self) -> str:
        """Check GitHub API connectivity"""
        try:
            if self.github_client:
                # Test API with rate limit check
                rate_limit = self.github_client.get_rate_limit()
                if rate_limit.core.remaining > 0:
                    return "healthy"
                else:
                    return "rate_limited"
            return "no_token"
        except Exception as e:
            print(f"GitHub health check failed: {e}")
            return "unhealthy"
    
    async def get_recent_activity(self, days: int = 7) -> List[GitHubActivity]:
        """Get recent GitHub activity for content generation"""
        try:
            if not self.github_client:
                return []
            
            activities = []
            user = self.github_client.get_user()
            
            # Calculate date range
            since = datetime.now(timezone.utc) - timedelta(days=days)
            
            # Get repositories
            repos = user.get_repos(sort="updated", direction="desc")
            
            for repo in repos[:10]:  # Limit to recent 10 repos
                try:
                    # Get recent commits
                    commits = repo.get_commits(since=since, author=user)
                    
                    for commit in commits[:5]:  # Limit to 5 commits per repo
                        # Analyze commit for learning signals
                        learning_signals = self._extract_learning_signals(
                            commit.commit.message,
                            commit.files if hasattr(commit, 'files') else []
                        )
                        
                        activity = GitHubActivity(
                            id=f"{repo.name}-{commit.sha[:8]}",
                            commit_sha=commit.sha,
                            commit_message=commit.commit.message,
                            repository=repo.name,
                            commit_url=commit.html_url,
                            commit_date=commit.commit.author.date,
                            changed_files=[f.filename for f in commit.files] if hasattr(commit, 'files') else [],
                            learning_signals=learning_signals,
                            content_generated=False,
                            created_at=datetime.now(timezone.utc)
                        )
                        
                        activities.append(activity)
                        
                except Exception as repo_error:
                    print(f"Error processing repo {repo.name}: {repo_error}")
                    continue
            
            return sorted(activities, key=lambda x: x.commit_date, reverse=True)
            
        except Exception as e:
            print(f"Failed to get GitHub activity: {e}")
            return []
    
    async def get_commit_details(self, commit_sha: str) -> Dict[str, Any]:
        """Get detailed information about a specific commit"""
        try:
            if not self.github_client:
                raise Exception("GitHub client not initialized")
            
            # Find the commit across user's repositories
            user = self.github_client.get_user()
            repos = user.get_repos()
            
            for repo in repos:
                try:
                    commit = repo.get_commit(commit_sha)
                    
                    # Extract detailed commit information
                    commit_details = {
                        'sha': commit.sha,
                        'message': commit.commit.message,
                        'author': commit.commit.author.name,
                        'author_email': commit.commit.author.email,
                        'date': commit.commit.author.date,
                        'repository': repo.name,
                        'url': commit.html_url,
                        'files_changed': [],
                        'stats': {
                            'additions': commit.stats.additions,
                            'deletions': commit.stats.deletions,
                            'total': commit.stats.total
                        }
                    }
                    
                    # Get file changes
                    for file in commit.files:
                        commit_details['files_changed'].append({
                            'filename': file.filename,
                            'status': file.status,
                            'additions': file.additions,
                            'deletions': file.deletions,
                            'changes': file.changes
                        })
                    
                    # Extract learning signals
                    commit_details['learning_signals'] = self._extract_learning_signals(
                        commit.commit.message,
                        commit.files
                    )
                    
                    return commit_details
                    
                except GithubException:
                    # Commit not in this repo, continue searching
                    continue
            
            raise Exception(f"Commit {commit_sha} not found in user's repositories")
            
        except Exception as e:
            print(f"Failed to get commit details: {e}")
            raise e
    
    async def sync_repository_data(self):
        """Sync repository data for analytics and insights"""
        try:
            if not self.github_client:
                return
            
            user = self.github_client.get_user()
            repos = user.get_repos(sort="updated", direction="desc")
            
            repository_stats = []
            
            for repo in repos[:20]:  # Limit to 20 most recent repos
                try:
                    # Get repository statistics
                    languages = repo.get_languages()
                    commits = repo.get_commits(author=user)
                    
                    # Count commits (limited to avoid rate limiting)
                    commit_count = 0
                    last_commit_date = None
                    
                    for commit in commits[:100]:  # Limit to recent 100 commits
                        commit_count += 1
                        if not last_commit_date or commit.commit.author.date > last_commit_date:
                            last_commit_date = commit.commit.author.date
                    
                    stats = RepositoryStats(
                        name=repo.name,
                        commits_count=commit_count,
                        languages=languages,
                        last_activity=last_commit_date or repo.updated_at,
                        primary_language=repo.language
                    )
                    
                    repository_stats.append(stats)
                    
                except Exception as repo_error:
                    print(f"Error syncing repo {repo.name}: {repo_error}")
                    continue
            
            self.repositories = repository_stats
            print(f"✅ Synced {len(repository_stats)} repositories")
            
        except Exception as e:
            print(f"Repository sync failed: {e}")
    
    def _extract_learning_signals(self, commit_message: str, files: List[Any]) -> List[str]:
        """Extract learning signals from commit message and files"""
        signals = []
        message_lower = commit_message.lower()
        
        # Technical learning signals
        if any(keyword in message_lower for keyword in ['fix', 'bug', 'error', 'debug']):
            signals.append('debugging')
        
        if any(keyword in message_lower for keyword in ['add', 'implement', 'create', 'new']):
            signals.append('feature-development')
        
        if any(keyword in message_lower for keyword in ['refactor', 'improve', 'optimize']):
            signals.append('code-optimization')
        
        if any(keyword in message_lower for keyword in ['test', 'testing', 'spec']):
            signals.append('testing')
        
        if any(keyword in message_lower for keyword in ['security', 'auth', 'login', 'encrypt']):
            signals.append('security')
        
        if any(keyword in message_lower for keyword in ['api', 'endpoint', 'route']):
            signals.append('api-development')
        
        if any(keyword in message_lower for keyword in ['database', 'db', 'migration', 'schema']):
            signals.append('database')
        
        if any(keyword in message_lower for keyword in ['ui', 'frontend', 'component', 'style']):
            signals.append('frontend')
        
        # Technology signals from file extensions
        file_extensions = []
        if files:
            for file in files:
                filename = file.filename if hasattr(file, 'filename') else str(file)
                if '.' in filename:
                    ext = filename.split('.')[-1].lower()
                    file_extensions.append(ext)
        
        # Map file extensions to technologies
        tech_mapping = {
            'py': 'python',
            'js': 'javascript',
            'ts': 'typescript',
            'jsx': 'react',
            'tsx': 'react-typescript',
            'vue': 'vue',
            'php': 'php',
            'java': 'java',
            'cpp': 'cpp',
            'c': 'c',
            'go': 'golang',
            'rs': 'rust',
            'sql': 'database',
            'css': 'css',
            'scss': 'sass',
            'html': 'html',
            'json': 'configuration',
            'yaml': 'configuration',
            'yml': 'configuration',
            'md': 'documentation',
            'dockerfile': 'docker',
            'sh': 'bash-scripting'
        }
        
        for ext in file_extensions:
            if ext in tech_mapping:
                signals.append(tech_mapping[ext])
        
        # Remove duplicates and return
        return list(set(signals))
    
    async def get_repository_analytics(self) -> Dict[str, Any]:
        """Get analytics about repositories and coding activity"""
        try:
            if not self.repositories:
                await self.sync_repository_data()
            
            # Calculate analytics
            total_commits = sum(repo.commits_count for repo in self.repositories)
            
            # Language distribution
            all_languages = {}
            for repo in self.repositories:
                for lang, bytes_count in repo.languages.items():
                    all_languages[lang] = all_languages.get(lang, 0) + bytes_count
            
            # Most active repositories
            most_active = sorted(self.repositories, key=lambda x: x.commits_count, reverse=True)[:5]
            
            # Recent activity pattern
            recent_activity = [repo for repo in self.repositories 
                             if repo.last_activity > datetime.now(timezone.utc) - timedelta(days=30)]
            
            analytics = {
                'total_commits': total_commits,
                'total_repositories': len(self.repositories),
                'languages': all_languages,
                'most_active_repos': [{'name': repo.name, 'commits': repo.commits_count} 
                                    for repo in most_active],
                'recent_activity_count': len(recent_activity),
                'primary_languages': list(all_languages.keys())[:5]
            }
            
            return analytics
            
        except Exception as e:
            print(f"Failed to get repository analytics: {e}")
            return {}