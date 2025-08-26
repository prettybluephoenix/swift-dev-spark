import React, { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Switch } from '@/components/ui/switch';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell
} from 'recharts';
import { 
  TrendingUp, 
  Calendar, 
  Activity, 
  Users, 
  MessageSquare, 
  Heart, 
  Share2,
  Moon,
  Sun,
  Settings,
  CheckCircle,
  AlertCircle,
  Clock
} from 'lucide-react';

const Analytics = () => {
  const [darkMode, setDarkMode] = useState(false);

  const engagementData = [
    { name: 'Mon', reddit: 120, discord: 80, mastodon: 40, twitter: 200 },
    { name: 'Tue', reddit: 150, discord: 95, mastodon: 55, twitter: 180 },
    { name: 'Wed', reddit: 180, discord: 110, mastodon: 65, twitter: 220 },
    { name: 'Thu', reddit: 160, discord: 85, mastodon: 50, twitter: 190 },
    { name: 'Fri', reddit: 200, discord: 130, mastodon: 75, twitter: 250 },
    { name: 'Sat', reddit: 140, discord: 100, mastodon: 60, twitter: 160 },
    { name: 'Sun', reddit: 110, discord: 70, mastodon: 45, twitter: 140 }
  ];

  const contentTypeData = [
    { name: 'Dev Journey', value: 35, color: '#3B82F6' },
    { name: 'Tech Explainer', value: 25, color: '#F59E0B' },
    { name: 'Security Insights', value: 20, color: '#EF4444' },
    { name: 'Project Showcase', value: 15, color: '#10B981' },
    { name: 'Hot Takes', value: 5, color: '#8B5CF6' }
  ];

  const weeklyStats = [
    { day: 'Mon', posts: 5, engagement: 420 },
    { day: 'Tue', posts: 7, engagement: 580 },
    { day: 'Wed', posts: 6, engagement: 635 },
    { day: 'Thu', posts: 4, engagement: 485 },
    { day: 'Fri', posts: 8, engagement: 655 },
    { day: 'Sat', posts: 3, engagement: 360 },
    { day: 'Sun', posts: 2, engagement: 265 }
  ];

  const platformHealth = [
    { platform: 'Reddit', status: 'healthy', lastPost: '2 hours ago', successRate: 95 },
    { platform: 'Discord', status: 'healthy', lastPost: '1 hour ago', successRate: 98 },
    { platform: 'Mastodon', status: 'degraded', lastPost: '6 hours ago', successRate: 78 },
    { platform: 'Twitter/X', status: 'manual', lastPost: 'Manual only', successRate: 100 }
  ];

  const upcomingPosts = [
    { time: '2:30 PM', platform: 'Reddit', content: 'Tech explainer about API rate limiting...', type: 'tech_explainer' },
    { time: '4:15 PM', platform: 'Discord', content: 'Dev journey: Debugging authentication issues...', type: 'dev_journey' },
    { time: '6:45 PM', platform: 'Mastodon', content: 'Security insight: JWT token best practices...', type: 'security' },
    { time: '8:00 PM', platform: 'Reddit', content: 'Project showcase: Building an AI content bot...', type: 'project' }
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'degraded':
        return <AlertCircle className="w-4 h-4 text-amber-500" />;
      case 'manual':
        return <Settings className="w-4 h-4 text-blue-500" />;
      default:
        return <AlertCircle className="w-4 h-4 text-red-500" />;
    }
  };

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-foreground">Analytics & Scheduling</h1>
            <p className="text-muted-foreground">Performance insights and content planning</p>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Sun className="w-4 h-4" />
              <Switch checked={darkMode} onCheckedChange={toggleDarkMode} />
              <Moon className="w-4 h-4" />
            </div>
          </div>
        </div>

        {/* Stats Overview */}
        <div className="grid md:grid-cols-4 gap-4">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <TrendingUp className="w-5 h-5 text-green-500" />
                <div>
                  <p className="text-2xl font-bold">2,847</p>
                  <p className="text-sm text-muted-foreground">Total Engagement</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <MessageSquare className="w-5 h-5 text-blue-500" />
                <div>
                  <p className="text-2xl font-bold">156</p>
                  <p className="text-sm text-muted-foreground">Posts This Week</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <Users className="w-5 h-5 text-purple-500" />
                <div>
                  <p className="text-2xl font-bold">1,243</p>
                  <p className="text-sm text-muted-foreground">New Followers</p>
                </div>
              </div>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-2">
                <Activity className="w-5 h-5 text-orange-500" />
                <div>
                  <p className="text-2xl font-bold">94%</p>
                  <p className="text-sm text-muted-foreground">Success Rate</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid lg:grid-cols-3 gap-6">
          {/* Charts Section */}
          <div className="lg:col-span-2 space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Weekly Engagement</CardTitle>
                <CardDescription>Engagement metrics across all platforms</CardDescription>
              </CardHeader>
              <CardContent>
                <ResponsiveContainer width="100%" height={300}>
                  <BarChart data={engagementData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="reddit" fill="#FF4500" />
                    <Bar dataKey="discord" fill="#5865F2" />
                    <Bar dataKey="mastodon" fill="#6364FF" />
                    <Bar dataKey="twitter" fill="#1DA1F2" />
                  </BarChart>
                </ResponsiveContainer>
              </CardContent>
            </Card>

            <div className="grid md:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle>Content Type Performance</CardTitle>
                  <CardDescription>Engagement by content category</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <PieChart>
                      <Pie
                        data={contentTypeData}
                        cx="50%"
                        cy="50%"
                        innerRadius={60}
                        outerRadius={100}
                        paddingAngle={5}
                        dataKey="value"
                      >
                        {contentTypeData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Publishing Trends</CardTitle>
                  <CardDescription>Posts vs engagement over time</CardDescription>
                </CardHeader>
                <CardContent>
                  <ResponsiveContainer width="100%" height={250}>
                    <LineChart data={weeklyStats}>
                      <CartesianGrid strokeDasharray="3 3" />
                      <XAxis dataKey="day" />
                      <YAxis />
                      <Tooltip />
                      <Line type="monotone" dataKey="posts" stroke="#3B82F6" strokeWidth={2} />
                      <Line type="monotone" dataKey="engagement" stroke="#F59E0B" strokeWidth={2} />
                    </LineChart>
                  </ResponsiveContainer>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Right Sidebar */}
          <div className="space-y-6">
            {/* Platform Health */}
            <Card>
              <CardHeader>
                <CardTitle>Platform Health</CardTitle>
                <CardDescription>Real-time status monitoring</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {platformHealth.map((platform, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div className="flex items-center space-x-3">
                        {getStatusIcon(platform.status)}
                        <div>
                          <p className="font-medium text-sm">{platform.platform}</p>
                          <p className="text-xs text-muted-foreground">{platform.lastPost}</p>
                        </div>
                      </div>
                      <Badge variant={platform.status === 'healthy' ? 'default' : 'secondary'}>
                        {platform.successRate}%
                      </Badge>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Upcoming Posts */}
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <Calendar className="w-5 h-5 mr-2" />
                  Content Calendar
                </CardTitle>
                <CardDescription>Scheduled posts for today</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-3">
                  {upcomingPosts.map((post, index) => (
                    <div key={index} className="flex items-start space-x-3 p-3 border rounded-lg">
                      <div className="flex items-center space-x-1 text-xs text-muted-foreground min-w-fit">
                        <Clock className="w-3 h-3" />
                        {post.time}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center space-x-2 mb-1">
                          <Badge variant="outline" className="text-xs">
                            {post.platform}
                          </Badge>
                          <Badge variant="secondary" className="text-xs">
                            {post.type}
                          </Badge>
                        </div>
                        <p className="text-sm text-foreground line-clamp-2">
                          {post.content}
                        </p>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;