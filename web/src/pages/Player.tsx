import React, { useState } from 'react';
import { usePlayer } from '../contexts/PlayerContext';
import AudioVisualizer from '../components/AudioVisualizer';

const Player: React.FC = () => {
  const {
    currentSong,
    isPlaying,
    currentTime,
    duration,
    volume,
    playlist,
    currentIndex,
    play,
    togglePlayPause,
    next,
    previous,
    setVolume,
    seek,
  } = usePlayer();
  
  const [error, setError] = useState<string | null>(null);

  const formatTime = (seconds: number) => {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-5xl font-bold text-white mb-2">Now Playing</h1>
        <p className="text-zinc-400 text-lg">Your music player</p>
      </div>
      
      {error && (
        <div className="card p-6 bg-red-900/20 border-red-800">
          <div className="flex items-center space-x-3">
            <svg className="w-8 h-8 text-red-500" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <div>
              <h3 className="font-bold text-red-400 text-lg">Error</h3>
              <p className="text-red-300">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Current Song */}
      <div className="card p-8">
        <h2 className="text-2xl font-bold text-white mb-6">Currently Playing</h2>
        {currentSong ? (
          <div className="space-y-6">
            <div>
              <h3 className="text-4xl font-bold text-white mb-2">{currentSong.title}</h3>
              <p className="text-xl text-zinc-400">{currentSong.artist}</p>
            </div>
            
            {/* Audio Visualizer */}
            <AudioVisualizer />
            
            {/* Progress Bar */}
            <div className="space-y-2">
              <input
                type="range"
                min="0"
                max={duration || 100}
                value={currentTime}
                onChange={(e) => seek(parseFloat(e.target.value))}
                className="w-full h-2 bg-zinc-700 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, #22c55e 0%, #22c55e ${(currentTime / duration) * 100}%, #3f3f46 ${(currentTime / duration) * 100}%, #3f3f46 100%)`
                }}
              />
              <div className="flex justify-between text-sm text-zinc-400">
                <span>{formatTime(currentTime)}</span>
                <span>{formatTime(duration)}</span>
              </div>
            </div>
            
            {/* Playback Controls */}
            <div className="flex items-center justify-center gap-4">
              <button onClick={previous} className="btn-secondary px-6 py-3">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M8.445 14.832A1 1 0 0010 14v-2.798l5.445 3.63A1 1 0 0017 14V6a1 1 0 00-1.555-.832L10 8.798V6a1 1 0 00-1.555-.832l-6 4a1 1 0 000 1.664l6 4z" />
                </svg>
              </button>
              
              <button onClick={togglePlayPause} className="btn-primary px-8 py-4 text-lg">
                {isPlaying ? (
                  <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                ) : (
                  <svg className="w-8 h-8" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                  </svg>
                )}
              </button>
              
              <button onClick={next} className="btn-secondary px-6 py-3">
                <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M4.555 5.168A1 1 0 003 6v8a1 1 0 001.555.832L10 11.202V14a1 1 0 001.555.832l6-4a1 1 0 000-1.664l-6-4A1 1 0 0010 6v2.798l-5.445-3.63z" />
                </svg>
              </button>
            </div>
            
            {/* Volume Control */}
            <div className="flex items-center gap-4">
              <svg className="w-5 h-5 text-zinc-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M9.383 3.076A1 1 0 0110 4v12a1 1 0 01-1.707.707L4.586 13H2a1 1 0 01-1-1V8a1 1 0 011-1h2.586l3.707-3.707a1 1 0 011.09-.217zM14.657 2.929a1 1 0 011.414 0A9.972 9.972 0 0119 10a9.972 9.972 0 01-2.929 7.071 1 1 0 01-1.414-1.414A7.971 7.971 0 0017 10c0-2.21-.894-4.208-2.343-5.657a1 1 0 010-1.414zm-2.829 2.828a1 1 0 011.415 0A5.983 5.983 0 0115 10a5.984 5.984 0 01-1.757 4.243 1 1 0 01-1.415-1.415A3.984 3.984 0 0013 10a3.983 3.983 0 00-1.172-2.828 1 1 0 010-1.415z" clipRule="evenodd" />
              </svg>
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={volume}
                onChange={(e) => setVolume(parseFloat(e.target.value))}
                className="flex-1 h-2 bg-zinc-700 rounded-lg appearance-none cursor-pointer"
                style={{
                  background: `linear-gradient(to right, #22c55e 0%, #22c55e ${volume * 100}%, #3f3f46 ${volume * 100}%, #3f3f46 100%)`
                }}
              />
              <span className="text-sm text-zinc-400 w-12">{Math.round(volume * 100)}%</span>
            </div>
          </div>
        ) : (
          <div className="text-center py-12">
            <svg className="w-20 h-20 text-zinc-700 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
            </svg>
            <p className="text-zinc-400 mb-6 text-lg">No song is currently playing</p>
            <button onClick={() => play(playlist[0], 0)} className="btn-primary">
              Play First Song
            </button>
          </div>
        )}
      </div>

      {/* Playlist Songs */}
      <div className="card p-0 overflow-hidden">
        <div className="p-6 border-b border-zinc-800">
          <h2 className="text-2xl font-bold text-white">Playlist</h2>
          <p className="text-zinc-400 text-sm mt-1">{playlist.length} songs</p>
        </div>
        <div className="p-4">
          <div className="space-y-1">
            {playlist.map((song, index) => (
              <div 
                key={song.id} 
                onClick={() => play(song, index)}
                className={`song-item p-3 flex items-center justify-between group cursor-pointer ${
                  currentSong?.id === song.id ? 'bg-green-500/10 border-l-4 border-green-500' : ''
                }`}
              >
                <div className="flex items-center space-x-4 flex-1">
                  <span className="text-zinc-400 text-sm w-6">{index + 1}</span>
                  {currentSong?.id === song.id && isPlaying ? (
                    <svg className="w-5 h-5 text-green-500 animate-pulse" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zM7 8a1 1 0 012 0v4a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v4a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                  ) : (
                    <svg className="w-5 h-5 text-zinc-600 group-hover:text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM9.555 7.168A1 1 0 008 8v4a1 1 0 001.555.832l3-2a1 1 0 000-1.664l-3-2z" clipRule="evenodd" />
                    </svg>
                  )}
                  <div className="flex-1">
                    <p className={`font-medium group-hover:text-green-500 transition-colors ${
                      currentSong?.id === song.id ? 'text-green-500' : 'text-white'
                    }`}>
                      {song.title}
                    </p>
                    <p className="text-zinc-400 text-sm">{song.artist}</p>
                  </div>
                </div>
                <span className="text-zinc-400 text-sm">
                  {formatTime(song.duration)}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
      
      {/* Up Next */}
      <div className="card p-0 overflow-hidden">
        <div className="p-6 border-b border-zinc-800">
          <h2 className="text-2xl font-bold text-white">Up Next</h2>
          <p className="text-zinc-400 text-sm mt-1">Coming up after current song</p>
        </div>
        <div className="p-4">
          {currentIndex < playlist.length - 1 ? (
            <div className="space-y-1">
              {playlist.slice(currentIndex + 1, currentIndex + 4).map((song, index) => (
                <div key={song.id} className="song-item p-3 flex items-center group">
                  <span className="text-zinc-400 text-sm w-6 mr-4">{index + 1}</span>
                  <div className="flex-1">
                    <p className="text-white font-medium group-hover:text-green-500 transition-colors">
                      {song.title}
                    </p>
                    <p className="text-zinc-400 text-sm">{song.artist}</p>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <p className="text-zinc-400">No upcoming songs</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Player;