"""
Platform Manager - Handles multi-platform posting and comment management
Manages Reddit, Discord, Mastodon integrations with graceful fallbacks
"""

import os
import asyncio
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
import praw
import discord
from mastodon import Mastodon
import aiohttp
from dataclasses import dataclass

@dataclass
class PostResult:
    platform: str
    status: str
    post_id: Optional[str] = None
    post_url: Optional[str] = None
    error: Optional[str] = None
    subreddit: Optional[str] = None

@dataclass
class PlatformContent:
    title: str
    body: str
    url: Optional[str] = None
    image_url: Optional[str] = None
    is_text: bool = True

class PlatformManager:
    def __init__(self):
        self.reddit_client = None
        self.discord_client = None
        self.mastodon_client = None
        self.notification_system = NotificationSystem()
        self.initialize_clients()
    
    def initialize_clients(self):
        """Initialize platform clients with graceful degradation"""
        # Reddit Setup
        try:
            if all([os.getenv('REDDIT_CLIENT_ID'), os.getenv('REDDIT_CLIENT_SECRET')]):
                self.reddit_client = praw.Reddit(
                    client_id=os.getenv('REDDIT_CLIENT_ID'),
                    client_secret=os.getenv('REDDIT_CLIENT_SECRET'),
                    username=os.getenv('REDDIT_USERNAME'),
                    password=os.getenv('REDDIT_PASSWORD'),
                    user_agent='Swifter Bot v1.0'
                )
                print("✅ Reddit client initialized")
        except Exception as e:
            print(f"⚠️ Reddit client failed: {e}")
        
        # Discord Setup
        try:
            if os.getenv('DISCORD_WEBHOOK_URL'):
                self.discord_webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
                print("✅ Discord webhook initialized")
        except Exception as e:
            print(f"⚠️ Discord setup failed: {e}")
        
        # Mastodon Setup
        try:
            if all([os.getenv('MASTODON_ACCESS_TOKEN'), os.getenv('MASTODON_API_BASE_URL')]):
                self.mastodon_client = Mastodon(
                    access_token=os.getenv('MASTODON_ACCESS_TOKEN'),
                    api_base_url=os.getenv('MASTODON_API_BASE_URL', 'https://mastodon.social')
                )
                print("✅ Mastodon client initialized")
        except Exception as e:
            print(f"⚠️ Mastodon client failed: {e}")
    
    async def initialize(self):
        """Async initialization"""
        return True
    
    async def health_check(self) -> Dict[str, str]:
        """Check health of all platform integrations"""
        health = {}
        
        # Reddit Health
        try:
            if self.reddit_client:
                self.reddit_client.user.me()
                health['reddit'] = 'healthy'
            else:
                health['reddit'] = 'no_credentials'
        except Exception as e:
            health['reddit'] = f'unhealthy: {str(e)}'
        
        # Discord Health
        try:
            if hasattr(self, 'discord_webhook_url'):
                health['discord'] = 'healthy'
            else:
                health['discord'] = 'no_credentials'
        except Exception as e:
            health['discord'] = f'unhealthy: {str(e)}'
        
        # Mastodon Health
        try:
            if self.mastodon_client:
                self.mastodon_client.account_verify_credentials()
                health['mastodon'] = 'healthy'
            else:
                health['mastodon'] = 'no_credentials'
        except Exception as e:
            health['mastodon'] = f'unhealthy: {str(e)}'
        
        return health
    
    async def post_to_platforms(self, content: Dict[str, Any], platforms: List[str], scheduled_time: Optional[datetime] = None) -> List[PostResult]:
        """Post content to selected platforms"""
        results = []
        
        for platform in platforms:
            if platform == 'reddit':
                result = await self.post_to_reddit(content.get('reddit', content))
            elif platform == 'discord':
                result = await self.post_to_discord(content.get('discord', content))
            elif platform == 'mastodon':
                result = await self.post_to_mastodon(content.get('mastodon', content))
            elif platform == 'twitter':
                result = await self.handle_twitter_notification(content.get('twitter', content))
            else:
                result = PostResult(platform=platform, status='unsupported')
            
            results.append(result)
        
        return results
    
    async def post_to_reddit(self, content: PlatformContent) -> PostResult:
        """Post to Reddit with subreddit suggestions"""
        if not self.reddit_client:
            return PostResult(platform='reddit', status='no_credentials', error='Reddit API not configured')
        
        try:
            # AI-suggested subreddits based on content
            target_subreddits = await self.suggest_subreddits(content)
            
            for subreddit_name in target_subreddits:
                try:
                    subreddit = self.reddit_client.subreddit(subreddit_name)
                    
                    # Check if we can post to this subreddit
                    if await self.can_post_to_subreddit(subreddit):
                        if content.is_text:
                            submission = subreddit.submit(
                                title=content.title,
                                selftext=content.body
                            )
                        else:
                            submission = subreddit.submit(
                                title=content.title,
                                url=content.url
                            )
                        
                        # Start monitoring for comments
                        asyncio.create_task(self.monitor_reddit_comments(submission))
                        
                        return PostResult(
                            platform='reddit',
                            status='success',
                            post_id=submission.id,
                            post_url=submission.url,
                            subreddit=subreddit_name
                        )
                        
                except Exception as e:
                    continue  # Try next subreddit
            
            return PostResult(platform='reddit', status='failed', error='No suitable subreddit found')
            
        except Exception as e:
            return PostResult(platform='reddit', status='failed', error=str(e))
    
    async def post_to_discord(self, content: PlatformContent) -> PostResult:
        """Post to Discord via webhook"""
        if not hasattr(self, 'discord_webhook_url'):
            return PostResult(platform='discord', status='no_credentials', error='Discord webhook not configured')
        
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "content": f"**{content.title}**\n\n{content.body}",
                    "username": "Swifter Bot",
                    "avatar_url": "https://example.com/swifter-avatar.png"
                }
                
                if content.image_url:
                    payload["embeds"] = [{
                        "image": {"url": content.image_url}
                    }]
                
                async with session.post(self.discord_webhook_url, json=payload) as response:
                    if response.status == 204:
                        return PostResult(platform='discord', status='success', post_url=self.discord_webhook_url)
                    else:
                        return PostResult(platform='discord', status='failed', error=f'HTTP {response.status}')
                        
        except Exception as e:
            return PostResult(platform='discord', status='failed', error=str(e))
    
    async def post_to_mastodon(self, content: PlatformContent) -> PostResult:
        """Post to Mastodon"""
        if not self.mastodon_client:
            return PostResult(platform='mastodon', status='no_credentials', error='Mastodon API not configured')
        
        try:
            status_text = f"{content.title}\n\n{content.body}"
            
            # Add relevant hashtags
            hashtags = ["#coding", "#webdev", "#tech", "#programming"]
            status_text += "\n\n" + " ".join(hashtags)
            
            # Limit to 500 characters for Mastodon
            if len(status_text) > 500:
                status_text = status_text[:497] + "..."
            
            post = self.mastodon_client.status_post(status_text)
            
            return PostResult(
                platform='mastodon',
                status='success',
                post_id=str(post['id']),
                post_url=post['url']
            )
            
        except Exception as e:
            return PostResult(platform='mastodon', status='failed', error=str(e))
    
    async def handle_twitter_notification(self, content: PlatformContent) -> PostResult:
        """Create notification for manual Twitter posting"""
        try:
            twitter_content = await self.optimize_for_twitter(content)
            
            notification_data = {
                'id': f'twitter_{datetime.now().timestamp()}',
                'title': '🐦 New Twitter Post Ready!',
                'body': f'"{twitter_content[:50]}..." Click to copy and post to Twitter.',
                'actions': [
                    {'id': 'copy', 'title': 'Copy to Clipboard'},
                    {'id': 'edit', 'title': 'Edit First'}
                ],
                'content': twitter_content,
                'platform': 'twitter',
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            await self.notification_system.send_notification(notification_data)
            
            return PostResult(
                platform='twitter',
                status='notification_sent',
                post_id=notification_data['id']
            )
            
        except Exception as e:
            return PostResult(platform='twitter', status='failed', error=str(e))
    
    async def suggest_subreddits(self, content: PlatformContent) -> List[str]:
        """AI-powered subreddit suggestions based on content"""
        # Simple keyword-based suggestion (can be enhanced with AI)
        keywords = content.title.lower() + " " + content.body.lower()
        
        subreddit_map = {
            'programming': ['programming', 'learnprogramming', 'webdev'],
            'javascript': ['javascript', 'node', 'reactjs'],
            'python': ['python', 'learnpython', 'django'],
            'security': ['netsec', 'cybersecurity', 'hacking'],
            'ai': ['MachineLearning', 'artificial', 'deeplearning'],
            'github': ['github', 'opensource', 'git'],
            'tutorial': ['learnprogramming', 'tutorials', 'coding']
        }
        
        suggested = []
        for keyword, subreddits in subreddit_map.items():
            if keyword in keywords:
                suggested.extend(subreddits)
        
        return suggested[:3] if suggested else ['programming']
    
    async def can_post_to_subreddit(self, subreddit) -> bool:
        """Check if we can post to a subreddit"""
        try:
            # Check if subreddit exists and is accessible
            subreddit.id
            return True
        except:
            return False
    
    async def optimize_for_twitter(self, content: PlatformContent) -> str:
        """Optimize content for Twitter's 280 character limit"""
        text = f"{content.title}\n\n{content.body}"
        
        # Add hashtags
        hashtags = " #coding #webdev #tech"
        
        max_length = 280 - len(hashtags)
        if len(text) > max_length:
            text = text[:max_length-3] + "..."
        
        return text + hashtags
    
    async def monitor_reddit_comments(self, submission):
        """Monitor Reddit post for comments and auto-reply"""
        try:
            # Refresh comments every 5 minutes for 24 hours
            for _ in range(288):  # 24 hours * 12 (5-minute intervals)
                await asyncio.sleep(300)  # 5 minutes
                
                submission.comments.replace_more(limit=0)
                for comment in submission.comments:
                    if not hasattr(comment, 'author') or comment.author == self.reddit_client.user.me():
                        continue
                    
                    # Simple auto-reply logic (can be enhanced with AI)
                    if any(word in comment.body.lower() for word in ['thanks', 'helpful', 'great']):
                        if not any(reply.author == self.reddit_client.user.me() for reply in comment.replies):
                            comment.reply("Glad you found it helpful! Feel free to ask if you have any questions. 🚀")
                            
        except Exception as e:
            print(f"Comment monitoring error: {e}")

class NotificationSystem:
    def __init__(self):
        self.notifications = []
    
    async def send_notification(self, notification_data: Dict[str, Any]):
        """Send notification to frontend"""
        self.notifications.append(notification_data)
        # In a real implementation, this would push to the frontend via WebSocket
        print(f"📱 Notification: {notification_data['title']}")
    
    async def get_notifications(self) -> List[Dict[str, Any]]:
        """Get pending notifications"""
        return self.notifications
    
    async def mark_notification_read(self, notification_id: str):
        """Mark notification as read"""
        self.notifications = [n for n in self.notifications if n['id'] != notification_id]