import React, { useState, useEffect } from 'react';
import { getTopFavorites } from '../services/api';

interface Favorite {
  song_id: string;
  title: string;
  artist: string;
  total_listen_time: number;
}

const Favorites: React.FC = () => {
  const [favorites, setFavorites] = useState<Favorite[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [topN, setTopN] = useState(10);

  useEffect(() => {
    loadFavorites();
  }, [topN]);

  const loadFavorites = async () => {
    try {
      setLoading(true);
      const data = await getTopFavorites(topN);
      setFavorites(data);
    } catch (err) {
      setError('Failed to load favorites');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-5xl font-bold text-white mb-2">Liked Songs</h1>
          <p className="text-zinc-400 text-lg">Your most played tracks</p>
        </div>
        <div className="flex items-center space-x-3">
          <label htmlFor="topN" className="text-sm font-semibold text-zinc-300">Show top</label>
          <select
            id="topN"
            value={topN}
            onChange={(e) => setTopN(parseInt(e.target.value))}
            className="bg-zinc-800 border border-zinc-700 text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-green-500"
          >
            <option value="5">5</option>
            <option value="10">10</option>
            <option value="20">20</option>
            <option value="50">50</option>
          </select>
          <span className="text-sm font-semibold text-zinc-300">songs</span>
        </div>
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

      {/* Favorites List */}
      <div className="card p-0 overflow-hidden">
        <div className="p-6 border-b border-zinc-800">
          <h2 className="text-2xl font-bold text-white">Your Top Songs</h2>
          <p className="text-zinc-400 text-sm mt-1">Ranked by total listen time</p>
        </div>
        <div className="p-4">
          {loading ? (
            <div className="flex justify-center items-center h-32">
              <div className="w-12 h-12 border-4 border-zinc-800 border-t-green-500 rounded-full animate-spin"></div>
            </div>
          ) : favorites.length === 0 ? (
            <div className="text-center py-12">
              <svg className="w-20 h-20 text-zinc-700 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
              </svg>
              <p className="text-zinc-400 text-lg">No favorite songs yet</p>
              <p className="text-zinc-500 text-sm mt-1">Start listening to build your favorites</p>
            </div>
          ) : (
            <div className="space-y-1">
              {favorites.map((fav, index) => (
                <div key={index} className="song-item p-4 flex items-center justify-between group">
                  <div className="flex items-center space-x-4 flex-1">
                    <span className="text-zinc-400 text-sm w-8">{index + 1}</span>
                    <div className="flex-1">
                      <p className="text-white font-medium group-hover:text-green-500 transition-colors">
                        {fav.title}
                      </p>
                      <p className="text-zinc-400 text-sm">{fav.artist}</p>
                    </div>
                    <div className="flex items-center gap-4">
                      <span className="text-zinc-400 text-sm">
                        {Math.floor(fav.total_listen_time / 60)}:{(fav.total_listen_time % 60).toString().padStart(2, '0')} total
                      </span>
                      <button className="btn-primary text-sm py-2 px-4">
                        Play
                      </button>
                    </div>
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

export default Favorites;