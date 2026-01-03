import { useState } from 'react';
import MoodWidget from '../components/MoodWidget';
import SmartPlaylistGenerator from '../components/SmartPlaylistGenerator';
import LyricsDisplay from '../components/LyricsDisplay';

export default function AIFeatures() {
  const [currentTime, setCurrentTime] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [showLyricsDemo, setShowLyricsDemo] = useState(false);

  // Demo: Simulate playback for lyrics
  const startLyricsDemo = () => {
    setShowLyricsDemo(true);
    setIsPlaying(true);
    setCurrentTime(0);

    // Simulate playback (1 second intervals)
    const interval = setInterval(() => {
      setCurrentTime((prev) => {
        const next = prev + 1;
        if (next > 60) {
          clearInterval(interval);
          setIsPlaying(false);
          return 0;
        }
        return next;
      });
    }, 1000);
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-5xl font-bold text-white mb-2">AI-Powered Features</h1>
        <p className="text-zinc-400 text-lg">
          Experience the future of music streaming
        </p>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 gap-6">
        {/* Voice Commands Info */}
        <div className="card p-6">
          <div className="flex items-start space-x-4">
            <div className="flex-shrink-0">
              <div className="w-12 h-12 bg-green-500/20 rounded-full flex items-center justify-center">
                <svg className="w-6 h-6 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
            </div>
            <div className="flex-1">
              <h3 className="text-xl font-bold text-white mb-2">Voice Commands</h3>
              <p className="text-zinc-400 mb-4">
                Control Groovex with your voice! Click the microphone button in the bottom right corner.
              </p>
              <div className="bg-zinc-800 rounded-lg p-4 space-y-2">
                <p className="text-sm text-zinc-300 font-medium mb-2">Try saying:</p>
                <div className="grid grid-cols-2 gap-2 text-sm">
                  <div className="flex items-center space-x-2">
                    <span className="text-green-500">•</span>
                    <span className="text-zinc-400">"Hey Groovex, play something chill"</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-500">•</span>
                    <span className="text-zinc-400">"Show recommendations"</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-500">•</span>
                    <span className="text-zinc-400">"Next song"</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-green-500">•</span>
                    <span className="text-zinc-400">"Go to favorites"</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Mood Detection */}
          <MoodWidget />

          {/* Quick Stats */}
          <div className="card p-6">
            <h3 className="text-lg font-bold text-white mb-4">AI Features Overview</h3>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 bg-zinc-800 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">🎤</span>
                  <span className="text-white font-medium">Voice Control</span>
                </div>
                <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-medium">
                  Active
                </span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-zinc-800 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">😊</span>
                  <span className="text-white font-medium">Mood Detection</span>
                </div>
                <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-medium">
                  Active
                </span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-zinc-800 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">✨</span>
                  <span className="text-white font-medium">Smart Playlists</span>
                </div>
                <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-medium">
                  Active
                </span>
              </div>
              
              <div className="flex items-center justify-between p-3 bg-zinc-800 rounded-lg">
                <div className="flex items-center space-x-3">
                  <span className="text-2xl">🎵</span>
                  <span className="text-white font-medium">Synced Lyrics</span>
                </div>
                <span className="px-3 py-1 bg-green-500/20 text-green-400 rounded-full text-xs font-medium">
                  Active
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Smart Playlist Generator */}
        <SmartPlaylistGenerator />

        {/* Lyrics Display Demo */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-2xl font-bold text-white">Karaoke-Style Lyrics</h3>
            {!showLyricsDemo && (
              <button onClick={startLyricsDemo} className="btn-primary">
                🎤 Start Demo
              </button>
            )}
            {showLyricsDemo && (
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => setIsPlaying(!isPlaying)}
                  className="btn-secondary"
                >
                  {isPlaying ? '⏸ Pause' : '▶ Play'}
                </button>
                <button
                  onClick={() => {
                    setShowLyricsDemo(false);
                    setIsPlaying(false);
                    setCurrentTime(0);
                  }}
                  className="btn-secondary"
                >
                  Reset Demo
                </button>
              </div>
            )}
          </div>

          {showLyricsDemo ? (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <div className="lg:col-span-2">
                <LyricsDisplay
                  songId="default"
                  songTitle="Welcome to Groovex"
                  artist="Groovex AI"
                  currentTime={currentTime}
                  isPlaying={isPlaying}
                />
              </div>
              <div className="card p-6">
                <h4 className="text-lg font-bold text-white mb-4">Playback Simulator</h4>
                <div className="space-y-4">
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm text-zinc-400">Time</span>
                      <span className="text-sm text-white font-mono">
                        {Math.floor(currentTime / 60)}:{String(currentTime % 60).padStart(2, '0')}
                      </span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="60"
                      value={currentTime}
                      onChange={(e) => setCurrentTime(parseInt(e.target.value))}
                      className="w-full"
                    />
                  </div>
                  
                  <div className="bg-zinc-800 rounded-lg p-4">
                    <p className="text-xs text-zinc-400 mb-2">Features:</p>
                    <ul className="text-xs text-zinc-300 space-y-1">
                      <li>✓ Auto-scroll to current line</li>
                      <li>✓ Gradient highlighting</li>
                      <li>✓ Progress bar per line</li>
                      <li>✓ Smooth transitions</li>
                    </ul>
                  </div>

                  <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                    <p className="text-xs text-green-400">
                      💡 Lyrics automatically sync with music playback and highlight the current line with a beautiful gradient effect!
                    </p>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="card p-12 flex items-center justify-center">
              <div className="text-center">
                <svg className="w-20 h-20 text-zinc-600 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z" />
                </svg>
                <p className="text-zinc-400 mb-4">
                  See lyrics sync in real-time with karaoke-style highlighting
                </p>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
