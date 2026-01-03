// Lyrics Service - Fetch and sync lyrics with karaoke-style highlighting

export interface LyricLine {
  time: number; // seconds
  text: string;
  endTime?: number;
}

export interface Lyrics {
  songId: string;
  title: string;
  artist: string;
  lines: LyricLine[];
  source: string;
  syncType: 'line' | 'word' | 'none';
}

export class LyricsService {
  private lyricsCache: Map<string, Lyrics> = new Map();
  private currentLyrics: Lyrics | null = null;
  private currentLineIndex: number = -1;

  // Mock lyrics database - in production, fetch from API
  private mockLyricsDatabase: Record<string, Lyrics> = {
    default: {
      songId: 'default',
      title: 'Sample Song',
      artist: 'Sample Artist',
      syncType: 'line',
      source: 'groovex',
      lines: [
        { time: 0, text: '♪ Instrumental ♪', endTime: 5 },
        { time: 5, text: 'Welcome to Groovex', endTime: 8 },
        { time: 8, text: 'Your music streaming platform', endTime: 11 },
        { time: 11, text: 'With AI-powered features', endTime: 14 },
        { time: 14, text: 'Making every moment musical', endTime: 17 },
        { time: 17, text: '♪ Instrumental ♪', endTime: 22 },
        { time: 22, text: 'Discover new sounds', endTime: 25 },
        { time: 25, text: 'Create perfect playlists', endTime: 28 },
        { time: 28, text: 'Let the music play', endTime: 31 },
        { time: 31, text: '♪ Instrumental outro ♪', endTime: 40 },
      ],
    },
  };

  constructor() {
    this.loadMockData();
  }

  // Fetch lyrics for a song
  async fetchLyrics(songId: string, title: string, artist: string): Promise<Lyrics | null> {
    // Check cache first
    if (this.lyricsCache.has(songId)) {
      return this.lyricsCache.get(songId)!;
    }

    try {
      // In production, call lyrics API (e.g., Musixmatch, Genius)
      // For demo, use mock data
      const lyrics = await this.getMockLyrics(songId, title, artist);
      
      if (lyrics) {
        this.lyricsCache.set(songId, lyrics);
        return lyrics;
      }

      return null;
    } catch (error) {
      console.error('Failed to fetch lyrics:', error);
      return null;
    }
  }

  // Get mock lyrics (simulates API call)
  private async getMockLyrics(songId: string, title: string, artist: string): Promise<Lyrics | null> {
    // Simulate network delay
    await new Promise((resolve) => setTimeout(resolve, 300));

    // Check if we have specific lyrics for this song
    if (this.mockLyricsDatabase[songId]) {
      return this.mockLyricsDatabase[songId];
    }

    // Generate generic lyrics based on song info
    const genericLyrics: Lyrics = {
      songId,
      title,
      artist,
      syncType: 'line',
      source: 'groovex',
      lines: this.generateGenericLyrics(title, artist),
    };

    return genericLyrics;
  }

  // Generate generic lyrics when real ones aren't available
  private generateGenericLyrics(title: string, artist: string): LyricLine[] {
    const duration = 180; // 3 minutes
    const lineCount = 20;
    const linesPerSection = 4;
    const lines: LyricLine[] = [];

    // Intro
    lines.push({ time: 0, text: '♪ Instrumental intro ♪', endTime: 8 });

    // Verse 1
    let currentTime = 8;
    for (let i = 0; i < linesPerSection; i++) {
      lines.push({
        time: currentTime,
        text: `${title} by ${artist}`,
        endTime: currentTime + 3,
      });
      currentTime += 3;
    }

    // Chorus
    lines.push({ time: currentTime, text: '♪ Chorus ♪', endTime: currentTime + 1 });
    currentTime += 1;
    for (let i = 0; i < linesPerSection; i++) {
      lines.push({
        time: currentTime,
        text: `Music fills the air tonight`,
        endTime: currentTime + 3,
      });
      currentTime += 3;
    }

    // Verse 2
    lines.push({ time: currentTime, text: '♪ Instrumental break ♪', endTime: currentTime + 8 });
    currentTime += 8;
    for (let i = 0; i < linesPerSection; i++) {
      lines.push({
        time: currentTime,
        text: `Feel the rhythm, feel the beat`,
        endTime: currentTime + 3,
      });
      currentTime += 3;
    }

    // Final chorus
    for (let i = 0; i < linesPerSection; i++) {
      lines.push({
        time: currentTime,
        text: `Let the music set you free`,
        endTime: currentTime + 3,
      });
      currentTime += 3;
    }

    // Outro
    lines.push({ time: currentTime, text: '♪ Instrumental outro ♪', endTime: duration });

    return lines;
  }

  // Get current line based on playback time
  getCurrentLine(currentTime: number): { current: LyricLine | null; next: LyricLine | null; index: number } {
    if (!this.currentLyrics) {
      return { current: null, next: null, index: -1 };
    }

    const lines = this.currentLyrics.lines;
    
    // Find the current line
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i];
      const nextLine = lines[i + 1];
      
