"""
Appwrite Service - Database operations for Swifter
Handles all database interactions with Appwrite cloud
"""

import os
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.account import Account
from appwrite.exception import AppwriteException
from appwrite.query import Query

class AppwriteService:
    def __init__(self):
        self.client = Client()
        self.databases = None
        self.account = None
        self.database_id = os.getenv('APPWRITE_DATABASE_ID', 'swifter-db')
        
        # Collection IDs
        self.collections = {
            'posts': 'posts',
            'github_activity': 'github_activity', 
            'content_schedule': 'content_schedule',
            'platform_health': 'platform_health',
            'engagement_analytics': 'engagement_analytics'
        }
    
    async def initialize(self):
        """Initialize Appwrite client and services"""
        try:
            self.client.set_endpoint(os.getenv('APPWRITE_ENDPOINT', 'https://cloud.appwrite.io/v1'))
            self.client.set_project(os.getenv('APPWRITE_PROJECT_ID'))
            self.client.set_key(os.getenv('APPWRITE_API_KEY'))
            
            self.databases = Databases(self.client)
            self.account = Account(self.client)
            
            print("✅ Appwrite service initialized")
            return True
        except Exception as e:
            print(f"❌ Appwrite initialization failed: {e}")
            raise e
    
    async def health_check(self) -> str:
        """Check Appwrite database connectivity"""
        try:
            # Try to list databases to verify connection
            await self.databases.list()
            return "healthy"
        except Exception as e:
            print(f"Appwrite health check failed: {e}")
            return "unhealthy"
    
    # Posts Collection Operations
    async def create_post(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new post record in database"""
        try:
            document_data = {
                'content': content_data.get('base_content', ''),
                'platform_variants': content_data.get('variants', {}),
                'metadata': content_data.get('metadata', {}),
                'platforms_status': content_data.get('platforms_status', {}),
                'content_category': content_data.get('content_type', 'general'),
                'source_commits': content_data.get('source_commits', []),
                'engagement_data': {},
                'ai_generation_meta': content_data.get('ai_meta', {}),
                'quality_metrics': {'score': content_data.get('quality_score', 0.0)},
                'scheduled_for': content_data.get('scheduled_for'),
                'posted_at': None,
                'created_at': datetime.now(timezone.utc).isoformat(),
                'updated_at': datetime.now(timezone.utc).isoformat()
            }
            
            result = await self.databases.create_document(
                database_id=self.database_id,
                collection_id=self.collections['posts'],
                document_id='unique()',
                data=document_data
            )
            
            return result
        except AppwriteException as e:
            print(f"Failed to create post: {e}")
            raise e
    
    async def get_posts(self, limit: int = 50, offset: int = 0) -> List[Dict[str, Any]]:
        """Retrieve posts with pagination"""
        try:
            result = await self.databases.list_documents(
                database_id=self.database_id,
                collection_id=self.collections['posts'],
                queries=[
                    Query.limit(limit),
                    Query.offset(offset),
                    Query.order_desc('created_at')
                ]
            )
            return result['documents']
        except AppwriteException as e:
            print(f"Failed to get posts: {e}")
            return []
    
    async def update_post_status(self, post_id: str, platform: str, status: str, post_url: str = None):
        """Update post status for specific platform"""
        try:
            # Get current post
            post = await self.databases.get_document(
                database_id=self.database_id,
                collection_id=self.collections['posts'],
                document_id=post_id
            )
            
            # Update platform status
            platforms_status = post.get('platforms_status', {})
            platforms_status[platform] = {
                'status': status,
                'posted_at': datetime.now(timezone.utc).isoformat() if status == 'posted' else None,
                'post_url': post_url
            }
            
            await self.databases.update_document(
                database_id=self.database_id,
                collection_id=self.collections['posts'],
                document_id=post_id,
                data={
                    'platforms_status': platforms_status,
                    'updated_at': datetime.now(timezone.utc).isoformat()
                }
            )
            
        except AppwriteException as e:
            print(f"Failed to update post status: {e}")
            raise e
    
    # GitHub Activity Operations
    async def store_github_activity(self, activity_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store GitHub commit activity"""
        try:
            document_data = {
                'commit_sha': activity_data['commit_sha'],
                'commit_message': activity_data['commit_message'],
                'changed_files': activity_data.get('changed_files', []),
                'repository': activity_data['repository'],
                'commit_url': activity_data['commit_url'],
                'commit_date': activity_data['commit_date'],
                'content_generated': False,
                'learning_signals': activity_data.get('learning_signals', []),
                'processed_at': None,
                'created_at': datetime.now(timezone.utc).isoformat()
            }
            
            result = await self.databases.create_document(
                database_id=self.database_id,
                collection_id=self.collections['github_activity'],
                document_id='unique()',
                data=document_data
            )
            
            return result
        except AppwriteException as e:
            print(f"Failed to store GitHub activity: {e}")
            raise e
    
    async def get_unprocessed_commits(self) -> List[Dict[str, Any]]:
        """Get commits that haven't been processed for content generation"""
        try:
            result = await self.databases.list_documents(
                database_id=self.database_id,
                collection_id=self.collections['github_activity'],
                queries=[
                    Query.equal('content_generated', False),
                    Query.order_desc('commit_date'),
                    Query.limit(10)
                ]
            )
            return result['documents']
        except AppwriteException as e:
            print(f"Failed to get unprocessed commits: {e}")
            return []
    
    # Analytics Operations
    async def get_engagement_analytics(self, days: int = 7) -> Dict[str, Any]:
        """Get engagement analytics for specified time period"""
        try:
            # Calculate date range
            from datetime import timedelta
            end_date = datetime.now(timezone.utc)
            start_date = end_date - timedelta(days=days)
            
            result = await self.databases.list_documents(
                database_id=self.database_id,
                collection_id=self.collections['posts'],
                queries=[
                    Query.greater_than('created_at', start_date.isoformat()),
                    Query.less_than('created_at', end_date.isoformat()),
                    Query.limit(1000)
                ]
            )
            
            # Process analytics data
            analytics = self._process_engagement_data(result['documents'])
            return analytics
            
        except AppwriteException as e:
            print(f"Failed to get engagement analytics: {e}")
            return {}
    
    async def get_content_performance(self) -> Dict[str, Any]:
        """Get content type performance metrics"""
        try:
            result = await self.databases.list_documents(
                database_id=self.database_id,
                collection_id=self.collections['posts'],
                queries=[
                    Query.limit(1000),
                    Query.order_desc('created_at')
                ]
            )
            
            # Process performance data by content category
            performance = self._process_content_performance(result['documents'])
            return performance
            
        except AppwriteException as e:
            print(f"Failed to get content performance: {e}")
            return {}
    
    # Platform Health Operations
    async def update_platform_health(self, platform: str, health_data: Dict[str, Any]):
        """Update platform health status"""
        try:
            document_data = {
                'platform': platform,
                'last_successful_post': health_data.get('last_successful_post'),
                'consecutive_failures': health_data.get('consecutive_failures', 0),
                'rate_limit_reset': health_data.get('rate_limit_reset'),
                'api_status': health_data.get('api_status', 'unknown'),
                'error_details': health_data.get('error_details', {}),
                'updated_at': datetime.now(timezone.utc).isoformat()
            }
            
            # Check if platform health record exists
            try:
                existing = await self.databases.list_documents(
                    database_id=self.database_id,
                    collection_id=self.collections['platform_health'],
                    queries=[Query.equal('platform', platform)]
                )
                
                if existing['documents']:
                    # Update existing record
                    await self.databases.update_document(
                        database_id=self.database_id,
                        collection_id=self.collections['platform_health'],
                        document_id=existing['documents'][0]['$id'],
                        data=document_data
                    )
                else:
                    # Create new record
                    await self.databases.create_document(
                        database_id=self.database_id,
                        collection_id=self.collections['platform_health'],
                        document_id='unique()',
                        data=document_data
                    )
                    
            except AppwriteException as inner_e:
                print(f"Failed to update platform health: {inner_e}")
                
        except AppwriteException as e:
            print(f"Failed to update platform health: {e}")
            raise e
    
    async def get_platform_health(self) -> List[Dict[str, Any]]:
        """Get health status for all platforms"""
        try:
            result = await self.databases.list_documents(
                database_id=self.database_id,
                collection_id=self.collections['platform_health']
            )
            return result['documents']
        except AppwriteException as e:
            print(f"Failed to get platform health: {e}")
            return []
    
    # Helper methods for data processing
    def _process_engagement_data(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process posts data to extract engagement analytics"""
        analytics = {
            'total_posts': len(posts),
            'total_engagement': 0,
            'platform_breakdown': {},
            'content_type_breakdown': {},
            'daily_stats': {}
        }
        
        for post in posts:
            engagement_data = post.get('engagement_data', {})
            content_category = post.get('content_category', 'general')
            
            # Calculate total engagement
            post_engagement = sum(engagement_data.values()) if engagement_data else 0
            analytics['total_engagement'] += post_engagement
            
            # Platform breakdown
            platforms_status = post.get('platforms_status', {})
            for platform in platforms_status.keys():
                if platform not in analytics['platform_breakdown']:
                    analytics['platform_breakdown'][platform] = {'posts': 0, 'engagement': 0}
                analytics['platform_breakdown'][platform]['posts'] += 1
                analytics['platform_breakdown'][platform]['engagement'] += post_engagement
            
            # Content type breakdown
            if content_category not in analytics['content_type_breakdown']:
                analytics['content_type_breakdown'][content_category] = {'posts': 0, 'engagement': 0}
            analytics['content_type_breakdown'][content_category]['posts'] += 1
            analytics['content_type_breakdown'][content_category]['engagement'] += post_engagement
        
        return analytics
    
    def _process_content_performance(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process posts to calculate content type performance"""
        performance = {}
        
        for post in posts:
            content_category = post.get('content_category', 'general')
            quality_score = post.get('quality_metrics', {}).get('score', 0.0)
            engagement_data = post.get('engagement_data', {})
            total_engagement = sum(engagement_data.values()) if engagement_data else 0
            
            if content_category not in performance:
                performance[content_category] = {
                    'total_posts': 0,
                    'total_engagement': 0,
                    'avg_quality_score': 0.0,
                    'avg_engagement_per_post': 0.0
                }
            
            performance[content_category]['total_posts'] += 1
            performance[content_category]['total_engagement'] += total_engagement
            performance[content_category]['avg_quality_score'] += quality_score
        
        # Calculate averages
        for category, data in performance.items():
            if data['total_posts'] > 0:
                data['avg_quality_score'] /= data['total_posts']
                data['avg_engagement_per_post'] = data['total_engagement'] / data['total_posts']
        
        return performance