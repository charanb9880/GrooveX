import React, { useState, useEffect } from 'react';
import { getRecommendations } from '../services/api';

interface Recommendation {
  song_id: string;
  title: string;
  artist: string;
  score: number;
  reason: string;
}

const Recommendations: React.FC = () => {
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadRecommendations();
  }, []);

  const loadRecommendations = async () => {
    try {
      setLoading(true);
      const data = await getRecommendations();
      setRecommendations(data);
    } catch (err) {
      setError('Failed to load recommendations');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-5xl font-bold text-white mb-2">Recommendations</h1>
          <p className="text-zinc-400 text-lg">Discover new music</p>
        </div>
        <button onClick={loadRecommendations} className="btn-secondary">
          Refresh
        </button>
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

      {/* Recommendations List */}
      <div className="card p-0 overflow-hidden">
        <div className="p-6 border-b border-zinc-800">
          <h2 className="text-2xl font-bold text-white">For You</h2>
          <p className="text-zinc-400 text-sm mt-1">Based on your listening history</p>
        </div>
        <div className="p-4">
          {loading ? (
            <div className="flex justify-center items-center h-32">
              <div className="w-12 h-12 border-4 border-zinc-800 border-t-green-500 rounded-full animate-spin"></div>
            </div>
          ) : recommendations.length === 0 ? (
            <div className="text-center py-12">
              <svg className="w-20 h-20 text-zinc-700 mx-auto mb-4" fill="currentColor" viewBox="0 0 20 20">
                <path d="M11 3a1 1 0 10-2 0v1a1 1 0 102 0V3zM15.657 5.757a1 1 0 00-1.414-1.414l-.707.707a1 1 0 001.414 1.414l.707-.707zM18 10a1 1 0 01-1 1h-1a1 1 0 110-2h1a1 1 0 011 1zM5.05 6.464A1 1 0 106.464 5.05l-.707-.707a1 1 0 00-1.414 1.414l.707.707zM5 10a1 1 0 01-1 1H3a1 1 0 110-2h1a1 1 0 011 1zM8 16v-1h4v1a2 2 0 11-4 0zM12 14c.015-.34.208-.646.477-.859a4 4 0 10-4.954 0c.27.213.462.519.476.859h4.002z" />
              </svg>
              <p className="text-zinc-400 text-lg">No recommendations available</p>
              <p className="text-zinc-500 text-sm mt-1">Play more songs to get personalized recommendations</p>
            </div>
          ) : (
            <div className="space-y-1">
              {recommendations.map((rec, index) => (
                <div key={index} className="song-item p-4 group">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-4 flex-1">
                      <span className="text-zinc-400 text-sm w-8">{index + 1}</span>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <p className="text-white font-medium group-hover:text-green-500 transition-colors">
                            {rec.title}
                          </p>
                          <span className="px-2 py-0.5 bg-green-500/20 text-green-400 rounded-full text-xs font-semibold">
                            {rec.score}
                          </span>
                        </div>
                        <p className="text-zinc-400 text-sm">{rec.artist}</p>
                        <p className="text-zinc-500 text-xs mt-1">{rec.reason}</p>
                      </div>
                    </div>
                    <div className="flex gap-2 ml-4">
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

export default Recommendations;