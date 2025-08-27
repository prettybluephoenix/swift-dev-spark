# 🚀 Swifter Social Media Bot

An AI-powered social media automation platform with intelligent content generation, multi-platform posting, and analytics. Built with React, Python FastAPI, and Appwrite.

## ✨ Features

### 🎯 Core Capabilities
- **AI Content Generation**: Powered by Groq and Hugging Face APIs
- **Multi-Platform Support**: Reddit, Discord, Mastodon (auto-post) + Twitter (notifications)
- **GitHub Integration**: Generate content from commits and development activity
- **Smart Scheduling**: Optimal posting times with timezone awareness
- **Analytics Dashboard**: Engagement tracking and performance metrics
- **Interactive Mascot**: Duolingo-style companion with animations

### 🛡️ Security & Authentication
- Admin-only access with secure authentication
- Environment variable configuration
- Graceful degradation when API keys are missing

### 🎨 User Experience
- Beautiful, responsive dark/light mode interface
- Real-time updates and notifications
- Interactive Swifter mascot with personality
- Content preview for all platforms

## 🏗️ Architecture

### Frontend (React + TypeScript + Tailwind)
- **Framework**: Next.js 14+ with TypeScript
- **Styling**: Tailwind CSS with custom design system
- **Components**: shadcn/ui with enhanced variants
- **Animations**: Framer Motion for smooth interactions
- **State Management**: TanStack Query for server state

### Backend (Python FastAPI)
- **Framework**: FastAPI with async support
- **Database**: Appwrite for cloud storage and real-time features
- **AI Integration**: Groq (primary) + Hugging Face (fallback)
- **Platform APIs**: Reddit (PRAW), Discord (webhooks), Mastodon
- **Scheduling**: Intelligent posting with sleep mode optimization

## 🚦 Getting Started

### Prerequisites
- Node.js 18+ and npm
- Python 3.9+
- Appwrite account (free tier)
- API keys for services (all have free tiers)

### Frontend Setup
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

### Backend Setup
```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Configure your API keys in .env
# Start the server
uvicorn main:app --reload
```

## 🔑 Environment Configuration

Create a `.env` file in the `backend/` directory:

```env
# Appwrite Configuration
APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
APPWRITE_PROJECT_ID=your_project_id
APPWRITE_API_KEY=your_api_key
APPWRITE_DATABASE_ID=swifter-db

# AI Services
GROQ_API_KEY=gsk_your_groq_api_key
HUGGING_FACE_TOKEN=hf_your_hugging_face_token

# Platform Integrations
GITHUB_TOKEN=ghp_your_github_token
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/your/webhook
MASTODON_ACCESS_TOKEN=your_mastodon_token
MASTODON_API_BASE_URL=https://mastodon.social

# Configuration
RAILWAY_TIMEZONE=America/New_York
FRONTEND_URL=http://localhost:5173
BACKEND_URL=http://localhost:8000
ENVIRONMENT=development
```

## 🎮 Usage

### Authentication
- Default admin credentials:
  - Email: `admin@swifter.dev`
  - Password: `SwifterAdmin2024!`

### Content Creation
1. **Select Content Type**: Choose from dev journey, tech explainer, hacking insights, etc.
2. **Choose Source**: Manual input or GitHub commit analysis
3. **Configure Platforms**: Select target platforms with preview
4. **Generate & Review**: AI creates optimized content for each platform
5. **Post or Schedule**: Immediate posting or intelligent scheduling

### Platform Behavior
- **Reddit**: Auto-posts to suggested subreddits, monitors for comments
- **Discord**: Posts via webhook with rich embeds
- **Mastodon**: Direct posting with hashtags
- **Twitter**: Generates optimized content with copy notification

### Analytics
- Engagement metrics across all platforms
- Content type performance analysis
- Optimal posting time recommendations
- Platform health monitoring

## 🧠 AI Content Engine

