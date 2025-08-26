"""
AI Content Engine - Groq + Hugging Face Integration
Multi-provider AI system for robust content generation
"""

import os
import asyncio
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
import aiohttp
from groq import AsyncGroq
from dataclasses import dataclass

@dataclass
class ContentOutput:
    base_content: str
    variants: Dict[str, str]
    metadata: Dict[str, Any]
    quality_score: float
    ai_meta: Dict[str, Any]

@dataclass
class ContentContext:
    content_type: str
    source_data: Dict[str, Any]
    platform_requirements: List[str]
    user_preferences: Dict[str, Any]

class AIContentEngine:
    def __init__(self):
        self.groq_client = None
        self.hf_token = os.getenv('HUGGING_FACE_TOKEN')
        self.hf_base_url = "https://api-inference.huggingface.co/models"
        
        # Rate limiting tracking
        self.rate_limits = {
            'groq': {'used': 0, 'daily_limit': 14400, 'reset_time': None},
            'hugging_face': {'used': 0, 'daily_limit': 1000, 'reset_time': None}
        }
        
        # Content generation templates
        self.content_templates = {
            'dev_journey': {
                'prompt_base': """
As Swifter, a friendly and knowledgeable developer, create engaging content about this development experience:

{context}

Write in first person, be authentic and educational. Share the challenge, the learning process, and insights gained. Keep it relatable and encouraging for fellow developers.

Content should be:
- Personal and authentic
- Educational with practical insights
- Encouraging and supportive
- Include relevant technical details without overwhelming
- End with a question or call for engagement

Character limit for base content: 500 characters
""",
                'hashtags': ['#WebDev', '#Coding', '#DevLife', '#Programming', '#TechJourney']
            },
            'tech_explainer': {
                'prompt_base': """
As Swifter, explain this technical concept in an accessible way:

{context}

Break down complex ideas into digestible parts. Use analogies when helpful. Make it educational but not intimidating.

Structure:
- Hook with why this matters
- Simple explanation with examples
- Practical applications
- Key takeaways
- Engagement question

Character limit for base content: 600 characters
""",
                'hashtags': ['#TechExplainer', '#WebDev', '#Programming', '#Learning', '#Education']
            },
            'hacking_insights': {
                'prompt_base': """
As Swifter, share ethical hacking/cybersecurity insights about:

{context}

Focus on:
- Educational approach to security concepts
- Why understanding this matters for developers
- Protection strategies and best practices
- Real-world applications
- Encourage responsible security practices

IMPORTANT: Keep content educational and ethical. No actual exploits or harmful information.

Character limit for base content: 550 characters
""",
                'hashtags': ['#CyberSecurity', '#EthicalHacking', '#WebSecurity', '#InfoSec', '#Security']
            },
            'project_showcase': {
                'prompt_base': """
As Swifter, showcase this project/work:

{context}

Highlight:
- What the project does/solves
- Interesting technical challenges
- Technologies used
- Key learnings or innovations
- What you're proud of
- Next steps or improvements planned

Make it engaging and inspiring for other developers.

Character limit for base content: 600 characters
""",
                'hashtags': ['#ProjectShowcase', '#WebDev', '#OpenSource', '#Development', '#Tech']
            },
            'hot_takes': {
                'prompt_base': """
As Swifter, share a thoughtful opinion about:

{context}

Provide:
- Clear stance with reasoning
- Evidence or examples
- Consider different perspectives
- Practical implications for developers
- Encourage discussion

Be opinionated but respectful and constructive.

Character limit for base content: 500 characters
""",
                'hashtags': ['#TechOpinion', '#WebDev', '#Programming', '#TechTrends', '#Developer']
            }
        }
        
        # Platform optimization rules
        self.platform_rules = {
            'reddit': {
                'max_length': 10000,
                'style': 'detailed_discussion',
                'formatting': 'markdown',
                'call_to_action': 'encourage_discussion'
            },
            'discord': {
                'max_length': 2000,
                'style': 'casual_conversational',
                'formatting': 'minimal_markdown',
                'call_to_action': 'quick_engagement'
            },
            'mastodon': {
                'max_length': 500,
                'style': 'professional_friendly',
                'formatting': 'hashtags_important',
                'call_to_action': 'boost_engagement'
            },
            'twitter': {
                'max_length': 280,
                'style': 'concise_impactful',
                'formatting': 'hashtags_essential',
                'call_to_action': 'retweet_worthy'
            }
        }
    
    async def initialize(self):
        """Initialize AI services"""
        try:
            # Initialize Groq client
            groq_api_key = os.getenv('GROQ_API_KEY')
            if groq_api_key:
                self.groq_client = AsyncGroq(api_key=groq_api_key)
                print("✅ Groq AI client initialized")
            else:
                print("⚠️ Groq API key not found, using Hugging Face only")
            
            return True
        except Exception as e:
            print(f"❌ AI service initialization failed: {e}")
            raise e
    
    async def health_check(self) -> str:
        """Check AI service availability"""
        try:
            if self.groq_client:
                # Test Groq with a simple request
                test_response = await self.groq_client.chat.completions.create(
                    model="llama3-8b-8192",
                    messages=[{"role": "user", "content": "Test"}],
                    max_tokens=10
                )
                if test_response:
                    return "healthy"
            
            # Fallback to Hugging Face test
            if self.hf_token:
                return "healthy_hf_only"
            
            return "unhealthy"
        except Exception as e:
            print(f"AI health check failed: {e}")
            return "degraded"
    
    async def generate_contextual_content(
        self, 
        context: ContentContext,
        content_type: str,
        platforms: List[str],
        custom_prompt: Optional[str] = None
    ) -> ContentOutput:
        """Generate platform-optimized content with Swifter's personality"""
        try:
            # Determine best AI provider
            provider = await self._get_best_provider()
            
            # Generate base content
            base_content = await self._generate_base_content(
                context, content_type, custom_prompt, provider
            )
            
            # Generate platform variants
            variants = {}
            for platform in platforms:
                if platform in self.platform_rules:
                    variant = await self._optimize_for_platform(
                        base_content, platform, provider
                    )
                    variants[platform] = variant
            
            # Calculate quality score
            quality_score = await self._assess_content_quality(base_content)
            
            # Prepare metadata
            metadata = {
                'content_type': content_type,
                'platforms': platforms,
                'generated_at': datetime.utcnow().isoformat(),
                'hashtags': self.content_templates[content_type]['hashtags'],
                'source_context': context.source_data
            }
            
            ai_meta = {
                'provider': provider,
                'model': 'llama3-8b-8192' if provider == 'groq' else 'huggingface-text-generation',
                'generation_time': datetime.utcnow().isoformat()
            }
            
            return ContentOutput(
                base_content=base_content,
                variants=variants,
                metadata=metadata,
                quality_score=quality_score,
                ai_meta=ai_meta
            )
            
        except Exception as e:
            print(f"Content generation failed: {e}")
            raise e
    
    async def generate_from_commit(self, commit_data: Dict[str, Any]) -> ContentOutput:
        """Generate content from GitHub commit data"""
        try:
            # Analyze commit for content type
            content_type = self._analyze_commit_for_content_type(commit_data)
            
            # Create context from commit
            context = ContentContext(
                content_type=content_type,
                source_data=commit_data,
                platform_requirements=['reddit', 'discord', 'mastodon'],
                user_preferences={}
            )
            
            # Generate content
            return await self.generate_contextual_content(
                context=context,
                content_type=content_type,
                platforms=['reddit', 'discord', 'mastodon', 'twitter']
            )
            
        except Exception as e:
            print(f"GitHub commit content generation failed: {e}")
            raise e
    
    async def _get_best_provider(self) -> str:
        """Determine best available AI provider based on rate limits"""
        if (self.groq_client and 
            self.rate_limits['groq']['used'] < self.rate_limits['groq']['daily_limit']):
            return 'groq'
        elif self.hf_token:
            return 'hugging_face'
        else:
            raise Exception("No AI providers available")
    
    async def _generate_base_content(
        self, 
        context: ContentContext, 
        content_type: str, 
        custom_prompt: Optional[str],
        provider: str
    ) -> str:
        """Generate base content using specified provider"""
        try:
            template = self.content_templates.get(content_type, self.content_templates['dev_journey'])
            
            if custom_prompt:
                prompt = f"{template['prompt_base']}\n\nAdditional context: {custom_prompt}\n\nContext: {json.dumps(context.source_data, indent=2)}"
            else:
                prompt = template['prompt_base'].format(context=json.dumps(context.source_data, indent=2))
            
            if provider == 'groq':
                return await self._groq_generate(prompt)
            else:
                return await self._hf_generate(prompt)
                
        except Exception as e:
            print(f"Base content generation failed: {e}")
            raise e
    
    async def _groq_generate(self, prompt: str) -> str:
        """Generate content using Groq API"""
        try:
            response = await self.groq_client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": "You are Swifter, a friendly and knowledgeable developer who creates engaging social media content. You're authentic, educational, and encouraging. Always write in first person and maintain a supportive tone."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1024,
                temperature=0.7
            )
            
            self.rate_limits['groq']['used'] += 1
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Groq generation failed: {e}")
            # Fallback to Hugging Face
            return await self._hf_generate(prompt)
    
    async def _hf_generate(self, prompt: str) -> str:
        """Generate content using Hugging Face API"""
        try:
            model_url = f"{self.hf_base_url}/microsoft/DialoGPT-large"
            
            headers = {
                "Authorization": f"Bearer {self.hf_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 500,
                    "temperature": 0.7,
                    "return_full_text": False
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(model_url, headers=headers, json=payload) as response:
                    if response.status == 200:
                        result = await response.json()
                        self.rate_limits['hugging_face']['used'] += 1
                        return result[0].get('generated_text', '').strip()
                    else:
                        raise Exception(f"HF API error: {response.status}")
                        
        except Exception as e:
            print(f"Hugging Face generation failed: {e}")
            # Return fallback content
            return "Content generation temporarily unavailable. Please try again."
    
    async def _optimize_for_platform(self, base_content: str, platform: str, provider: str) -> str:
        """Optimize content for specific platform requirements"""
        try:
            rules = self.platform_rules[platform]
            
            optimization_prompt = f"""
Adapt this content for {platform}:

Original content: {base_content}

Platform requirements:
- Max length: {rules['max_length']} characters
- Style: {rules['style']}
- Formatting: {rules['formatting']}
- Call to action: {rules['call_to_action']}

Optimize while maintaining the core message and Swifter's friendly, knowledgeable personality.
"""
            
            if provider == 'groq':
                return await self._groq_generate(optimization_prompt)
            else:
                return await self._hf_generate(optimization_prompt)
                
        except Exception as e:
            print(f"Platform optimization failed for {platform}: {e}")
            # Return truncated base content as fallback
            max_length = self.platform_rules[platform]['max_length']
            return base_content[:max_length-3] + "..." if len(base_content) > max_length else base_content
    
    async def _assess_content_quality(self, content: str) -> float:
        """Assess content quality score (0.0 to 1.0)"""
        try:
            quality_score = 0.0
            
            # Length check (optimal 100-500 chars)
            length = len(content)
            if 100 <= length <= 500:
                quality_score += 0.3
            elif 50 <= length < 100 or 500 < length <= 800:
                quality_score += 0.2
            elif length > 800:
                quality_score += 0.1
            
            # Engagement elements
            if '?' in content:  # Has question for engagement
                quality_score += 0.2
            if any(word in content.lower() for word in ['learn', 'tip', 'insight', 'challenge']):
                quality_score += 0.2
            if any(word in content.lower() for word in ['you', 'your', 'fellow', 'community']):
                quality_score += 0.15
            
            # Technical depth
            if any(tech in content.lower() for tech in ['api', 'database', 'function', 'code', 'debug']):
                quality_score += 0.15
            
            return min(quality_score, 1.0)
            
        except Exception as e:
            print(f"Quality assessment failed: {e}")
            return 0.5  # Default score
    
    def _analyze_commit_for_content_type(self, commit_data: Dict[str, Any]) -> str:
        """Analyze commit to determine best content type"""
        try:
            message = commit_data.get('commit_message', '').lower()
            files = commit_data.get('changed_files', [])
            
            # Security-related
            if any(keyword in message for keyword in ['security', 'auth', 'login', 'encrypt', 'hash']):
                return 'hacking_insights'
            
            # Bug fixes and challenges
            if any(keyword in message for keyword in ['fix', 'bug', 'error', 'debug', 'issue']):
                return 'dev_journey'
            
            # New features and projects
            if any(keyword in message for keyword in ['add', 'implement', 'create', 'build', 'new']):
                return 'project_showcase'
            
            # Documentation and explanations
            if any(keyword in message for keyword in ['doc', 'readme', 'comment', 'explain']):
                return 'tech_explainer'
            
            # Default to dev journey
            return 'dev_journey'
            
        except Exception as e:
            print(f"Commit analysis failed: {e}")
            return 'dev_journey'