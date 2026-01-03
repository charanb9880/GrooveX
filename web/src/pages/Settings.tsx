import React, { useState, useEffect } from 'react';
import { healthCheck } from '../services/api';

const Settings: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');
  const [dedupePolicy, setDedupePolicy] = useState<'first' | 'latest'>('first');
  const [skippedTrackerCapacity, setSkippedTrackerCapacity] = useState(10);

  useEffect(() => {
    checkApiStatus();
  }, []);

  const checkApiStatus = async () => {
    try {
      const result = await healthCheck();
      setApiStatus(result.status === 'ok' ? 'online' : 'offline');
    } catch (err) {
      setApiStatus('offline');
    }
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-5xl font-bold text-white mb-2">Settings</h1>
        <p className="text-zinc-400 text-lg">Manage your preferences</p>
      </div>
      
      {/* API Status */}
      <div className="card p-6">
        <h2 className="text-2xl font-bold text-white mb-6">System Status</h2>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className={`h-4 w-4 rounded-full ${
              apiStatus === 'online' ? 'bg-green-500 animate-pulse' : 
              apiStatus === 'offline' ? 'bg-red-500' : 'bg-yellow-500'
            }`}></div>
            <span className="text-white font-semibold text-lg">
              {apiStatus === 'checking' ? 'Checking connection...' : 
               apiStatus === 'online' ? 'Connected' : 'Disconnected'}
            </span>
          </div>
          <button onClick={checkApiStatus} className="btn-secondary">
            Refresh Status
          </button>
        </div>
      </div>

      {/* Dedupe Policy */}
      <div className="card p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Duplicate Handling</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-zinc-300 mb-4">
              Deduplication Policy
            </label>
            <div className="space-y-3">
              <label className="flex items-center p-4 bg-zinc-800 hover:bg-zinc-700 rounded-lg cursor-pointer transition-colors">
                <input
                  id="dedupe-first"
                  name="dedupe-policy"
                  type="radio"
                  checked={dedupePolicy === 'first'}
                  onChange={() => setDedupePolicy('first')}
                  className="w-4 h-4 text-green-500 focus:ring-green-500 border-zinc-600 bg-zinc-700"
                />
                <div className="ml-3">
                  <span className="block text-white font-medium">Keep First Occurrence</span>
                  <span className="text-zinc-400 text-sm">Original song will be preserved</span>
                </div>
              </label>
              <label className="flex items-center p-4 bg-zinc-800 hover:bg-zinc-700 rounded-lg cursor-pointer transition-colors">
                <input
                  id="dedupe-latest"
                  name="dedupe-policy"
                  type="radio"
                  checked={dedupePolicy === 'latest'}
                  onChange={() => setDedupePolicy('latest')}
                  className="w-4 h-4 text-green-500 focus:ring-green-500 border-zinc-600 bg-zinc-700"
                />
                <div className="ml-3">
                  <span className="block text-white font-medium">Keep Latest Occurrence</span>
                  <span className="text-zinc-400 text-sm">Most recent song will be kept</span>
                </div>
              </label>
            </div>
          </div>
        </div>
      </div>

      {/* Skipped Tracker */}
      <div className="card p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Recently Skipped Tracker</h2>
        <div className="space-y-4">
          <div>
            <label htmlFor="capacity" className="block text-sm font-semibold text-zinc-300 mb-4">
              Capacity (number of songs to track)
            </label>
            <input
              type="range"
              id="capacity"
              min="1"
              max="50"
              value={skippedTrackerCapacity}
              onChange={(e) => setSkippedTrackerCapacity(parseInt(e.target.value))}
              className="w-full h-2 bg-zinc-700 rounded-lg appearance-none cursor-pointer accent-green-500"
            />
            <div className="flex justify-between text-sm text-zinc-400 mt-3">
              <span>1 song</span>
              <span className="text-white font-bold text-lg">{skippedTrackerCapacity} songs</span>
              <span>50 songs</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;