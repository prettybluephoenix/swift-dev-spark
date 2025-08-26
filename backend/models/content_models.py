"""
Pydantic models for content management
"""

from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum

class ContentType(str, Enum):
    DEV_JOURNEY = "dev_journey"
    TECH_EXPLAINER = "tech_explainer"
    HACKING_INSIGHTS = "hacking_insights"
    PROJECT_SHOWCASE = "project_showcase"
    HOT_TAKES = "hot_takes"

class Platform(str, Enum):
    REDDIT = "reddit"
    DISCORD = "discord"
    MASTODON = "mastodon"
    TWITTER = "twitter"

class PostStatus(str, Enum):
    DRAFT = "draft"
    SCHEDULED = "scheduled"
    POSTED = "posted"
    FAILED = "failed"

class ContentRequest(BaseModel):
    content_type: ContentType
    platforms: List[Platform]
    context: Dict[str, Any] = Field(default_factory=dict)
    custom_prompt: Optional[str] = None
    scheduled_time: Optional[datetime] = None

class ContentResponse(BaseModel):
    id: str
    content: str
    platform_variants: Dict[str, str]
    metadata: Dict[str, Any]
    quality_score: float
    created_at: datetime

class PostRequest(BaseModel):
    content_id: Optional[str] = None
    content: str
    platforms: List[Platform]
    platform_variants: Optional[Dict[str, str]] = None
    scheduled_time: Optional[datetime] = None

class PostResult(BaseModel):
    platform: Platform
    status: PostStatus
    post_id: Optional[str] = None
    post_url: Optional[str] = None
    error: Optional[str] = None
    posted_at: Optional[datetime] = None

class AnalyticsRequest(BaseModel):
    start_date: datetime
    end_date: datetime
    platforms: Optional[List[Platform]] = None
    content_types: Optional[List[ContentType]] = None

class EngagementMetrics(BaseModel):
    likes: int = 0
    comments: int = 0
    shares: int = 0
    views: int = 0
    clicks: int = 0

class PostAnalytics(BaseModel):
    post_id: str
    platform: Platform
    engagement: EngagementMetrics
    reach: int = 0
    impressions: int = 0
    last_updated: datetime