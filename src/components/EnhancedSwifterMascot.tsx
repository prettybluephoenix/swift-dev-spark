import React, { useState, useEffect, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Zap, Sparkles, AlertCircle, CheckCircle, Coffee, Code, 
  Brain, Heart, Star, Rocket, Target, Lightbulb, Flame
} from 'lucide-react';

interface SwifterState {
  mood: 'idle' | 'working' | 'celebrating' | 'thinking' | 'error' | 'sleeping' | 'active' | 'success' | 'failure' | 'excited' | 'focused';
  expression: 'happy' | 'focused' | 'excited' | 'concerned' | 'mischievous' | 'success' | 'failure' | 'loving' | 'determined';
  activity: string;
  streak: number;
  level: number;
}

interface MascotProps {
  contentGenerating?: boolean;
  postSuccess?: boolean;
  postFailure?: boolean;
  className?: string;
}

const EnhancedSwifterMascot: React.FC<MascotProps> = ({ 
  contentGenerating, 
  postSuccess, 
  postFailure,
  className = "" 
}) => {
  const [state, setState] = useState<SwifterState>({ 
    mood: 'idle', 
    expression: 'happy', 
    activity: '',
    streak: Math.floor(Math.random() * 15) + 1,
    level: Math.floor(Math.random() * 5) + 1
  });

  const [showTooltip, setShowTooltip] = useState(false);
  const [particles, setParticles] = useState<Array<{ id: number; x: number; y: number }>>([]);

  // Duolingo-like motivational messages
  const motivationalMessages = [
    "You're on fire! 🔥",
    "Keep the momentum going! 💪",
    "Amazing content streak! ⭐",
    "You're a content wizard! 🧙‍♂️",
    "Social media mastery unlocked! 🗝️",
    "Your followers will love this! 💖",
    "Content creation champion! 🏆",
    "Ready to go viral? 🚀"
  ];

  const encouragingMessages = [
    "Don't worry, we'll get it right! 💪",
    "Every expert was once a beginner! 🌱",
    "This is how we learn and grow! 📈",
    "Let's try a different approach! 🎯",
    "Persistence pays off! 🌟"
  ];

  // React to external props
  useEffect(() => {
    if (contentGenerating) {
      setState(prev => ({ 
        ...prev, 
        mood: 'working', 
        expression: 'focused', 
        activity: 'Generating amazing content...' 
      }));
    } else if (postSuccess) {
      setState(prev => ({ 
        ...prev, 
        mood: 'celebrating', 
        expression: 'success', 
        activity: motivationalMessages[Math.floor(Math.random() * motivationalMessages.length)],
        streak: prev.streak + 1
      }));
      createSuccessParticles();
    } else if (postFailure) {
      setState(prev => ({ 
        ...prev, 
        mood: 'error', 
        expression: 'concerned', 
        activity: encouragingMessages[Math.floor(Math.random() * encouragingMessages.length)]
      }));
    }
  }, [contentGenerating, postSuccess, postFailure]);

  const createSuccessParticles = useCallback(() => {
    const newParticles = Array.from({ length: 6 }, (_, i) => ({
      id: Date.now() + i,
      x: Math.random() * 100,
      y: Math.random() * 100
    }));
    setParticles(newParticles);
    setTimeout(() => setParticles([]), 2000);
  }, []);

  const getMoodIcon = () => {
    const iconProps = { className: "w-8 h-8" };
    
    switch (state.mood) {
      case 'working':
        return <Brain {...iconProps} className="w-8 h-8 text-primary animate-pulse" />;
      case 'celebrating':
        return <Rocket {...iconProps} className="w-8 h-8 text-accent" />;
      case 'success':
        return <Star {...iconProps} className="w-8 h-8 text-yellow-500" />;
      case 'error':
      case 'failure':
        return <Heart {...iconProps} className="w-8 h-8 text-pink-500" />;
      case 'thinking':
        return <Lightbulb {...iconProps} className="w-8 h-8 text-yellow-400" />;
      case 'excited':
        return <Flame {...iconProps} className="w-8 h-8 text-orange-500" />;
      case 'focused':
        return <Target {...iconProps} className="w-8 h-8 text-green-500" />;
      default:
        return <Zap {...iconProps} className="w-8 h-8 text-primary" />;
    }
  };

  const getAnimation = () => {
    switch (state.mood) {
      case 'working':
        return { 
          scale: [1, 1.1, 1], 
          rotate: [0, -5, 5, 0],
          y: [0, -5, 0] 
        };
      case 'celebrating':
        return { 
          y: [0, -20, -10, -20, 0], 
          scale: [1, 1.2, 1.1, 1.2, 1],
          rotate: [0, -10, 10, -10, 0]
        };
      case 'thinking':
        return { 
          rotate: [-3, 3, -3, 0],
          scale: [1, 1.05, 1]
        };
      case 'error':
        return { 
          x: [-5, 5, -5, 0],
          y: [0, -3, 0]
        };
      case 'active':
        return { 
          scale: [1, 1.15, 1],
          y: [0, -8, 0]
        };
      case 'excited':
        return {
          scale: [1, 1.2, 1.1, 1.2, 1],
          rotate: [0, -15, 15, -15, 0],
          y: [0, -10, -5, -10, 0]
        };
      default:
        return { y: [0, -4, 0] };
    }
  };

  const handleHover = () => {
    setState(prev => ({ 
      ...prev, 
      mood: 'excited', 
      expression: 'mischievous', 
      activity: `Level ${prev.level} Content Creator! 🎯` 
    }));
    setShowTooltip(true);
  };

  const handleLeave = () => {
    setState(prev => ({ 
      ...prev, 
      mood: 'idle', 
      expression: 'happy', 
      activity: '' 
    }));
    setShowTooltip(false);
  };

  const handleClick = () => {
    setState(prev => ({ 
      ...prev,
      mood: 'celebrating', 
      expression: 'excited', 
      activity: `${prev.streak} day streak! Keep it up! 🔥`,
      streak: prev.streak + 1
    }));
    createSuccessParticles();
    
    setTimeout(() => {
      setState(prev => ({ 
        ...prev, 
        mood: 'idle', 
        expression: 'happy', 
        activity: '' 
      }));
    }, 4000);
  };

  return (
    <div className={`relative flex flex-col items-center space-y-3 ${className}`}>
      {/* Success Particles */}
      <AnimatePresence>
        {particles.map((particle) => (
          <motion.div
            key={particle.id}
            initial={{ opacity: 1, scale: 0, x: particle.x, y: particle.y }}
            animate={{ 
              opacity: 0, 
              scale: 1.5, 
              x: particle.x + (Math.random() - 0.5) * 100,
              y: particle.y - 50
            }}
            exit={{ opacity: 0 }}
            transition={{ duration: 2, ease: "easeOut" }}
            className="absolute text-2xl pointer-events-none"
          >
            ✨
          </motion.div>
        ))}
      </AnimatePresence>

      {/* Main Mascot */}
      <motion.div
        animate={getAnimation()}
        transition={{ 
          duration: state.mood === 'celebrating' ? 1.2 : state.mood === 'excited' ? 0.8 : 2.5, 
          repeat: state.mood === 'idle' ? Infinity : state.mood === 'working' ? Infinity : 0,
          ease: state.mood === 'celebrating' ? "easeInOut" : "easeInOut"
        }}
        className={`relative w-20 h-20 rounded-full cursor-pointer shadow-xl
                   bg-gradient-to-br from-primary via-primary to-accent
                   flex items-center justify-center group
                   ${state.mood === 'success' ? 'animate-pulse' : ''}
                   ${state.mood === 'working' ? 'ring-4 ring-primary/30 ring-offset-2' : ''}
                   ${state.mood === 'celebrating' ? 'ring-4 ring-accent/50 ring-offset-2' : ''}
                   hover:shadow-2xl hover:ring-4 hover:ring-primary/40 hover:ring-offset-2
                   transition-all duration-300`}
        onHoverStart={handleHover}
        onHoverEnd={handleLeave}
        onClick={handleClick}
      >
        {getMoodIcon()}
        
        {/* Level Badge */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          className="absolute -top-1 -right-1 w-6 h-6 bg-accent text-accent-foreground rounded-full flex items-center justify-center text-xs font-bold shadow-lg"
        >
          {state.level}
        </motion.div>

        {/* Streak Indicator */}
        {state.streak > 0 && (
          <motion.div
            initial={{ scale: 0, rotate: -45 }}
            animate={{ scale: 1, rotate: 0 }}
            className="absolute -bottom-1 -left-1 bg-gradient-to-r from-orange-500 to-red-500 text-white rounded-full px-2 py-1 text-xs font-bold shadow-lg flex items-center gap-1"
          >
            <Flame className="w-3 h-3" />
            {state.streak}
          </motion.div>
        )}

        {/* Success/Celebration Effect */}
        {state.mood === 'celebrating' && (
          <motion.div
            initial={{ opacity: 0, scale: 0 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0 }}
            className="absolute inset-0 rounded-full bg-gradient-to-br from-yellow-400/20 to-orange-500/20 animate-pulse"
          />
        )}
      </motion.div>
      
      {/* Activity Bubble */}
      <AnimatePresence>
        {state.activity && (
          <motion.div
            initial={{ opacity: 0, y: 10, scale: 0.8 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -10, scale: 0.8 }}
            transition={{ type: "spring", damping: 20, stiffness: 300 }}
            className="relative bg-card text-card-foreground text-sm px-4 py-2 rounded-2xl shadow-lg border border-border/50 max-w-64 text-center backdrop-blur-sm"
          >
            <div className="absolute -top-1 left-1/2 transform -translate-x-1/2 w-0 h-0 border-l-4 border-r-4 border-b-4 border-transparent border-b-card"></div>
            {state.activity}
          </motion.div>
        )}
      </AnimatePresence>

      {/* Tooltip on Hover */}
      <AnimatePresence>
        {showTooltip && (
          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className="absolute -bottom-16 bg-popover text-popover-foreground text-xs px-3 py-2 rounded-lg shadow-xl border border-border/50 whitespace-nowrap"
          >
            Click me for motivation! 🚀
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default EnhancedSwifterMascot;