### Content Specializations
- **Dev Journey**: Progress tracking, debugging stories, milestones
- **Tech Explainers**: Complex topics with analogies and examples
- **Hacking Insights**: Ethical security content and protection strategies
- **Project Showcases**: Technical deep dives and architecture explanations

### Multi-Provider Fallback
1. **Primary**: Groq API (14,400 free requests/day)
2. **Fallback**: Hugging Face Inference API (free tier)
3. **Graceful degradation** when rate limits are reached

## 📊 Database Schema

### Appwrite Collections

#### Posts Collection
```json
{
  "content": "string",
  "platform_variants": "json",
  "metadata": "json",
  "platforms_status": "json",
  "content_category": "string",
  "source_commits": "json",
  "engagement_data": "json",
  "ai_generation_meta": "json",
  "quality_metrics": "json",
  "scheduled_for": "datetime",
  "posted_at": "datetime"
}
```

#### GitHub Activity Collection
```json
{
  "commit_sha": "string",
  "commit_message": "string",
  "changed_files": "json",
  "repository": "string",
  "commit_url": "string",
  "commit_date": "datetime",
  "content_generated": "boolean",
  "learning_signals": "json"
}
```

## 🎭 Interactive Mascot

Swifter features a Duolingo-inspired mascot with:
- **Dynamic Moods**: Working, celebrating, thinking, error states
- **Streak Tracking**: Daily content creation streaks
- **Level System**: Gamified progress indicators
- **Motivational Messages**: Context-aware encouragement
- **Interactive Animations**: Hover effects and click responses

## 🔧 Development

### Project Structure
```
swifter/
├── src/                    # Frontend source
│   ├── components/         # Reusable UI components
│   ├── pages/             # Page components
│   └── hooks/             # Custom React hooks
├── backend/               # Python FastAPI backend
│   ├── services/          # Business logic services
│   ├── models/            # Data models
│   └── config/            # Configuration
└── public/                # Static assets
```

### API Endpoints

#### Content Generation
- `POST /api/content/generate` - Generate AI content
- `POST /api/content/from-github` - Generate from GitHub commit

#### Platform Management
- `POST /api/platforms/post` - Post to platforms
- `GET /api/platforms/status` - Platform health check

#### Analytics
- `GET /api/analytics/engagement` - Engagement metrics
- `GET /api/analytics/content-performance` - Performance data

#### Scheduling
- `GET /api/schedule/upcoming` - Upcoming posts
- `POST /api/schedule/optimize` - Optimize schedule

## 🚀 Deployment

### Frontend (Vercel)
```bash
# Deploy to Vercel
vercel --prod
```

### Backend (Railway)
```bash
# Connect to Railway
railway login
railway link
railway up
```

### Environment Variables
Configure all environment variables in your deployment platforms.

## 🎯 Free Tier Optimization

- **Groq**: 14,400 requests/day for text generation
- **Hugging Face**: Free inference API for fallbacks and images
- **Appwrite**: Free tier for database and real-time features
- **Vercel**: Free hosting for frontend
- **Railway**: Free tier with sleep mode during inactive hours

## 🛠️ Troubleshooting

### Common Issues

1. **Authentication Failed**
   - Check admin credentials
   - Clear localStorage and try again

2. **API Rate Limits**
   - System automatically falls back to Hugging Face
   - Check API key configuration

3. **Platform Posting Fails**
   - Verify API credentials in environment
   - Check platform-specific rate limits
   - Review subreddit posting rules

4. **Mascot Not Animating**
   - Ensure Framer Motion is properly installed
   - Check for JavaScript errors in console

### Development Tips
- Use browser developer tools to monitor API calls
- Check backend logs for detailed error messages
- Test with limited API quotas to verify fallback behavior

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 🎉 Acknowledgments

- **Groq** for fast AI inference
- **Hugging Face** for free AI models
- **Appwrite** for backend services
- **shadcn/ui** for beautiful components
- **Duolingo** for mascot inspiration

---

Built with ❤️ for the developer community. Happy coding! 🚀