import React, { useState, useEffect } from 'react';
import { getSnapshot } from '../services/api';
import { Link } from 'react-router-dom';

interface SnapshotData {
  timestamp: string;
  system_overview: {
    total_songs_in_playlist: number;
    total_duration_seconds: number;
    average_song_duration: number;
    total_playback_history: number;
  };
  top_5_longest_songs: Array<{
    song_id?: string;
    title: string;
    artist: string;
    duration: number;
  }>;
  recently_played_songs: Array<{
    song_id?: string;
    title: string;
    artist: string;
    duration: number;
  }>;
  song_count_by_rating: Record<number, number>;
  extremes: {
    shortest_song: {
      title: string | null;
      duration: number | null;
    };
    longest_song: {
      title: string | null;
      duration: number | null;
    };
  };
}

const Dashboard: React.FC = () => {
  const [snapshot, setSnapshot] = useState<SnapshotData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadSnapshot();
  }, []);

  const loadSnapshot = async () => {
    try {
      setLoading(true);
      const data = await getSnapshot();
      setSnapshot(data);
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handlePlayDemo = async () => {
    try {
      // This would play a demo song
      // For now, just reload the snapshot to show updated data
      await loadSnapshot();
    } catch (err) {
      setError('Failed to play demo');
      console.error(err);
    }
  };

  const handleRunRecommendations = async () => {
    try {
      // This would run recommendations
      // For now, just reload the snapshot to show updated data
      await loadSnapshot();
    } catch (err) {
      setError('Failed to run recommendations');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center h-96 space-y-4">
        <div className="w-16 h-16 border-4 border-zinc-800 border-t-green-500 rounded-full animate-spin"></div>
        <p className="text-zinc-400 font-medium">Loading your music...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card p-6 bg-red-900/20 border-red-800">
        <div className="flex items-center space-x-3">
          <svg className="w-8 h-8 text-red-500" fill="currentColor" viewBox="0 0 20 20">
            <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
          </svg>
          <div>
            <h3 className="font-bold text-red-400 text-lg">Error Loading Dashboard</h3>
            <p className="text-red-300">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  if (!snapshot) {
    return <div>No data available</div>;
  }

  // Format seconds to HH:MM:SS
  const formatDuration = (seconds: number): string => {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    return `${hrs.toString().padStart(2, '0')}:${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-5xl font-bold text-white mb-2">Good evening</h1>
          <p className="text-zinc-400 text-lg">Your music stats</p>
        </div>
        <div className="flex gap-3">
          <button onClick={handlePlayDemo} className="btn-primary">
            Play Demo
          </button>
          <button onClick={handleRunRecommendations} className="btn-secondary">
            Get Recommendations
          </button>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div className="stat-card">
          <p className="text-zinc-400 text-sm mb-2">Total Songs</p>
          <p className="text-4xl font-bold text-white">
            {snapshot.system_overview.total_songs_in_playlist}
          </p>
        </div>

        <div className="stat-card">
          <p className="text-zinc-400 text-sm mb-2">Total Duration</p>
          <p className="text-2xl font-bold text-white">
            {formatDuration(snapshot.system_overview.total_duration_seconds)}
          </p>
        </div>

        <div className="stat-card">
          <p className="text-zinc-400 text-sm mb-2">Avg Duration</p>
          <p className="text-4xl font-bold text-white">
            {Math.round(snapshot.system_overview.average_song_duration)}s
          </p>
        </div>

        <div className="stat-card">
          <p className="text-zinc-400 text-sm mb-2">Plays</p>
          <p className="text-4xl font-bold text-white">
            {snapshot.system_overview.total_playback_history}
          </p>
        </div>
      </div>

      {/* AI Features Highlight */}
      <Link to="/ai-features" className="block">
        <div className="card p-6 bg-gradient-to-r from-green-500/20 to-blue-500/20 border border-green-500/30 hover:border-green-500/50 transition-all duration-300 cursor-pointer group">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-12 h-12 bg-green-500/30 rounded-full flex items-center justify-center group-hover:bg-green-500/40 transition-all">
                <svg className="w-6 h-6 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M13 7H7v6h6V7z" />
                  <path fillRule="evenodd" d="M7 2a1 1 0 012 0v1h2V2a1 1 0 112 0v1h2a2 2 0 012 2v2h1a1 1 0 110 2h-1v2h1a1 1 0 110 2h-1v2a2 2 0 01-2 2h-2v1a1 1 0 11-2 0v-1H9v1a1 1 0 11-2 0v-1H5a2 2 0 01-2-2v-2H2a1 1 0 110-2h1V9H2a1 1 0 010-2h1V5a2 2 0 012-2h2V2zM5 5h10v10H5V5z" clipRule="evenodd" />
                </svg>
              </div>
              <div>
                <h3 className="text-xl font-bold text-white mb-1 group-hover:text-green-400 transition-colors">✨ AI-Powered Features</h3>
                <p className="text-zinc-400 text-sm">Voice commands, mood detection, smart playlists, and synced lyrics</p>
              </div>
            </div>
            <svg className="w-6 h-6 text-zinc-400 group-hover:text-green-400 transition-colors" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clipRule="evenodd" />
            </svg>
          </div>
        </div>
      </Link>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Songs */}
        <div className="card p-0 overflow-hidden">
          <div className="p-6 border-b border-zinc-800">
            <h3 className="text-2xl font-bold text-white">Top Longest Songs</h3>
            <p className="text-zinc-400 text-sm mt-1">Your extended tracks</p>
          </div>
          <div className="p-4">
            <div className="space-y-1">
              {snapshot.top_5_longest_songs.map((song, index) => (
                <div key={index} className="song-item p-3 flex items-center justify-between group">
                  <div className="flex items-center space-x-4 flex-1">
                    <span className="text-zinc-400 text-sm w-6">{index + 1}</span>
                    <div className="flex-1">
                      <p className="text-white font-medium group-hover:text-green-500 transition-colors">
                        {song.title}
                      </p>
                      <p className="text-zinc-400 text-sm">{song.artist}</p>
                    </div>
                  </div>
                  <span className="text-zinc-400 text-sm">
                    {Math.floor(song.duration / 60)}:{(song.duration % 60).toString().padStart(2, '0')}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Recently Played */}
        <div className="card p-0 overflow-hidden">
          <div className="p-6 border-b border-zinc-800">
            <h3 className="text-2xl font-bold text-white">Recently Played</h3>
            <p className="text-zinc-400 text-sm mt-1">Your latest tracks</p>
          </div>
          <div className="p-4">
            <div className="space-y-1">
              {snapshot.recently_played_songs.map((song, index) => (
                <div key={index} className="song-item p-3 flex items-center justify-between group">
                  <div className="flex items-center space-x-4 flex-1">
                    <span className="text-zinc-400 text-sm w-6">{index + 1}</span>
                    <div className="flex-1">
                      <p className="text-white font-medium group-hover:text-green-500 transition-colors">
                        {song.title}
                      </p>
                      <p className="text-zinc-400 text-sm">{song.artist}</p>
                    </div>
                  </div>
                  <span className="text-zinc-400 text-sm">
                    {Math.floor(song.duration / 60)}:{(song.duration % 60).toString().padStart(2, '0')}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Ratings */}
        <div className="card p-6">
          <h3 className="text-2xl font-bold text-white mb-6">Song Ratings</h3>
          <div className="space-y-4">
            {Object.entries(snapshot.song_count_by_rating)
              .sort(([a], [b]) => parseInt(b) - parseInt(a))
              .map(([rating, count]) => (
                <div key={rating} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <span className="text-white font-bold">{rating} ★</span>
                      <span className="text-zinc-400 text-sm">({count} songs)</span>
                    </div>
                    <span className="text-zinc-400 text-sm">
                      {Math.round((count / Object.values(snapshot.song_count_by_rating).reduce((a, b) => a + b, 0)) * 100)}%
                    </span>
                  </div>
                  <div className="h-2 bg-zinc-800 rounded-full overflow-hidden">
                    <div 
                      className="h-full bg-green-500 rounded-full transition-all duration-500" 
                      style={{ width: `${(count / Math.max(...Object.values(snapshot.song_count_by_rating))) * 100}%` }}
                    ></div>
                  </div>
                </div>
              ))}
          </div>
        </div>

        {/* Extremes */}
        <div className="card p-6">
          <h3 className="text-2xl font-bold text-white mb-6">Extremes</h3>
          <div className="space-y-4">
            <div className="bg-zinc-800/50 rounded-lg p-6">
              <p className="text-zinc-400 text-sm mb-2">Shortest Song</p>
              {snapshot.extremes.shortest_song.title ? (
                <div>
                  <p className="text-xl font-bold text-white mb-1">{snapshot.extremes.shortest_song.title}</p>
                  <p className="text-green-500 font-semibold">{snapshot.extremes.shortest_song.duration}s</p>
                </div>
              ) : (
                <p className="text-zinc-500">No songs available</p>
              )}
            </div>
            <div className="bg-zinc-800/50 rounded-lg p-6">
              <p className="text-zinc-400 text-sm mb-2">Longest Song</p>
              {snapshot.extremes.longest_song.title ? (
                <div>
                  <p className="text-xl font-bold text-white mb-1">{snapshot.extremes.longest_song.title}</p>
                  <p className="text-green-500 font-semibold">{snapshot.extremes.longest_song.duration}s</p>
                </div>
              ) : (
                <p className="text-zinc-500">No songs available</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;