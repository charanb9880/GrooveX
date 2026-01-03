/**
 * Voice Control Component
 * 
 * Features:
 * - Optimized Web Speech API with interim results for faster feedback
 * - Auto-restart for continuous listening
 * - Visual feedback showing what's being heard in real-time
 * - Support for wake word "Hey Groovex"
 * 
 * Performance Improvements:
 * - Interim results enabled for instant feedback
 * - Auto-restart prevents connection drops
 * - Better error handling with specific messages
 * - Sound and speech detection events for better UX
 */

import { useState, useEffect } from 'react';
import { voiceCommandService } from '../services/voiceCommands';
import { usePlayer } from '../contexts/PlayerContext';
import { useNavigate } from 'react-router-dom';

export default function VoiceControl() {
  const [isListening, setIsListening] = useState(false);
  const [status, setStatus] = useState('');
  const [lastCommand, setLastCommand] = useState('');
  const [isSupported, setIsSupported] = useState(true);
  const navigate = useNavigate();
  const player = usePlayer();

  useEffect(() => {
    setIsSupported(voiceCommandService.isSupported());

    // Setup callbacks
    voiceCommandService.onCommand((command, message) => {
      setLastCommand(message);
      handleCommand(command);
      
      // Clear message after 3 seconds
      setTimeout(() => setLastCommand(''), 3000);
    });

    voiceCommandService.onError((error) => {
      setStatus(`Error: ${error}`);
      setTimeout(() => setStatus(''), 3000);
    });

    voiceCommandService.onStatus((status) => {
      setStatus(status);
    });

    return () => {
      voiceCommandService.stop();
    };
  }, []);

  const handleCommand = (command: string) => {
    switch (command) {
      case 'play':
        player.togglePlayPause();
        console.log('Play command received');
        break;
      case 'pause':
        player.pause();
        console.log('Pause command received');
        break;
      case 'next':
        player.next();
        console.log('Next command received');
        break;
      case 'previous':
        player.previous();
        console.log('Previous command received');
        break;
      case 'volume_up':
        player.increaseVolume();
        console.log('Volume up');
        break;
      case 'volume_down':
        player.decreaseVolume();
        console.log('Volume down');
        break;
      case 'shuffle':
        console.log('Shuffle enabled');
        break;
      case 'play_chill':
      case 'play_energetic':
      case 'play_happy':
      case 'play_sad':
        navigate('/recommendations');
        break;
      case 'recommendations':
        navigate('/recommendations');
        break;
      case 'favorites':
        navigate('/favorites');
        break;
      case 'home':
        navigate('/');
        break;
    }
  };

  const toggleListening = () => {
    if (isListening) {
      voiceCommandService.stop();
      setIsListening(false);
    } else {
      voiceCommandService.start();
      setIsListening(true);
    }
  };

  if (!isSupported) {
    return null;
  }

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Voice Control Button */}
      <button
        onClick={toggleListening}
        className={`w-16 h-16 rounded-full shadow-2xl flex items-center justify-center transition-all duration-300 ${
          isListening
            ? 'bg-green-500 animate-pulse scale-110'
            : 'bg-zinc-800 hover:bg-zinc-700 hover:scale-105'
        }`}
        title="Voice Commands"
      >
        <svg
          className={`w-8 h-8 ${isListening ? 'text-black' : 'text-white'}`}
          fill="currentColor"
          viewBox="0 0 20 20"
        >
          <path
            fillRule="evenodd"
            d="M7 4a3 3 0 016 0v4a3 3 0 11-6 0V4zm4 10.93A7.001 7.001 0 0017 8a1 1 0 10-2 0A5 5 0 015 8a1 1 0 00-2 0 7.001 7.001 0 006 6.93V17H6a1 1 0 100 2h8a1 1 0 100-2h-3v-2.07z"
            clipRule="evenodd"
          />
        </svg>
      </button>

      {/* Status Indicator */}
      {(status || lastCommand) && (
        <div className="absolute bottom-20 right-0 bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-3 shadow-xl min-w-[250px] max-w-[300px]">
          <div className="flex items-start space-x-3">
            <div className="flex-shrink-0">
              {isListening ? (
                <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              ) : (
                <svg className="w-5 h-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                    clipRule="evenodd"
                  />
                </svg>
              )}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm text-white font-medium">
                {lastCommand || status}
              </p>
              {isListening && (
                <p className="text-xs text-zinc-400 mt-1">
                  Try: "Hey Groovex, play something chill"
                </p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Help Tooltip */}
      {!isListening && !status && !lastCommand && (
        <div className="absolute bottom-20 right-0 bg-zinc-900 border border-zinc-700 rounded-lg px-4 py-2 shadow-xl opacity-0 hover:opacity-100 transition-opacity duration-200 whitespace-nowrap">
          <p className="text-xs text-zinc-400">Click to enable voice commands</p>
        </div>
      )}
    </div>
  );
}
