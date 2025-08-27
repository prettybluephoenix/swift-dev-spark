import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Lock, Shield, User } from 'lucide-react';
import { useToast } from '@/hooks/use-toast';
import SwifterMascot from '@/components/SwifterMascot';

const ADMIN_EMAIL = 'admin@swifter.dev';
const ADMIN_PASSWORD = 'SwifterAdmin2024!';

interface AuthProps {
  onAuth: (authenticated: boolean) => void;
}

const Auth: React.FC<AuthProps> = ({ onAuth }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1500));

    if (email === ADMIN_EMAIL && password === ADMIN_PASSWORD) {
      localStorage.setItem('swifter_auth', 'true');
      onAuth(true);
      toast({
        title: "Welcome to Swifter! 🚀",
        description: "You're now authenticated and ready to create amazing content.",
      });
    } else {
      toast({
        title: "Access Denied",
        description: "Invalid credentials. Only authorized users can access Swifter.",
        variant: "destructive",
      });
    }

    setIsLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-background to-muted flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.95 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="w-full max-w-md"
      >
        <Card className="border-border/50 shadow-2xl backdrop-blur-sm bg-background/95">
          <CardHeader className="text-center space-y-4">
            <div className="flex justify-center">
              <SwifterMascot />
            </div>
            <div className="space-y-2">
              <CardTitle className="text-2xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent">
                Swifter Admin Access
              </CardTitle>
              <CardDescription>
                Secure portal for AI-powered social media automation
              </CardDescription>
            </div>
          </CardHeader>
          
          <CardContent className="space-y-4">
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email" className="flex items-center gap-2">
                  <User className="w-4 h-4" />
                  Email
                </Label>
                <Input
                  id="email"
                  type="email"
                  placeholder="admin@swifter.dev"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  className="border-border/50 focus:border-primary"
                />
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="password" className="flex items-center gap-2">
                  <Lock className="w-4 h-4" />
                  Password
                </Label>
                <Input
                  id="password"
                  type="password"
                  placeholder="Enter admin password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="border-border/50 focus:border-primary"
                />
              </div>
              
              <Button
                type="submit"
                className="w-full bg-gradient-to-r from-primary to-accent hover:from-primary/90 hover:to-accent/90"
                disabled={isLoading}
              >
                {isLoading ? (
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                    className="w-4 h-4 border-2 border-primary-foreground border-t-transparent rounded-full"
                  />
                ) : (
                  <>
                    <Shield className="w-4 h-4 mr-2" />
                    Authenticate
                  </>
                )}
              </Button>
            </form>
            
            <div className="text-center text-xs text-muted-foreground pt-4 border-t border-border/50">
              <div className="flex items-center justify-center gap-2">
                <Shield className="w-3 h-3" />
                Secure admin-only access
              </div>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
};

export default Auth;