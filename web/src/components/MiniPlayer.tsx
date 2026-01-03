import { usePlayer } from '../contexts/PlayerContext';
import { useNavigate } from 'react-router-dom';
import { useState } from 'react';

export default function MiniPlayer() {
  const { currentSong, isPlaying, togglePlayPause, next } = usePlayer();
  const navigate = useNavigate();
  const [showHelp, setShowHelp] = useState(false);

  if (!currentSong) {
    return null;
  }

  return (
    <>
      <div className="fixed bottom-0 left-64 right-0 bg-zinc-900 border-t border-zinc-800 px-6 py-4 z-40">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          {/* Song Info */}
          <div 
            className="flex items-center space-x-4 flex-1 cursor-pointer hover:text-green-500 transition-colors"
            onClick={() => navigate('/player')}
          >
            <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-600 rounded-lg flex items-center justify-center flex-shrink-0">
              <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z" />
              </svg>
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-white font-medium truncate">{currentSong.title}</p>
              <p className="text-zinc-400 text-sm truncate">{currentSong.artist}</p>
            </div>
          </div>

          {/* Controls */}
          <div className="flex items-center space-x-2">
            <button
              onClick={togglePlayPause}
              className="w-10 h-10 rounded-full bg-white hover:bg-gray-100 flex items-center justify-center transition-colors"
            >
              {isPlaying ? (
                <svg className="w-5 h-5 text-black" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                </svg>
              ) : (
                <svg className="w-5 h-5 text-black ml-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                </svg>
              )}
            </button>
            <button
              onClick={next}
              className="w-10 h-10 rounded-full hover:bg-zinc-800 flex items-center justify-center transition-colors"
            >
              <svg className="w-5 h-5 text-white" fill="currentColor" viewBox="0 0 20 20">
                <path d="M4.555 5.168A1 1 0 003 6v8a1 1 0 001.555.832L10 11.202V14a1 1 0 001.555.832l6-4a1 1 0 000-1.664l-6-4A1 1 0 0010 6v2.798l-5.445-3.63z" />
              </svg>
            </button>
            
            {/* Keyboard Shortcuts Button */}
            <button
              onClick={() => setShowHelp(!showHelp)}
              className="w-10 h-10 rounded-full hover:bg-zinc-800 flex items-center justify-center transition-colors text-zinc-400 hover:text-white"
              title="Keyboard Shortcuts"
            >
              ⌨️
            </button>
          </div>
        </div>
      </div>

      {/* Keyboard Shortcuts Help */}
      {showHelp && (
        <div className="fixed inset-0 bg-black/70 z-50 flex items-center justify-center" onClick={() => setShowHelp(false)}>
          <div className="bg-zinc-900 border border-zinc-700 rounded-lg p-6 max-w-md" onClick={(e) => e.stopPropagation()}>
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-xl font-bold text-white">⌨️ Keyboard Shortcuts</h3>
              <button onClick={() => setShowHelp(false)} className="text-zinc-400 hover:text-white">
                ✕
              </button>
            </div>
            <div className="space-y-3">
              <div className="flex items-center justify-between text-sm">
                <span className="text-zinc-400">Play/Pause</span>
                <kbd className="px-2 py-1 bg-zinc-800 rounded text-white">Space</kbd>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-zinc-400">Next Track</span>
                <kbd className="px-2 py-1 bg-zinc-800 rounded text-white">→</kbd>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-zinc-400">Previous Track</span>
                <kbd className="px-2 py-1 bg-zinc-800 rounded text-white">←</kbd>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-zinc-400">Volume Up</span>
                <kbd className="px-2 py-1 bg-zinc-800 rounded text-white">↑</kbd>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-zinc-400">Volume Down</span>
                <kbd className="px-2 py-1 bg-zinc-800 rounded text-white">↓</kbd>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-zinc-400">Mute/Unmute</span>
                <kbd className="px-2 py-1 bg-zinc-800 rounded text-white">M</kbd>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-zinc-400">Go to Player</span>
                <kbd className="px-2 py-1 bg-zinc-800 rounded text-white">P</kbd>
              </div>
              <div className="flex items-center justify-between text-sm">
                <span className="text-zinc-400">Go Home</span>
                <kbd className="px-2 py-1 bg-zinc-800 rounded text-white">H</kbd>
              </div>
            </div>
            <div className="mt-4 pt-4 border-t border-zinc-800">
              <p className="text-xs text-zinc-500">💡 Tip: Use voice commands with the microphone button!</p>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
