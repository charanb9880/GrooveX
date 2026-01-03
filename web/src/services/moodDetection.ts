// Mood Detection Service - Analyzes listening patterns to detect user mood

export type Mood = 'happy' | 'sad' | 'energetic' | 'chill' | 'focus' | 'neutral';

export interface MoodData {
  mood: Mood;
  confidence: number;
  timestamp: number;
  factors: {
    timeOfDay: number;
    listeningDuration: number;
    songTempo: number;
    genrePattern: string[];
  };
}

export interface ListeningPattern {
  timestamp: number;
  songTitle: string;
  artist: string;
  duration: number;
  genre?: string;
  tempo?: 'slow' | 'medium' | 'fast';
  mood?: string;
}

export class MoodDetectionService {
  private listeningHistory: ListeningPattern[] = [];
  private currentMood: MoodData | null = null;
  private moodHistory: MoodData[] = [];

  constructor() {
    this.loadFromStorage();
  }

  // Track a song play
  trackSongPlay(song: {
    title: string;
    artist: string;
    duration: number;
    genre?: string;
    tempo?: 'slow' | 'medium' | 'fast';
    mood?: string;
  }) {
    const pattern: ListeningPattern = {
      timestamp: Date.now(),
      songTitle: song.title,
      artist: song.artist,
      duration: song.duration,
      genre: song.genre,
      tempo: song.tempo,
      mood: song.mood,
    };

    this.listeningHistory.push(pattern);
    
    // Keep only last 100 songs
    if (this.listeningHistory.length > 100) {
      this.listeningHistory.shift();
    }

    this.saveToStorage();
    this.detectMood();
  }

  // Detect current mood based on recent listening patterns
  detectMood(): MoodData {
    const now = Date.now();
    const recentThreshold = 60 * 60 * 1000; // Last hour
    const recentSongs = this.listeningHistory.filter(
      (song) => now - song.timestamp < recentThreshold
    );

    if (recentSongs.length === 0) {
      // Default to neutral if no recent activity
      this.currentMood = {
        mood: 'neutral',
        confidence: 0.5,
        timestamp: now,
        factors: {
          timeOfDay: this.getTimeOfDayScore(),
          listeningDuration: 0,
          songTempo: 0,
          genrePattern: [],
        },
      };
      return this.currentMood;
    }

    // Analyze factors
    const timeOfDayScore = this.getTimeOfDayScore();
    const totalDuration = recentSongs.reduce((sum, song) => sum + song.duration, 0);
    const avgTempo = this.calculateAverageTempo(recentSongs);
    const genres = recentSongs.map((s) => s.genre).filter(Boolean) as string[];
    const moods = recentSongs.map((s) => s.mood).filter(Boolean) as string[];

    // Mood detection logic
    let detectedMood: Mood = 'neutral';
    let confidence = 0.5;

    // Check explicit mood tags first
    if (moods.length > 0) {
      const moodCounts = this.countOccurrences(moods);
      const dominantMood = Object.keys(moodCounts).reduce((a, b) =>
        moodCounts[a] > moodCounts[b] ? a : b
      );
      
      if (this.isValidMood(dominantMood)) {
        detectedMood = dominantMood as Mood;
        confidence = moodCounts[dominantMood] / moods.length;
      }
    }

    // Tempo-based mood detection
    if (avgTempo > 0.7) {
      detectedMood = 'energetic';
      confidence = Math.max(confidence, 0.7);
    } else if (avgTempo < 0.3) {
      detectedMood = 'chill';
      confidence = Math.max(confidence, 0.7);
    }

    // Time of day influence
    const hour = new Date().getHours();
    if (hour >= 6 && hour < 9) {
      // Morning - likely energetic or focus
      if (detectedMood === 'neutral') {
        detectedMood = 'energetic';
        confidence = 0.6;
      }
    } else if (hour >= 22 || hour < 6) {
      // Night - likely chill or sad
      if (detectedMood === 'neutral') {
        detectedMood = 'chill';
        confidence = 0.6;
      }
    } else if (hour >= 9 && hour < 17) {
      // Work hours - possibly focus
      if (totalDuration > 1800) { // More than 30 mins
        detectedMood = 'focus';
        confidence = 0.65;
      }
    }

    // Long listening sessions suggest focus or chill
    if (totalDuration > 3600) { // More than 1 hour
      if (avgTempo < 0.5) {
        detectedMood = 'focus';
      }
      confidence = Math.min(confidence + 0.1, 0.9);
    }

    this.currentMood = {
      mood: detectedMood,
      confidence,
      timestamp: now,
      factors: {
        timeOfDay: timeOfDayScore,
        listeningDuration: totalDuration,
        songTempo: avgTempo,
        genrePattern: genres,
      },
    };

    this.moodHistory.push(this.currentMood);
    
    // Keep only last 50 mood detections
    if (this.moodHistory.length > 50) {
      this.moodHistory.shift();
    }

    this.saveToStorage();
    return this.currentMood;
  }

