import { useState, useEffect } from 'react';
import { moodDetectionService, MoodData } from '../services/moodDetection';

export default function MoodWidget() {
  const [moodData, setMoodData] = useState<MoodData | null>(null);
  const [recommendation, setRecommendation] = useState('');

  useEffect(() => {
    updateMood();
    
    // Update mood every 5 minutes
    const interval = setInterval(updateMood, 5 * 60 * 1000);
    
    return () => clearInterval(interval);
  }, []);

  const updateMood = () => {
    const current = moodDetectionService.getCurrentMood();
    setMoodData(current);
    setRecommendation(moodDetectionService.getMoodRecommendation());
  };

  const getMoodColor = (mood: string): string => {
    const colors: Record<string, string> = {
      happy: 'text-yellow-400',
      sad: 'text-blue-400',
      energetic: 'text-red-400',
      chill: 'text-green-400',
      focus: 'text-purple-400',
      neutral: 'text-zinc-400',
    };
    return colors[mood] || 'text-zinc-400';
  };

  const getMoodEmoji = (mood: string): string => {
    const emojis: Record<string, string> = {
      happy: '😊',
      sad: '😢',
      energetic: '⚡',
      chill: '😌',
      focus: '🎯',
      neutral: '😐',
    };
    return emojis[mood] || '🎵';
  };

  if (!moodData) {
    return null;
  }

  return (
    <div className="card p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-bold text-white">Your Mood</h3>
        <span className="text-3xl">{getMoodEmoji(moodData.mood)}</span>
      </div>

      <div className="space-y-4">
        {/* Mood Display */}
        <div>
          <div className="flex items-center justify-between mb-2">
            <span className={`text-2xl font-bold capitalize ${getMoodColor(moodData.mood)}`}>
              {moodData.mood}
            </span>
            <span className="text-sm text-zinc-400">
              {Math.round(moodData.confidence * 100)}% confident
            </span>
          </div>
          
          {/* Confidence Bar */}
          <div className="w-full bg-zinc-800 rounded-full h-2 overflow-hidden">
            <div
              className="bg-green-500 h-full rounded-full transition-all duration-500"
              style={{ width: `${moodData.confidence * 100}%` }}
            />
          </div>
        </div>

        {/* Recommendation */}
        <div className="bg-zinc-800 rounded-lg p-4">
          <p className="text-sm text-zinc-300">{recommendation}</p>
        </div>

        {/* Factors */}
        <div className="grid grid-cols-2 gap-3 text-xs">
          <div className="bg-zinc-800 rounded-lg p-3">
            <p className="text-zinc-400 mb-1">Time of Day</p>
            <p className="text-white font-medium">
              {Math.round(moodData.factors.timeOfDay * 100)}%
            </p>
          </div>
          <div className="bg-zinc-800 rounded-lg p-3">
            <p className="text-zinc-400 mb-1">Listening Duration</p>
            <p className="text-white font-medium">
              {Math.round(moodData.factors.listeningDuration / 60)}m
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