      const endTime = line.endTime || (nextLine ? nextLine.time : Infinity);
      
      if (currentTime >= line.time && currentTime < endTime) {
        this.currentLineIndex = i;
        return {
          current: line,
          next: nextLine || null,
          index: i,
        };
      }
    }

    // If past all lines, return last line
    if (currentTime >= lines[lines.length - 1].time) {
      this.currentLineIndex = lines.length - 1;
      return {
        current: lines[lines.length - 1],
        next: null,
        index: lines.length - 1,
      };
    }

    // Before first line
    return {
      current: null,
      next: lines[0],
      index: -1,
    };
  }

  // Get all lines with highlight info
  getAllLines(currentTime: number): Array<LyricLine & { isCurrent: boolean; isPast: boolean }> {
    if (!this.currentLyrics) {
      return [];
    }

    const currentLineInfo = this.getCurrentLine(currentTime);
    
    return this.currentLyrics.lines.map((line, index) => ({
      ...line,
      isCurrent: index === currentLineInfo.index,
      isPast: index < currentLineInfo.index,
    }));
  }

  // Set current lyrics
  setCurrentLyrics(lyrics: Lyrics | null) {
    this.currentLyrics = lyrics;
    this.currentLineIndex = -1;
  }

  // Get current lyrics
  getCurrentLyrics(): Lyrics | null {
    return this.currentLyrics;
  }

  // Check if lyrics are available
  hasLyrics(songId: string): boolean {
    return this.lyricsCache.has(songId) || !!this.mockLyricsDatabase[songId];
  }

  // Clear cache
  clearCache() {
    this.lyricsCache.clear();
  }

  // Load mock data (for demo purposes)
  private loadMockData() {
    // Add some sample songs with timed lyrics
    this.mockLyricsDatabase['chill_vibes'] = {
      songId: 'chill_vibes',
      title: 'Chill Vibes',
      artist: 'Groovex Artists',
      syncType: 'line',
      source: 'groovex',
      lines: [
        { time: 0, text: '♪ Soft instrumental ♪', endTime: 5 },
        { time: 5, text: 'Slow down, take it easy', endTime: 9 },
        { time: 9, text: 'Let the world fade away', endTime: 13 },
        { time: 13, text: 'In this moment, we can stay', endTime: 17 },
        { time: 17, text: 'Finding peace in the quiet', endTime: 21 },
        { time: 21, text: '♪ Instrumental break ♪', endTime: 29 },
        { time: 29, text: 'Breathe in, breathe out', endTime: 33 },
        { time: 33, text: 'Feel the rhythm all around', endTime: 37 },
        { time: 37, text: 'Chill vibes, they surround', endTime: 41 },
        { time: 41, text: 'In the sound we have found', endTime: 45 },
        { time: 45, text: '♪ Outro ♪', endTime: 60 },
      ],
    };

    this.mockLyricsDatabase['workout_anthem'] = {
      songId: 'workout_anthem',
      title: 'Workout Anthem',
      artist: 'Power Beat',
      syncType: 'line',
      source: 'groovex',
      lines: [
        { time: 0, text: '♪ Energetic intro ♪', endTime: 3 },
        { time: 3, text: 'Push yourself to the limit', endTime: 6 },
        { time: 6, text: "Don't you dare quit it", endTime: 9 },
        { time: 9, text: 'Feel the power rising', endTime: 12 },
        { time: 12, text: 'Keep on energizing', endTime: 15 },
        { time: 15, text: '♪ Beat drop ♪', endTime: 18 },
        { time: 18, text: 'One more rep, one more set', endTime: 21 },
        { time: 21, text: "This is how we get there yet", endTime: 24 },
        { time: 24, text: 'Stronger every single day', endTime: 27 },
        { time: 27, text: 'Nothing standing in our way', endTime: 30 },
        { time: 30, text: '♪ Powerful outro ♪', endTime: 45 },
      ],
    };
  }

  // Add custom lyrics (for user-generated content)
  addCustomLyrics(lyrics: Lyrics) {
    this.mockLyricsDatabase[lyrics.songId] = lyrics;
    this.lyricsCache.set(lyrics.songId, lyrics);
  }

  // Search lyrics text
  searchLyrics(query: string): Array<{ song: Lyrics; matches: LyricLine[] }> {
    const results: Array<{ song: Lyrics; matches: LyricLine[] }> = [];
    const lowerQuery = query.toLowerCase();

    for (const lyrics of Object.values(this.mockLyricsDatabase)) {
      const matches = lyrics.lines.filter((line) =>
        line.text.toLowerCase().includes(lowerQuery)
      );

      if (matches.length > 0) {
        results.push({ song: lyrics, matches });
      }
    }

    return results;
  }
}

export const lyricsService = new LyricsService();
