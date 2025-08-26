"""
Swifter Social Media Bot - FastAPI Backend
AI-powered social media automation with Appwrite database integration
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
from datetime import datetime, timezone
import asyncio
from typing import List, Dict, Any, Optional

# Import our custom modules
from services.appwrite_service import AppwriteService
from services.ai_service import AIContentEngine
from services.github_service import GitHubService
from services.platform_manager import PlatformManager
from services.scheduler import IntelligentScheduler
from models.content_models import ContentRequest, ContentResponse, PostRequest
from models.github_models import GitHubActivity
from config.settings import get_settings

# Initialize FastAPI app
app = FastAPI(
    title="Swifter Social Media Bot API",
    description="AI-powered social media automation platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global service instances
settings = get_settings()
appwrite_service = AppwriteService()
ai_engine = AIContentEngine()
github_service = GitHubService()
platform_manager = PlatformManager()
scheduler = IntelligentScheduler()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    try:
        await appwrite_service.initialize()
        await ai_engine.initialize()
        await platform_manager.initialize()
        print("✅ Swifter backend initialized successfully")
    except Exception as e:
        print(f"❌ Startup error: {e}")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "Swifter Social Media Bot API",
        "status": "operational",
        "version": "1.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/health")
async def health_check():
    """Detailed health check with service status"""
    try:
        health_status = {
            "api": "healthy",
            "database": await appwrite_service.health_check(),
            "ai_service": await ai_engine.health_check(),
            "github": await github_service.health_check(),
            "platforms": await platform_manager.health_check(),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        return health_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

# Content Generation Endpoints
@app.post("/api/content/generate", response_model=ContentResponse)
async def generate_content(request: ContentRequest):
    """Generate AI-powered content for social media platforms"""
    try:
        # Generate content using AI engine
        content = await ai_engine.generate_contextual_content(
            context=request.context,
            content_type=request.content_type,
            platforms=request.platforms,
            custom_prompt=request.custom_prompt
        )
        
        # Store in database
        post_data = await appwrite_service.create_post(content)
        
        return ContentResponse(
            id=post_data["$id"],
            content=content.base_content,
            platform_variants=content.variants,
            metadata=content.metadata,
            quality_score=content.quality_score,
            created_at=post_data["created_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

@app.post("/api/content/from-github")
async def generate_from_github(commit_sha: str):
    """Generate content from specific GitHub commit"""
    try:
        # Fetch commit details
        commit_data = await github_service.get_commit_details(commit_sha)
        
        # Generate content based on commit
        content = await ai_engine.generate_from_commit(commit_data)
        
        # Store and return
        post_data = await appwrite_service.create_post(content)
        
        return ContentResponse(
            id=post_data["$id"],
            content=content.base_content,
            platform_variants=content.variants,
            metadata=content.metadata,
            quality_score=content.quality_score,
            created_at=post_data["created_at"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub content generation failed: {str(e)}")

# GitHub Integration Endpoints
@app.get("/api/github/activity", response_model=List[GitHubActivity])
async def get_github_activity():
    """Fetch recent GitHub activity for content generation"""
    try:
        activities = await github_service.get_recent_activity()
        return activities
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub activity fetch failed: {str(e)}")

@app.post("/api/github/sync")
async def sync_github_data(background_tasks: BackgroundTasks):
    """Sync GitHub data in background"""
    try:
        background_tasks.add_task(github_service.sync_repository_data)
        return {"message": "GitHub sync started", "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GitHub sync failed: {str(e)}")

# Platform Management Endpoints
@app.post("/api/platforms/post")
async def post_to_platforms(request: PostRequest):
    """Post content to selected social media platforms"""
    try:
        results = await platform_manager.post_to_platforms(
            content=request.content,
            platforms=request.platforms,
            scheduled_time=request.scheduled_time
        )
        return {"results": results, "status": "completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Platform posting failed: {str(e)}")

@app.get("/api/platforms/status")
async def get_platform_status():
    """Get current status of all connected platforms"""
    try:
        status = await platform_manager.get_platform_health()
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Platform status check failed: {str(e)}")

# Analytics Endpoints
@app.get("/api/analytics/engagement")
async def get_engagement_analytics(days: int = 7):
    """Get engagement analytics for specified time period"""
    try:
        analytics = await appwrite_service.get_engagement_analytics(days)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics fetch failed: {str(e)}")

@app.get("/api/analytics/content-performance")
async def get_content_performance():
    """Get content type performance metrics"""
    try:
        performance = await appwrite_service.get_content_performance()
        return performance
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content performance fetch failed: {str(e)}")

# Scheduling Endpoints
@app.get("/api/schedule/upcoming")
async def get_upcoming_posts():
    """Get upcoming scheduled posts"""
    try:
        posts = await scheduler.get_upcoming_posts()
        return posts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schedule fetch failed: {str(e)}")

@app.post("/api/schedule/optimize")
async def optimize_schedule():
    """Optimize posting schedule based on engagement data"""
    try:
        optimized_schedule = await scheduler.optimize_schedule()
        return optimized_schedule
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Schedule optimization failed: {str(e)}")

# Error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "timestamp": datetime.now(timezone.utc).isoformat()}
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )