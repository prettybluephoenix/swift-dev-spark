"""
Application settings and configuration
"""

import os
from functools import lru_cache
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    app_name: str = "Swifter Social Media Bot"
    debug: bool = False
    environment: str = "production"
    
    # API Keys
    groq_api_key: str = ""
    hugging_face_token: str = ""
    github_token: str = ""
    
    # Appwrite Configuration
    appwrite_endpoint: str = "https://cloud.appwrite.io/v1"
    appwrite_project_id: str = ""
    appwrite_api_key: str = ""
    appwrite_database_id: str = "swifter-db"
    
    # Social Media Platform APIs
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_username: str = ""
    reddit_password: str = ""
    
    discord_webhook_url: str = ""
    discord_bot_token: str = ""
    
    mastodon_access_token: str = ""
    mastodon_api_base_url: str = ""
    
    # Twitter/X (manual posting only due to API costs)
    twitter_bearer_token: str = ""
    
    # Railway/Server Configuration
    port: int = 8000
    host: str = "0.0.0.0"
    railway_timezone: str = "UTC"
    
    # Frontend Configuration
    frontend_url: str = "http://localhost:3000"
    cors_origins: list = ["http://localhost:3000", "https://vercel.app"]
    
    # Rate Limiting
    groq_daily_limit: int = 14400
    hf_daily_limit: int = 1000
    
    # Content Generation Settings
    default_content_length: int = 500
    max_posts_per_day: int = 50
    min_interval_between_posts: int = 30  # minutes
    
    # Scheduling Settings
    sleep_start_hour: int = 0  # 00:00
    sleep_end_hour: int = 6    # 06:00
    optimal_posting_hours: list = [9, 12, 15, 18, 21]  # Peak engagement times
    
    class Config:
        env_file = ".env"
        case_sensitive = False

@lru_cache()
def get_settings():
    return Settings()