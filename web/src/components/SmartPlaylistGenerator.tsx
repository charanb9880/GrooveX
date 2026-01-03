import { useState } from 'react';
import { smartPlaylistService, PlaylistContext } from '../services/smartPlaylist';

export default function SmartPlaylistGenerator() {
  const [isGenerating, setIsGenerating] = useState(false);
  const [selectedActivity, setSelectedActivity] = useState<string>('');
  const [selectedMood, setSelectedMood] = useState<string>('');
  const [generatedPlaylist, setGeneratedPlaylist] = useState<any>(null);

  const activities = smartPlaylistService.getActivitySuggestions();
  
  const moods = [
    { value: 'happy', label: 'Happy', emoji: '😊' },
    { value: 'sad', label: 'Sad', emoji: '😢' },
    { value: 'energetic', label: 'Energetic', emoji: '⚡' },
    { value: 'chill', label: 'Chill', emoji: '😌' },
    { value: 'focus', label: 'Focus', emoji: '🎯' },
  ];

  const handleGenerate = async () => {
    setIsGenerating(true);
    
    const context: Partial<PlaylistContext> = {};
    if (selectedActivity) {
      context.activity = selectedActivity as any;
    }
    if (selectedMood) {
      context.mood = selectedMood as any;
    }

    try {
      const playlist = await smartPlaylistService.generatePlaylist(context);
      setGeneratedPlaylist(playlist);
    } catch (error) {
      console.error('Failed to generate playlist:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleQuickGenerate = async () => {
    setIsGenerating(true);
    try {
      const playlist = await smartPlaylistService.generatePlaylist();
      setGeneratedPlaylist(playlist);
    } catch (error) {
      console.error('Failed to generate playlist:', error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="card p-6">
      <div className="mb-6">
        <h3 className="text-2xl font-bold text-white mb-2">Smart Playlist Generator</h3>
        <p className="text-zinc-400 text-sm">
          AI-powered playlists based on your context
        </p>
      </div>

      {!generatedPlaylist ? (
        <div className="space-y-6">
          {/* Quick Generate */}
          <div>
            <button
              onClick={handleQuickGenerate}
              disabled={isGenerating}
              className="btn-primary w-full"
            >
              {isGenerating ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin h-5 w-5 mr-3" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Generating...
                </span>
              ) : (
                '✨ Generate for Right Now'
              )}
            </button>
            <p className="text-xs text-zinc-500 mt-2 text-center">
              Automatically detects time, weather, and your mood
            </p>
          </div>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <div className="w-full border-t border-zinc-700"></div>
            </div>
            <div className="relative flex justify-center text-sm">
              <span className="px-4 bg-zinc-900 text-zinc-400">Or customize</span>
            </div>
          </div>

          {/* Activity Selection */}
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-3">
              What are you doing?
            </label>
            <div className="grid grid-cols-3 gap-2">
              {activities.map((activity) => (
                <button
                  key={activity.activity}
                  onClick={() => setSelectedActivity(activity.activity === selectedActivity ? '' : activity.activity)}
                  className={`p-3 rounded-lg border-2 transition-all duration-200 ${
                    selectedActivity === activity.activity
                      ? 'border-green-500 bg-green-500/10'
                      : 'border-zinc-700 bg-zinc-800 hover:border-zinc-600'
                  }`}
                >
                  <div className="text-2xl mb-1">{activity.emoji}</div>
                  <div className="text-xs text-white font-medium">{activity.label}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Mood Selection */}
          <div>
            <label className="block text-sm font-medium text-zinc-300 mb-3">
              How are you feeling?
            </label>
            <div className="grid grid-cols-3 gap-2">
              {moods.map((mood) => (
                <button
                  key={mood.value}
                  onClick={() => setSelectedMood(mood.value === selectedMood ? '' : mood.value)}
                  className={`p-3 rounded-lg border-2 transition-all duration-200 ${
                    selectedMood === mood.value
                      ? 'border-green-500 bg-green-500/10'
                      : 'border-zinc-700 bg-zinc-800 hover:border-zinc-600'
                  }`}
                >
                  <div className="text-2xl mb-1">{mood.emoji}</div>
                  <div className="text-xs text-white font-medium">{mood.label}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Custom Generate Button */}
          <button
            onClick={handleGenerate}
            disabled={isGenerating || (!selectedActivity && !selectedMood)}
            className="btn-secondary w-full disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Generate Custom Playlist
          </button>
        </div>
      ) : (
        /* Generated Playlist Display */
        <div className="space-y-6">
          <div className="bg-gradient-to-r from-green-500/20 to-blue-500/20 rounded-lg p-6 border border-green-500/30">
            <h4 className="text-2xl font-bold text-white mb-2">
              {generatedPlaylist.name}
            </h4>
            <p className="text-zinc-300 text-sm mb-4">
              {generatedPlaylist.description}
            </p>
            
            <div className="flex flex-wrap gap-2 mb-4">
              {generatedPlaylist.criteria.moods.slice(0, 3).map((mood: string) => (
                <span
                  key={mood}
                  className="px-3 py-1 bg-zinc-800 rounded-full text-xs text-zinc-300 capitalize"
                >
                  {mood}
                </span>
              ))}
            </div>

            <div className="grid grid-cols-2 gap-3 text-xs">
              <div className="bg-black/30 rounded-lg p-3">
                <p className="text-zinc-400 mb-1">Context</p>
                <p className="text-white capitalize font-medium">
                  {generatedPlaylist.context.activity || generatedPlaylist.context.timeOfDay}
                </p>
              </div>
              <div className="bg-black/30 rounded-lg p-3">
                <p className="text-zinc-400 mb-1">Duration</p>
                <p className="text-white font-medium">
                  {generatedPlaylist.context.duration} mins
                </p>
              </div>
            </div>
          </div>

          <div className="space-y-2">
            <button className="btn-primary w-full">
              🎵 Start Playing
            </button>
            <button
              onClick={() => {
                setGeneratedPlaylist(null);
                setSelectedActivity('');
                setSelectedMood('');
              }}
              className="btn-secondary w-full"
            >
              Generate Another
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
