import React, { useState, useEffect } from 'react';
import { getPlaylist, addSongToPlaylist, deleteSongFromPlaylist, moveSongInPlaylist, reversePlaylist } from '../services/api';

interface Song {
  index?: number;
  song_id?: string;
  title: string;
  artist: string;
  duration: number;
}

const Playlists: React.FC = () => {
  const [songs, setSongs] = useState<Song[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [newSong, setNewSong] = useState({ title: '', artist: '', duration: 0 });

  useEffect(() => {
    loadPlaylist();
  }, []);

  const loadPlaylist = async () => {
    try {
      setLoading(true);
      const data = await getPlaylist('main');
      setSongs(data.songs);
    } catch (err) {
      setError('Failed to load playlist');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddSong = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await addSongToPlaylist('main', {
        title: newSong.title,
        artist: newSong.artist,
        duration: newSong.duration
      });
      setNewSong({ title: '', artist: '', duration: 0 });
      await loadPlaylist();
    } catch (err) {
      setError('Failed to add song');
      console.error(err);
    }
  };

  const handleDeleteSong = async (index: number) => {
    try {
      await deleteSongFromPlaylist('main', index);
      await loadPlaylist();
    } catch (err) {
      setError('Failed to delete song');
      console.error(err);
    }
  };

  const handleMoveSong = async (fromIndex: number, toIndex: number) => {
    try {
      await moveSongInPlaylist('main', fromIndex, toIndex);
      await loadPlaylist();
    } catch (err) {
      setError('Failed to move song');
      console.error(err);
    }
  };

  const handleReversePlaylist = async () => {
    try {
      await reversePlaylist('main');
      await loadPlaylist();
    } catch (err) {
      setError('Failed to reverse playlist');
      console.error(err);
    }
  };

  if (loading) {
    return (
      <div className="flex flex-col justify-center items-center h-96 space-y-4">
        <div className="w-16 h-16 border-4 border-zinc-800 border-t-green-500 rounded-full animate-spin"></div>
        <p className="text-zinc-400 font-medium">Loading playlist...</p>
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
            <h3 className="font-bold text-red-400 text-lg">Error</h3>
            <p className="text-red-300">{error}</p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-5xl font-bold text-white mb-2">Your Library</h1>
          <p className="text-zinc-400 text-lg">{songs.length} songs</p>
        </div>
        <button onClick={handleReversePlaylist} className="btn-secondary">
          Reverse Order
        </button>
      </div>

      {/* Add Song Form */}
      <div className="card p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Add New Song</h2>
        <form onSubmit={handleAddSong} className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label htmlFor="title" className="block text-sm font-semibold text-zinc-300 mb-2">Song Title</label>
            <input
              type="text"
              id="title"
              value={newSong.title}
              onChange={(e) => setNewSong({...newSong, title: e.target.value})}
              className="input-field"
              placeholder="Enter song title"
              required
            />
          </div>
          <div>
            <label htmlFor="artist" className="block text-sm font-semibold text-zinc-300 mb-2">Artist Name</label>
            <input
              type="text"
              id="artist"
              value={newSong.artist}
              onChange={(e) => setNewSong({...newSong, artist: e.target.value})}
              className="input-field"
              placeholder="Enter artist name"
              required
            />
          </div>
          <div>
            <label htmlFor="duration" className="block text-sm font-semibold text-zinc-300 mb-2">Duration (seconds)</label>
            <input
              type="number"
              id="duration"
              value={newSong.duration || ''}
              onChange={(e) => setNewSong({...newSong, duration: parseInt(e.target.value) || 0})}
              className="input-field"
              placeholder="180"
              required
            />
          </div>
          <div className="flex items-end">
            <button type="submit" className="w-full btn-primary">
              Add Song
            </button>
          </div>
        </form>
      </div>

      {/* Playlist Songs */}
      <div className="card p-0 overflow-hidden">
        <div className="p-6 border-b border-zinc-800">
          <h2 className="text-2xl font-bold text-white">Playlist</h2>
          <p className="text-zinc-400 text-sm mt-1">Manage your songs</p>
        </div>
        <div className="p-4">
          {songs.length === 0 ? (
            <div className="text-center py-16">
              <div className="flex flex-col items-center space-y-4">
                <svg className="w-20 h-20 text-zinc-700" fill="currentColor" viewBox="0 0 20 20">
                  <path d="M18 3a1 1 0 00-1.196-.98l-10 2A1 1 0 006 5v9.114A4.369 4.369 0 005 14c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V7.82l8-1.6v5.894A4.37 4.37 0 0015 12c-1.657 0-3 .895-3 2s1.343 2 3 2 3-.895 3-2V3z" />
                </svg>
                <div>
                  <p className="text-zinc-400 font-semibold text-lg">No songs yet</p>
                  <p className="text-zinc-500 text-sm mt-1">Add your first song to get started</p>
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-1">
              {songs.map((song, index) => (
                <div key={index} className="song-item p-4 flex items-center justify-between group">
                  <div className="flex items-center space-x-4 flex-1">
                    <span className="text-zinc-400 text-sm w-8">{index + 1}</span>
                    <div className="flex-1">
                      <p className="text-white font-medium group-hover:text-green-500 transition-colors">
                        {song.title}
                      </p>
                      <p className="text-zinc-400 text-sm">{song.artist}</p>
                    </div>
                    <span className="text-zinc-400 text-sm">
                      {Math.floor(song.duration / 60)}:{(song.duration % 60).toString().padStart(2, '0')}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2 ml-4">
                    <button
                      onClick={() => handleMoveSong(index, Math.max(0, index - 1))}
                      disabled={index === 0}
                      className="p-2 text-zinc-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                      title="Move up"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clipRule="evenodd" />
                      </svg>
                    </button>
                    <button
                      onClick={() => handleMoveSong(index, Math.min(songs.length - 1, index + 1))}
                      disabled={index === songs.length - 1}
                      className="p-2 text-zinc-400 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
                      title="Move down"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
                      </svg>
                    </button>
                    <button
                      onClick={() => handleDeleteSong(index)}
                      className="p-2 text-zinc-400 hover:text-red-500 transition-colors"
                      title="Delete song"
                    >
                      <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Playlists;