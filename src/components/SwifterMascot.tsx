import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Zap, Sparkles, AlertCircle, CheckCircle, Coffee, Code } from 'lucide-react';

interface SwifterState {
  mood: 'idle' | 'working' | 'celebrating' | 'thinking' | 'error' | 'sleeping' | 'active' | 'success' | 'failure';
  expression: 'happy' | 'focused' | 'excited' | 'concerned' | 'mischievous' | 'success' | 'failure';
  activity: string;
}

const SwifterMascot: React.FC = () => {
  const [state, setState] = useState<SwifterState>({ 
    mood: 'idle', 
    expression: 'happy', 
    activity: '' 
  });

  const getMoodIcon = () => {
    switch (state.mood) {
      case 'working':
        return <Code className="w-8 h-8 text-primary" />;
      case 'celebrating':
        return <Sparkles className="w-8 h-8 text-accent" />;
      case 'success':
        return <CheckCircle className="w-8 h-8 text-green-500" />;
      case 'error':
      case 'failure':
        return <AlertCircle className="w-8 h-8 text-destructive" />;
      case 'sleeping':
        return <Coffee className="w-8 h-8 text-muted-foreground" />;
      default:
        return <Zap className="w-8 h-8 text-primary" />;
    }
  };

  const getAnimation = () => {
    switch (state.mood) {
      case 'working':
        return { scale: [1, 1.05, 1], rotate: [-2, 2, -2, 0] };
      case 'celebrating':
        return { y: [0, -10, 0], scale: [1, 1.1, 1] };
      case 'thinking':
        return { rotate: [-5, 5, -5, 0] };
      case 'error':
        return { x: [-3, 3, -3, 0] };
      case 'active':
        return { scale: [1, 1.1, 1] };
      default:
        return { y: [0, -2, 0] };
    }
  };

  const handleHover = () => {
    setState(prev => ({ 
      ...prev, 
      mood: 'active', 
      expression: 'mischievous', 
      activity: 'Hey there! 👋' 
    }));
  };

  const handleLeave = () => {
    setState(prev => ({ 
      ...prev, 
      mood: 'idle', 
      expression: 'happy', 
      activity: '' 
    }));
  };

  const handleClick = () => {
    setState({ 
      mood: 'celebrating', 
      expression: 'excited', 
      activity: 'Ready to create amazing content! 🚀' 
    });
    setTimeout(() => {
      setState(prev => ({ 
        ...prev, 
        mood: 'idle', 
        expression: 'happy', 
        activity: '' 
      }));
    }, 3000);
  };

  return (
    <div className="flex flex-col items-center space-y-2">
      <motion.div
        animate={getAnimation()}
        transition={{ 
          duration: state.mood === 'celebrating' ? 0.6 : 2, 
          repeat: state.mood === 'idle' ? Infinity : 0,
          ease: "easeInOut"
        }}
        className={`relative w-16 h-16 rounded-full bg-gradient-to-br from-primary to-accent 
                   flex items-center justify-center cursor-pointer shadow-lg
                   ${state.mood === 'success' ? 'animate-pulse-glow' : ''}
                   ${state.mood === 'working' ? 'animate-bounce-gentle' : ''}
                   ${state.mood === 'active' ? 'animate-wiggle' : ''}`}
        onHoverStart={handleHover}
        onHoverEnd={handleLeave}
        onClick={handleClick}
      >
        {getMoodIcon()}
        
        {state.mood === 'celebrating' && (
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            className="absolute -top-1 -right-1 w-4 h-4 bg-accent rounded-full flex items-center justify-center"
          >
            ✨
          </motion.div>
        )}
      </motion.div>
      
      {state.activity && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -10 }}
          className="bg-card text-card-foreground text-xs px-3 py-1 rounded-full shadow-md border max-w-48 text-center"
        >
          {state.activity}
        </motion.div>
      )}
    </div>
  );
};

export default SwifterMascot;