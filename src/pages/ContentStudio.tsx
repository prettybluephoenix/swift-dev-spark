import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Textarea } from '@/components/ui/textarea';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import EnhancedSwifterMascot from '@/components/EnhancedSwifterMascot';
import { 
  GitBranch, 
  Zap, 
  Twitter, 
  MessageSquare, 
  Send, 
  Clock, 
  Eye,
  Hash,
  User,
  Copy,
  ExternalLink
} from 'lucide-react';

const ContentStudio = () => {
  const [contentType, setContentType] = useState('dev_journey');
  const [selectedPlatforms, setSelectedPlatforms] = useState(['reddit', 'discord']);
  const [isGenerating, setIsGenerating] = useState(false);

  const mockGitHubActivity = [
    {
      id: 1,
      commit: 'Fix authentication bug in user login',
      repo: 'swifter-bot',
      time: '2 hours ago',
      files: ['auth.py', 'models.py'],
      learningSignals: ['debugging', 'authentication', 'security']
    },
    {
      id: 2,
      commit: 'Implement AI content generation engine',
      repo: 'swifter-bot',
      time: '5 hours ago',
      files: ['ai_engine.py', 'prompts.py', 'content_generator.py'],
      learningSignals: ['ai', 'content-generation', 'api-integration']
    },
    {
      id: 3,
      commit: 'Add social media platform integrations',
      repo: 'swifter-bot',
      time: '1 day ago',
      files: ['reddit_api.py', 'discord_api.py', 'twitter_api.py'],
      learningSignals: ['api-integration', 'social-media', 'automation']
    }
  ];

  const mockTwitterNotifications = [
    {
      id: 1,
      content: "Just fixed a tricky authentication bug! 🔐 The key was understanding how JWT tokens expire and implementing proper refresh logic. Always validate your tokens, folks! #WebDev #Security",
      generated: '10 minutes ago',
      platform: 'twitter'
    },
    {
      id: 2,
      content: "Building an AI-powered content generator for social media automation. The challenge: making it sound human while being technically accurate. Progress update coming soon! 🤖✨ #AI #Automation",
      generated: '1 hour ago',
      platform: 'twitter'
    }
  ];

  const contentTypes = [
    { value: 'dev_journey', label: 'Dev Journey', description: 'Personal coding experiences and lessons' },
    { value: 'tech_explainer', label: 'Tech Explainer', description: 'Break down complex concepts' },
    { value: 'hacking_insights', label: 'Security Insights', description: 'Ethical hacking and cybersecurity' },
    { value: 'project_showcase', label: 'Project Showcase', description: 'Highlight your latest work' },
    { value: 'hot_takes', label: 'Tech Hot Takes', description: 'Industry opinions and trends' }
  ];

  const platforms = [
    { id: 'reddit', name: 'Reddit', icon: MessageSquare, color: 'bg-orange-500' },
    { id: 'discord', name: 'Discord', icon: Hash, color: 'bg-indigo-500' },
    { id: 'mastodon', name: 'Mastodon', icon: User, color: 'bg-purple-500' },
    { id: 'twitter', name: 'Twitter/X', icon: Twitter, color: 'bg-blue-500', manual: true }
  ];

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center gap-6 mb-8">
          <EnhancedSwifterMascot 
            contentGenerating={isGenerating}
            postSuccess={false}
            postFailure={false}
          />
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
              Content Studio
            </h1>
            <p className="text-lg text-muted-foreground">
              AI-powered content creation for your social media
            </p>
          </div>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Content Creation Panel */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Zap className="w-5 h-5 mr-2 text-primary" />
                  Content Generator
                </CardTitle>
                <CardDescription>
                  Create engaging posts from your development activity
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium mb-2 block">Content Type</label>
                    <Select value={contentType} onValueChange={setContentType}>
                      <SelectTrigger>
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {contentTypes.map((type) => (
                          <SelectItem key={type.value} value={type.value}>
                            <div>
                              <div className="font-medium">{type.label}</div>
                              <div className="text-xs text-muted-foreground">{type.description}</div>
                            </div>
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                  
                  <div>
                    <label className="text-sm font-medium mb-2 block">Target Platforms</label>
                    <div className="flex flex-wrap gap-2">
                      {platforms.map((platform) => {
                        const Icon = platform.icon;
                        const isSelected = selectedPlatforms.includes(platform.id);
                        return (
                          <Button
                            key={platform.id}
                            variant={isSelected ? "default" : "outline"}
                            size="sm"
                            onClick={() => {
                              if (isSelected) {
                                setSelectedPlatforms(prev => prev.filter(p => p !== platform.id));
                              } else {
                                setSelectedPlatforms(prev => [...prev, platform.id]);
                              }
                            }}
                          >
                            <Icon className="w-3 h-3 mr-1" />
                            {platform.name}
                            {platform.manual && <span className="ml-1 text-xs">(Manual)</span>}
                          </Button>
                        );
                      })}
                    </div>
                  </div>
                </div>

                <div>
                  <label className="text-sm font-medium mb-2 block">Custom Prompt (Optional)</label>
                  <Textarea 
                    placeholder="Add specific context or requirements for your content..."
                    className="min-h-[80px]"
                  />
                </div>

                <Button 
                  className="w-full bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90"
                  onClick={() => {
                    setIsGenerating(true);
                    setTimeout(() => setIsGenerating(false), 3000);
                  }}
                  disabled={isGenerating}
                >
                  {isGenerating ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-2 border-primary-foreground border-t-transparent mr-2" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Zap className="w-4 h-4 mr-2" />
                      Generate AI Content
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>

            {/* GitHub Activity Feed */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <GitBranch className="w-5 h-5 mr-2 text-primary" />
                  GitHub Activity Feed
                </CardTitle>
                <CardDescription>
                  Recent commits ready for content generation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockGitHubActivity.map((activity) => (
                    <div key={activity.id} className="border rounded-lg p-4 space-y-3">
                      <div className="flex justify-between items-start">
                        <div className="flex-1">
                          <h4 className="font-medium text-foreground">{activity.commit}</h4>
                          <p className="text-sm text-muted-foreground">
                            {activity.repo} • {activity.time}
                          </p>
                        </div>
                        <Button size="sm" variant="outline">
                          <Zap className="w-3 h-3 mr-1" />
                          Generate
                        </Button>
                      </div>
                      
                      <div className="flex flex-wrap gap-1">
                        {activity.files.map((file, idx) => (
                          <Badge key={idx} variant="secondary" className="text-xs">
                            {file}
                          </Badge>
                        ))}
                      </div>
                      
                      <div className="flex flex-wrap gap-1">
                        {activity.learningSignals.map((signal, idx) => (
                          <Badge key={idx} variant="outline" className="text-xs">
                            #{signal}
                          </Badge>
                        ))}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Twitter Notifications Panel */}
          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Twitter className="w-5 h-5 mr-2 text-blue-500" />
                  Twitter Notifications
                </CardTitle>
                <CardDescription>
                  Ready to post manually
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {mockTwitterNotifications.map((notification) => (
                    <div key={notification.id} className="border rounded-lg p-3 space-y-3">
                      <div className="text-sm text-foreground leading-relaxed">
                        {notification.content}
                      </div>
                      
                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <span className="flex items-center">
                          <Clock className="w-3 h-3 mr-1" />
                          {notification.generated}
                        </span>
                        <div className="flex space-x-2">
                          <Button size="sm" variant="outline" className="h-7 px-2">
                            <Copy className="w-3 h-3 mr-1" />
                            Copy
                          </Button>
                          <Button size="sm" variant="outline" className="h-7 px-2">
                            <ExternalLink className="w-3 h-3 mr-1" />
                            Post
                          </Button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Platform Status */}
            <Card>
              <CardHeader>
                <CardTitle>Platform Status</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {platforms.map((platform) => {
                    const Icon = platform.icon;
                    const status = platform.manual ? 'manual' : 'active';
                    return (
                      <div key={platform.id} className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <div className={`w-3 h-3 rounded-full ${platform.color}`} />
                          <Icon className="w-4 h-4" />
                          <span className="text-sm font-medium">{platform.name}</span>
                        </div>
                        <Badge variant={status === 'active' ? 'default' : 'secondary'}>
                          {status === 'active' ? 'Auto' : 'Manual'}
                        </Badge>
                      </div>
                    );
                  })}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ContentStudio;