import React, { useState } from 'react';
import { searchSongs } from '../services/api';

interface Song {
  song_id?: string;
  title: string;
  artist: string;
  duration: number;
}

const Explorer: React.FC = () => {
  const [searchParams, setSearchParams] = useState({
    genre: '',
    subgenre: '',
    mood: '',
    artist: ''
  });
  const [songs, setSongs] = useState<Song[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setLoading(true);
      const results = await searchSongs(searchParams);
      setSongs(results);
    } catch (err) {
      setError('Failed to search songs');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-5xl font-bold text-white mb-2">Search & Explore</h1>
        <p className="text-zinc-400 text-lg">Find songs by genre, mood, and more</p>
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

      {/* Search Form */}
      <div className="card p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Search Criteria</h2>
        <form onSubmit={handleSearch} className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div>
            <label htmlFor="genre" className="block text-sm font-semibold text-zinc-300 mb-2">Genre</label>
            <input
              type="text"
              id="genre"
              value={searchParams.genre}
              onChange={(e) => setSearchParams({...searchParams, genre: e.target.value})}
              className="input-field"
              placeholder="Rock, Pop, Jazz..."
            />
          </div>
          <div>
            <label htmlFor="subgenre" className="block text-sm font-semibold text-zinc-300 mb-2">Subgenre</label>
            <input
              type="text"
              id="subgenre"
              value={searchParams.subgenre}
              onChange={(e) => setSearchParams({...searchParams, subgenre: e.target.value})}
              className="input-field"
              placeholder="Alternative, Indie..."
            />
          </div>
          <div>
            <label htmlFor="mood" className="block text-sm font-semibold text-zinc-300 mb-2">Mood</label>
            <input
              type="text"
              id="mood"
              value={searchParams.mood}
              onChange={(e) => setSearchParams({...searchParams, mood: e.target.value})}
              className="input-field"
              placeholder="Happy, Chill, Energetic..."
            />
          </div>
          <div>
            <label htmlFor="artist" className="block text-sm font-semibold text-zinc-300 mb-2">Artist</label>
            <input
              type="text"
              id="artist"
              value={searchParams.artist}
              onChange={(e) => setSearchParams({...searchParams, artist: e.target.value})}
              className="input-field"
              placeholder="Artist name..."
            />
          </div>
          <div className="md:col-span-4 flex justify-end">
            <button type="submit" disabled={loading} className="btn-primary">
              {loading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>
      </div>

      {/* Search Results */}
      <div className="card p-0 overflow-hidden">
        <div className="p-6 border-b border-zinc-800">
          <h2 className="text-2xl font-bold text-white">Search Results</h2>
          <p className="text-zinc-400 text-sm mt-1">{songs.length} songs found</p>
        </div>
        <div className="p-4">
          {loading ? (
            <div className="flex justify-center items-center h-32">
              <div className="w-12 h-12 border-4 border-zinc-800 border-t-green-500 rounded-full animate-spin"></div>
            </div>
          ) : songs.length === 0 ? (
            <div className="text-center py-12">
              <svg className="w-20 h-20 text-zinc-700 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9 9a2 2 0 114 0 2 2 0 01-4 0z" />
                <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm1-13a4 4 0 00-3.446 6.032l-2.261 2.26a1 1 0 101.414 1.415l2.261-2.261A4 4 0 1011 5z" clipRule="evenodd" />
              </svg>
              <p className="text-zinc-400 text-lg">No songs found</p>
              <p className="text-zinc-500 text-sm mt-1">Try adjusting your search criteria</p>
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
                  <div className="flex gap-2 ml-4">
                    <button className="btn-primary text-sm py-2 px-4">
                      Play
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

export default Explorer;