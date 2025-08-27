"""
Intelligent Scheduler - Optimizes posting times and manages Railway sleep periods
Handles smart scheduling with timezone awareness and free tier optimization
"""

import os
import asyncio
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
import pytz
from dataclasses import dataclass, asdict

@dataclass
class OptimalTimeSlot:
    hour: int
    minute: int
    day_of_week: int  # 0=Monday, 6=Sunday
    engagement_score: float
    platform: str

@dataclass
class ScheduleEntry:
    id: str
    content_id: str
    platform: str
    scheduled_time: datetime
    status: str  # 'pending', 'posted', 'failed'
    created_at: datetime

class IntelligentScheduler:
    def __init__(self):
        self.user_timezone = os.getenv('RAILWAY_TIMEZONE', 'UTC')
        self.sleep_start = 0  # 00:00
        self.sleep_end = 6    # 06:00
        self.optimal_times = self._load_default_optimal_times()
        self.scheduled_posts = []
    
    def _load_default_optimal_times(self) -> List[OptimalTimeSlot]:
        """Load default optimal posting times based on research"""
        return [
            # Reddit optimal times
            OptimalTimeSlot(9, 0, 1, 0.85, 'reddit'),   # Tuesday 9 AM
            OptimalTimeSlot(14, 0, 2, 0.82, 'reddit'),  # Wednesday 2 PM
            OptimalTimeSlot(11, 0, 6, 0.78, 'reddit'),  # Sunday 11 AM
            
            # Discord optimal times
            OptimalTimeSlot(20, 0, 4, 0.88, 'discord'), # Friday 8 PM
            OptimalTimeSlot(19, 30, 5, 0.85, 'discord'), # Saturday 7:30 PM
            OptimalTimeSlot(15, 0, 6, 0.80, 'discord'), # Sunday 3 PM
            
            # Mastodon optimal times
            OptimalTimeSlot(8, 30, 1, 0.83, 'mastodon'), # Tuesday 8:30 AM
            OptimalTimeSlot(18, 0, 3, 0.81, 'mastodon'), # Thursday 6 PM
            OptimalTimeSlot(12, 0, 5, 0.79, 'mastodon'), # Saturday 12 PM
        ]
    
    async def optimize_schedule(self) -> Dict[str, Any]:
        """Optimize posting schedule based on engagement data and constraints"""
        user_tz = pytz.timezone(self.user_timezone)
        now = datetime.now(user_tz)
        
        # Calculate next week's optimal schedule
        schedule = []
        for slot in self.optimal_times:
            next_occurrence = self._get_next_occurrence(slot, now)
            if not self._is_sleep_time(next_occurrence):
                schedule.append({
                    'platform': slot.platform,
                    'time': next_occurrence.isoformat(),
                    'engagement_score': slot.engagement_score,
                    'day_name': next_occurrence.strftime('%A'),
                    'local_time': next_occurrence.strftime('%I:%M %p')
                })
        
        # Sort by engagement score
        schedule.sort(key=lambda x: x['engagement_score'], reverse=True)
        
        return {
            'optimal_schedule': schedule,
            'timezone': self.user_timezone,
            'sleep_period': f"{self.sleep_start:02d}:00 - {self.sleep_end:02d}:00",
            'next_post_time': schedule[0]['time'] if schedule else None
        }
    
    async def schedule_post(self, content_id: str, platform: str, preferred_time: Optional[datetime] = None) -> ScheduleEntry:
        """Schedule a post for optimal time"""
        if preferred_time:
            scheduled_time = preferred_time
        else:
            scheduled_time = await self._find_next_optimal_slot(platform)
        
        entry = ScheduleEntry(
            id=f"{platform}_{content_id}_{int(scheduled_time.timestamp())}",
            content_id=content_id,
            platform=platform,
            scheduled_time=scheduled_time,
            status='pending',
            created_at=datetime.now(timezone.utc)
        )
        
        self.scheduled_posts.append(entry)
        return entry
    
    async def get_upcoming_posts(self) -> List[Dict[str, Any]]:
        """Get upcoming scheduled posts"""
        now = datetime.now(timezone.utc)
        upcoming = [
            post for post in self.scheduled_posts
            if post.scheduled_time > now and post.status == 'pending'
        ]
        
        # Sort by scheduled time
        upcoming.sort(key=lambda x: x.scheduled_time)
        
        return [asdict(post) for post in upcoming[:10]]  # Return next 10
    
    async def process_scheduled_posts(self):
        """Process posts that are due to be published"""
        now = datetime.now(timezone.utc)
        
        for post in self.scheduled_posts:
            if (post.status == 'pending' and 
                post.scheduled_time <= now and 
                not self._is_sleep_time(now)):
                
                try:
                    # Here you would trigger the actual posting
                    # This would integrate with PlatformManager
                    print(f"📤 Publishing scheduled post: {post.id}")
                    post.status = 'posted'
                except Exception as e:
                    print(f"❌ Failed to publish post {post.id}: {e}")
                    post.status = 'failed'
    
    async def _find_next_optimal_slot(self, platform: str) -> datetime:
        """Find the next optimal time slot for a platform"""
        user_tz = pytz.timezone(self.user_timezone)
        now = datetime.now(user_tz)
        
        # Get platform-specific optimal times
        platform_slots = [slot for slot in self.optimal_times if slot.platform == platform]
        
        if not platform_slots:
            # Default to next non-sleep hour
            return self._get_next_non_sleep_time(now)
        
        # Find next occurrence of optimal times
        next_slots = []
        for slot in platform_slots:
            next_time = self._get_next_occurrence(slot, now)
            if not self._is_sleep_time(next_time):
                next_slots.append((next_time, slot.engagement_score))
        
        if next_slots:
            # Sort by engagement score and return best time
            next_slots.sort(key=lambda x: x[1], reverse=True)
            return next_slots[0][0]
        
        return self._get_next_non_sleep_time(now)
    
    def _get_next_occurrence(self, slot: OptimalTimeSlot, from_time: datetime) -> datetime:
        """Get next occurrence of an optimal time slot"""
        # Calculate days until next occurrence
        days_ahead = slot.day_of_week - from_time.weekday()
        if days_ahead <= 0:  # Target day already happened this week
            days_ahead += 7
        
        target_date = from_time.date() + timedelta(days=days_ahead)
        target_time = datetime.combine(
            target_date,
            datetime.min.time().replace(hour=slot.hour, minute=slot.minute)
        )
        
        return from_time.tzinfo.localize(target_time.replace(tzinfo=None))
    
    def _is_sleep_time(self, dt: datetime) -> bool:
        """Check if the given time is during sleep period"""
        local_hour = dt.astimezone(pytz.timezone(self.user_timezone)).hour
        return self.sleep_start <= local_hour < self.sleep_end
    
    def _get_next_non_sleep_time(self, from_time: datetime) -> datetime:
        """Get next time that's not during sleep period"""
        current = from_time
        while self._is_sleep_time(current):
            current += timedelta(hours=1)
        return current
    
    async def update_engagement_data(self, platform: str, post_time: datetime, engagement_score: float):
        """Update optimal times based on actual engagement data"""
        # In a real implementation, this would use ML to optimize timing
        day_of_week = post_time.weekday()
        hour = post_time.hour
        
        # Find existing slot or create new one
        existing_slot = None
        for slot in self.optimal_times:
            if (slot.platform == platform and 
                slot.day_of_week == day_of_week and 
                abs(slot.hour - hour) <= 1):
                existing_slot = slot
                break
        
        if existing_slot:
            # Update existing slot with moving average
            existing_slot.engagement_score = (
                existing_slot.engagement_score * 0.8 + engagement_score * 0.2
            )
        else:
            # Add new optimal time if engagement is high
            if engagement_score > 0.75:
                new_slot = OptimalTimeSlot(
                    hour=hour,
                    minute=0,
                    day_of_week=day_of_week,
                    engagement_score=engagement_score,
                    platform=platform
                )
                self.optimal_times.append(new_slot)
    
    async def get_sleep_schedule(self) -> Dict[str, Any]:
        """Get current sleep schedule configuration"""
        user_tz = pytz.timezone(self.user_timezone)
        now = datetime.now(user_tz)
        
        # Calculate next sleep and wake times
        today = now.date()
        next_sleep = user_tz.localize(
            datetime.combine(today, datetime.min.time().replace(hour=self.sleep_start))
        )
        next_wake = user_tz.localize(
            datetime.combine(today, datetime.min.time().replace(hour=self.sleep_end))
        )
        
        # If current time is past today's sleep time, use tomorrow
        if now.hour >= self.sleep_start:
            next_sleep += timedelta(days=1)
            next_wake += timedelta(days=1)
        
        return {
            'timezone': self.user_timezone,
            'sleep_start': f"{self.sleep_start:02d}:00",
            'sleep_end': f"{self.sleep_end:02d}:00",
            'next_sleep_time': next_sleep.isoformat(),
            'next_wake_time': next_wake.isoformat(),
            'currently_sleeping': self._is_sleep_time(now),
            'active_hours': f"{self.sleep_end:02d}:00 - {self.sleep_start:02d}:00"
        }

    async def start_scheduler(self):
        """Start the background scheduler process"""
        while True:
            try:
                await self.process_scheduled_posts()
                await asyncio.sleep(60)  # Check every minute
            except Exception as e:
                print(f"Scheduler error: {e}")
                await asyncio.sleep(300)  # Wait 5 minutes on error