  // Get mood recommendation text
  getMoodRecommendation(): string {
    if (!this.currentMood) {
      return 'Start listening to get personalized recommendations!';
    }

    const moodMessages: Record<Mood, string[]> = {
      happy: [
        '🎉 You seem happy! Keep those good vibes going!',
        '😊 Great energy! Here are more upbeat tracks!',
        '✨ Loving the positive mood! More happy tunes coming!',
      ],
      sad: [
        '💙 Need some comfort? Here are some soothing songs.',
        '🌙 Taking it slow. Music for reflection.',
        '🎵 Sometimes we need to feel the feels. Here for you.',
      ],
      energetic: [
        '⚡ High energy detected! Time to pump it up!',
        '🔥 Let\'s keep this momentum going!',
        '💪 Workout mode activated! Here are some bangers!',
      ],
      chill: [
        '😌 Relaxation mode on. Smooth vibes ahead.',
        '🌊 Taking it easy. Here are some chill beats.',
        '☁️ Perfect vibe for unwinding.',
      ],
      focus: [
        '🎯 Focus mode detected. Minimal distractions ahead.',
        '📚 Deep work playlist ready for you.',
        '🧘 In the zone. Concentration music incoming.',
      ],
      neutral: [
        '🎵 Not sure what mood you\'re in? Let\'s explore!',
        '🎼 Ready for anything! What do you feel like?',
        '🎶 Let\'s find the perfect vibe for you.',
      ],
    };

    const messages = moodMessages[this.currentMood.mood];
    return messages[Math.floor(Math.random() * messages.length)];
  }

  // Get current mood
  getCurrentMood(): MoodData | null {
    return this.currentMood;
  }

  // Get mood history
  getMoodHistory(): MoodData[] {
    return this.moodHistory;
  }

  // Helper: Calculate average tempo score (0-1)
  private calculateAverageTempo(songs: ListeningPattern[]): number {
    const tempoScores: number[] = songs
      .map((song) => {
        if (song.tempo === 'fast') return 1;
        if (song.tempo === 'medium') return 0.5;
        if (song.tempo === 'slow') return 0;
        // Estimate from duration - shorter songs tend to be faster
        return song.duration < 180 ? 0.7 : song.duration < 240 ? 0.5 : 0.3;
      });

    return tempoScores.reduce((sum: number, score: number) => sum + score, 0) / tempoScores.length;
  }

  // Helper: Get time of day score (0-1)
  private getTimeOfDayScore(): number {
    const hour = new Date().getHours();
    // Peak energy hours: 9-11 AM and 2-4 PM
    if ((hour >= 9 && hour <= 11) || (hour >= 14 && hour <= 16)) {
      return 1;
    }
    // Low energy: late night
    if (hour >= 22 || hour <= 6) {
      return 0.2;
    }
    return 0.5;
  }

  // Helper: Count occurrences
  private countOccurrences(arr: string[]): Record<string, number> {
    return arr.reduce((acc, item) => {
      acc[item] = (acc[item] || 0) + 1;
      return acc;
    }, {} as Record<string, number>);
  }

  // Helper: Check if mood is valid
  private isValidMood(mood: string): boolean {
    return ['happy', 'sad', 'energetic', 'chill', 'focus', 'neutral'].includes(mood);
  }

  // Storage helpers
  private saveToStorage() {
    try {
      localStorage.setItem('groovex_listening_history', JSON.stringify(this.listeningHistory));
      localStorage.setItem('groovex_mood_history', JSON.stringify(this.moodHistory));
      if (this.currentMood) {
        localStorage.setItem('groovex_current_mood', JSON.stringify(this.currentMood));
      }
    } catch (error) {
      console.error('Failed to save mood data:', error);
    }
  }

  private loadFromStorage() {
    try {
      const history = localStorage.getItem('groovex_listening_history');
      const moodHist = localStorage.getItem('groovex_mood_history');
      const current = localStorage.getItem('groovex_current_mood');

      if (history) {
        this.listeningHistory = JSON.parse(history);
      }
      if (moodHist) {
        this.moodHistory = JSON.parse(moodHist);
      }
      if (current) {
        this.currentMood = JSON.parse(current);
      }
    } catch (error) {
      console.error('Failed to load mood data:', error);
    }
  }

  // Clear history (for testing or reset)
  clearHistory() {
    this.listeningHistory = [];
    this.moodHistory = [];
    this.currentMood = null;
    localStorage.removeItem('groovex_listening_history');
    localStorage.removeItem('groovex_mood_history');
    localStorage.removeItem('groovex_current_mood');
  }
}

export const moodDetectionService = new MoodDetectionService();
