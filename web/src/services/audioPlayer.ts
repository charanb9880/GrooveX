// Audio Player Service for managing music playback

export interface Song {
  id: string;
  title: string;
  artist: string;
  duration: number;
  audioUrl: string;
}

// Sample songs with royalty-free audio URLs
export const SAMPLE_SONGS: Song[] = [
  {
    id: '1',
    title: 'Summer Vibes',
    artist: 'Groovex Artists',
    duration: 180,
    audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'
  },
  {
    id: '2',
    title: 'Chill Beats',
    artist: 'Lo-Fi Collective',
    duration: 165,
    audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3'
  },
  {
    id: '3',
    title: 'Electronic Dreams',
    artist: 'Digital Wave',
    duration: 210,
    audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3'
  },
  {
    id: '4',
    title: 'Acoustic Sunset',
    artist: 'Indie Folk Band',
    duration: 195,
    audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3'
  },
  {
    id: '5',
    title: 'Night Drive',
    artist: 'Synthwave Collective',
    duration: 220,
    audioUrl: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3'
  }
];

export class AudioPlayerService {
  private audio: HTMLAudioElement | null = null;
  private currentSong: Song | null = null;
  private isPlaying: boolean = false;
  private volume: number = 0.7;
  private onPlayCallback?: (song: Song) => void;
  private onPauseCallback?: () => void;
  private onEndCallback?: () => void;
  private onTimeUpdateCallback?: (currentTime: number, duration: number) => void;

  constructor() {
    this.audio = new Audio();
    this.audio.volume = this.volume;
    this.audio.crossOrigin = "anonymous"; // Enable CORS
    this.audio.preload = "auto"; // Preload audio for faster playback
    this.setupEventListeners();
  }

  private setupEventListeners() {
    if (!this.audio) return;

    this.audio.addEventListener('play', () => {
      this.isPlaying = true;
      if (this.currentSong) {
        this.onPlayCallback?.(this.currentSong);
      }
    });

    this.audio.addEventListener('pause', () => {
      this.isPlaying = false;
      this.onPauseCallback?.();
    });

    this.audio.addEventListener('ended', () => {
      this.isPlaying = false;
      this.onEndCallback?.();
    });

    this.audio.addEventListener('timeupdate', () => {
      if (this.audio) {
        this.onTimeUpdateCallback?.(this.audio.currentTime, this.audio.duration);
      }
    });
  }

  async loadSong(song: Song) {
    if (!this.audio) return;

    this.currentSong = song;
    this.audio.src = song.audioUrl;
    this.audio.crossOrigin = "anonymous";
    try {
      await this.audio.load();
      console.log('Song loaded:', song.title);
    } catch (error) {
      console.error('Error loading song:', error);
    }
  }

  async play(song?: Song) {
    if (!this.audio) return;

    if (song) {
      await this.loadSong(song);
    }

    if (!this.currentSong) {
      console.warn('No song loaded');
      return;
    }

    try {
      // Reset if ended
      if (this.audio.ended) {
        this.audio.currentTime = 0;
      }
      
      const playPromise = this.audio.play();
      if (playPromise !== undefined) {
        await playPromise;
        this.isPlaying = true;
        console.log('Playing:', this.currentSong.title);
      }
    } catch (error) {
      console.error('Failed to play audio:', error);
      // Try to provide helpful error message
      if ((error as Error).name === 'NotAllowedError') {
        console.error('Autoplay blocked - user interaction required');
      }
    }
  }

  pause() {
    if (!this.audio) return;
    this.audio.pause();
    this.isPlaying = false;
  }

  togglePlayPause() {
    if (this.isPlaying) {
      this.pause();
    } else {
      this.play();
    }
  }

  setVolume(volume: number) {
    if (!this.audio) return;
    this.volume = Math.max(0, Math.min(1, volume));
    this.audio.volume = this.volume;
  }

  getVolume(): number {
    return this.volume;
  }

  increaseVolume() {
    this.setVolume(this.volume + 0.1);
  }

  decreaseVolume() {
    this.setVolume(this.volume - 0.1);
  }

  seek(time: number) {
    if (!this.audio) return;
    this.audio.currentTime = time;
  }

  getCurrentTime(): number {
    return this.audio?.currentTime || 0;
  }

  getDuration(): number {
    return this.audio?.duration || 0;
  }

  getCurrentSong(): Song | null {
    return this.currentSong;
  }

  getIsPlaying(): boolean {
    return this.isPlaying;
  }

  onPlay(callback: (song: Song) => void) {
    this.onPlayCallback = callback;
  }

  onPause(callback: () => void) {
    this.onPauseCallback = callback;
  }

  onEnd(callback: () => void) {
    this.onEndCallback = callback;
  }

  onTimeUpdate(callback: (currentTime: number, duration: number) => void) {
    this.onTimeUpdateCallback = callback;
  }
}

export const audioPlayerService = new AudioPlayerService();
