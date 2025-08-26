import React from 'react';
import { Outlet, Link, useLocation } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { cn } from '@/lib/utils';
import { 
  Zap, 
  BarChart3, 
  Settings, 
  HelpCircle,
  Github,
  Sparkles
} from 'lucide-react';

const Layout = () => {
  const location = useLocation();

  const navigation = [
    {
      name: 'Content Studio',
      href: '/',
      icon: Zap,
      description: 'Create and manage content'
    },
    {
      name: 'Analytics',
      href: '/analytics',
      icon: BarChart3,
      description: 'Performance insights'
    }
  ];

  const isActive = (path: string) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation Header */}
      <header className="border-b bg-card/50 backdrop-blur supports-[backdrop-filter]:bg-card/50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            {/* Logo */}
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-primary-foreground" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-foreground">Swifter</h1>
                <p className="text-xs text-muted-foreground">AI Social Media Bot</p>
              </div>
            </div>

            {/* Navigation */}
            <nav className="hidden md:flex items-center space-x-1">
              {navigation.map((item) => {
                const Icon = item.icon;
                return (
                  <Link key={item.name} to={item.href}>
                    <Button
                      variant={isActive(item.href) ? "default" : "ghost"}
                      className={cn(
                        "flex items-center space-x-2 px-4 py-2",
                        isActive(item.href) && "bg-primary text-primary-foreground"
                      )}
                    >
                      <Icon className="w-4 h-4" />
                      <span>{item.name}</span>
                    </Button>
                  </Link>
                );
              })}
            </nav>

            {/* Right Actions */}
            <div className="flex items-center space-x-2">
              <Button variant="ghost" size="sm">
                <Github className="w-4 h-4 mr-2" />
                Connect GitHub
              </Button>
              <Button variant="ghost" size="sm">
                <Settings className="w-4 h-4" />
              </Button>
              <Button variant="ghost" size="sm">
                <HelpCircle className="w-4 h-4" />
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Mobile Navigation */}
      <div className="md:hidden border-b bg-card">
        <div className="flex overflow-x-auto">
          {navigation.map((item) => {
            const Icon = item.icon;
            return (
              <Link key={item.name} to={item.href} className="flex-shrink-0">
                <Button
                  variant={isActive(item.href) ? "default" : "ghost"}
                  className="h-14 px-6 rounded-none"
                >
                  <div className="flex flex-col items-center space-y-1">
                    <Icon className="w-4 h-4" />
                    <span className="text-xs">{item.name}</span>
                  </div>
                </Button>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Main Content */}
      <main>
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="border-t bg-card/30 mt-auto">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <div className="w-6 h-6 rounded bg-gradient-to-br from-primary to-accent flex items-center justify-center">
                  <Sparkles className="w-3 h-3 text-primary-foreground" />
                </div>
                <span className="text-sm font-medium">Swifter</span>
              </div>
              <Separator orientation="vertical" className="h-4" />
              <p className="text-sm text-muted-foreground">
                AI-powered social media automation
              </p>
            </div>
            
            <div className="flex items-center space-x-4 text-sm text-muted-foreground">
              <span>Built with Python, FastAPI & React</span>
              <Separator orientation="vertical" className="h-4" />
              <span>Powered by Appwrite & Groq AI</span>
            </div>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;