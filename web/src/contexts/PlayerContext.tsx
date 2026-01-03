import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { audioPlayerService, SAMPLE_SONGS, Song } from '../services/audioPlayer';

interface PlayerContextType {
  currentSong: Song | null;
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  volume: number;
  playlist: Song[];
  currentIndex: number;
  play: (song?: Song, index?: number) => void;
  pause: () => void;
  togglePlayPause: () => void;
  next: () => void;
  previous: () => void;
  setVolume: (volume: number) => void;
  increaseVolume: () => void;
  decreaseVolume: () => void;
  seek: (time: number) => void;
}

const PlayerContext = createContext<PlayerContextType | undefined>(undefined);

export function PlayerProvider({ children }: { children: ReactNode }) {
  const [currentSong, setCurrentSong] = useState<Song | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolumeState] = useState(0.7);
  const [playlist] = useState<Song[]>(SAMPLE_SONGS);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    // Setup audio player callbacks
    audioPlayerService.onPlay((song) => {
      setCurrentSong(song);
      setIsPlaying(true);
    });

    audioPlayerService.onPause(() => {
      setIsPlaying(false);
    });

    audioPlayerService.onEnd(() => {
      handleNext();
    });

    audioPlayerService.onTimeUpdate((currentTime, duration) => {
      setCurrentTime(currentTime);
      setDuration(duration);
    });

    return () => {
      audioPlayerService.pause();
    };
  }, []);

  const play = (song?: Song, index?: number) => {
    const songToPlay = song || playlist[currentIndex];
    const idx = index !== undefined ? index : currentIndex;
    
    if (songToPlay) {
      audioPlayerService.play(songToPlay);
      setCurrentIndex(idx);
      setCurrentSong(songToPlay);
    }
  };

  const pause = () => {
    audioPlayerService.pause();
  };

  const togglePlayPause = () => {
    if (currentSong) {
      audioPlayerService.togglePlayPause();
    } else {
      play(playlist[0], 0);
    }
  };

  const handleNext = () => {
    const nextIndex = (currentIndex + 1) % playlist.length;
    play(playlist[nextIndex], nextIndex);
  };

  const previous = () => {
    const prevIndex = currentIndex === 0 ? playlist.length - 1 : currentIndex - 1;
    play(playlist[prevIndex], prevIndex);
  };

  const setVolume = (newVolume: number) => {
    setVolumeState(newVolume);
    audioPlayerService.setVolume(newVolume);
  };

  const increaseVolume = () => {
    const newVolume = Math.min(1, volume + 0.1);
    setVolume(newVolume);
  };

  const decreaseVolume = () => {
    const newVolume = Math.max(0, volume - 0.1);
    setVolume(newVolume);
  };

  const seek = (time: number) => {
    audioPlayerService.seek(time);
  };

  return (
    <PlayerContext.Provider
      value={{
        currentSong,
        isPlaying,
        currentTime,
        duration,
        volume,
        playlist,
        currentIndex,
        play,
        pause,
        togglePlayPause,
        next: handleNext,
        previous,
        setVolume,
        increaseVolume,
        decreaseVolume,
        seek,
      }}
    >
      {children}
    </PlayerContext.Provider>
  );
}

export function usePlayer() {
  const context = useContext(PlayerContext);
  if (context === undefined) {
    throw new Error('usePlayer must be used within a PlayerProvider');
  }
  return context;
}
