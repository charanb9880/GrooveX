// Smart Playlist Generation - AI creates playlists based on context

export interface PlaylistContext {
  timeOfDay: 'morning' | 'afternoon' | 'evening' | 'night';
  weather?: 'sunny' | 'rainy' | 'cloudy' | 'snowy';
  activity?: 'working' | 'exercising' | 'relaxing' | 'studying' | 'commuting' | 'party';
  mood?: 'happy' | 'sad' | 'energetic' | 'chill' | 'focus';
  duration?: number; // minutes
}

export interface SmartPlaylist {
  id: string;
  name: string;
  description: string;
  context: PlaylistContext;
  songs: string[]; // song IDs
  createdAt: number;
  criteria: {
    genres: string[];
    tempos: string[];
    moods: string[];
  };
}

export class SmartPlaylistService {
  private playlists: SmartPlaylist[] = [];
  private weatherCache: { temp?: number; condition?: string; timestamp: number } | null = null;

  constructor() {
    this.loadFromStorage();
  }

  // Generate a smart playlist based on current context
  async generatePlaylist(customContext?: Partial<PlaylistContext>): Promise<SmartPlaylist> {
    const context = await this.buildContext(customContext);
    const criteria = this.determineCriteria(context);
    
    const playlist: SmartPlaylist = {
      id: this.generateId(),
      name: this.generatePlaylistName(context),
      description: this.generateDescription(context),
      context,
      songs: [], // Will be populated by API
      createdAt: Date.now(),
      criteria,
    };

    this.playlists.push(playlist);
    this.saveToStorage();

    return playlist;
  }

  // Build context based on current conditions
  private async buildContext(custom?: Partial<PlaylistContext>): Promise<PlaylistContext> {
    const hour = new Date().getHours();
    let timeOfDay: PlaylistContext['timeOfDay'];

    if (hour >= 5 && hour < 12) {
      timeOfDay = 'morning';
    } else if (hour >= 12 && hour < 17) {
      timeOfDay = 'afternoon';
    } else if (hour >= 17 && hour < 22) {
      timeOfDay = 'evening';
    } else {
      timeOfDay = 'night';
    }

    // Try to get weather (if location available)
    const weather = await this.getWeather();

    return {
      timeOfDay,
      weather,
      activity: custom?.activity,
      mood: custom?.mood,
      duration: custom?.duration || 60,
    };
  }

  // Determine playlist criteria based on context
  private determineCriteria(context: PlaylistContext): SmartPlaylist['criteria'] {
    const criteria = {
      genres: [] as string[],
      tempos: [] as string[],
      moods: [] as string[],
    };

    // Time of day influences
    switch (context.timeOfDay) {
      case 'morning':
        criteria.moods.push('energetic', 'happy', 'uplifting');
        criteria.tempos.push('medium', 'fast');
        criteria.genres.push('pop', 'indie', 'electronic');
        break;
      case 'afternoon':
        criteria.moods.push('focus', 'neutral', 'upbeat');
        criteria.tempos.push('medium');
        criteria.genres.push('instrumental', 'jazz', 'acoustic');
        break;
      case 'evening':
        criteria.moods.push('chill', 'relaxing', 'mellow');
        criteria.tempos.push('medium', 'slow');
        criteria.genres.push('r&b', 'soul', 'indie');
        break;
      case 'night':
        criteria.moods.push('chill', 'ambient', 'calm');
        criteria.tempos.push('slow');
        criteria.genres.push('ambient', 'chillout', 'lo-fi');
        break;
    }

    // Weather influences
    switch (context.weather) {
      case 'rainy':
        criteria.moods.push('melancholic', 'cozy', 'introspective');
        criteria.genres.push('indie', 'acoustic', 'classical');
        break;
      case 'sunny':
        criteria.moods.push('happy', 'upbeat', 'cheerful');
        criteria.tempos.push('fast', 'medium');
        criteria.genres.push('pop', 'reggae', 'summer');
        break;
      case 'snowy':
        criteria.moods.push('cozy', 'warm', 'peaceful');
        criteria.genres.push('classical', 'jazz', 'folk');
        break;
      case 'cloudy':
        criteria.moods.push('contemplative', 'calm');
        criteria.genres.push('indie', 'alternative');
        break;
    }

    // Activity influences
    switch (context.activity) {
      case 'working':
      case 'studying':
        criteria.moods.push('focus', 'concentration', 'productive');
        criteria.tempos.push('medium', 'slow');
        criteria.genres.push('instrumental', 'classical', 'lo-fi', 'ambient');
        break;
      case 'exercising':
        criteria.moods.push('energetic', 'powerful', 'motivating');
        criteria.tempos.push('fast');
        criteria.genres.push('edm', 'rock', 'hip-hop', 'electronic');
        break;
      case 'relaxing':
        criteria.moods.push('chill', 'peaceful', 'calm');
        criteria.tempos.push('slow');
        criteria.genres.push('ambient', 'chillout', 'acoustic', 'new age');
        break;
      case 'commuting':
        criteria.moods.push('upbeat', 'energetic');
        criteria.tempos.push('medium', 'fast');
        criteria.genres.push('pop', 'rock', 'indie');
        break;
      case 'party':
        criteria.moods.push('energetic', 'fun', 'danceable');
        criteria.tempos.push('fast');
        criteria.genres.push('edm', 'dance', 'pop', 'hip-hop');
        break;
    }

    // Mood override if specified
    if (context.mood) {
      criteria.moods = [context.mood, ...criteria.moods.slice(0, 2)];
    }

    return criteria;
  }

  // Generate playlist name
  private generatePlaylistName(context: PlaylistContext): string {
    const parts: string[] = [];

    if (context.activity) {
      const activityNames: Record<string, string> = {
        working: 'Work Session',
        exercising: 'Workout Fuel',
        relaxing: 'Chill Time',
        studying: 'Study Focus',
        commuting: 'On The Go',
        party: 'Party Mode',
      };
      parts.push(activityNames[context.activity]);
    } else {
      const timeNames: Record<string, string> = {
        morning: 'Morning Boost',
        afternoon: 'Afternoon Flow',
        evening: 'Evening Wind Down',
        night: 'Night Vibes',
      };
      parts.push(timeNames[context.timeOfDay]);
    }

    if (context.weather) {
      const weatherEmojis: Record<string, string> = {
        sunny: '☀️',
        rainy: '🌧️',
        cloudy: '☁️',
        snowy: '❄️',
      };
      parts.push(weatherEmojis[context.weather]);
    }

    return parts.join(' ');
  }

  // Generate description
  private generateDescription(context: PlaylistContext): string {
    const descriptions: string[] = [];

    if (context.activity) {
      const activityDescs: Record<string, string> = {
        working: 'Perfect background music for getting things done',
        exercising: 'High-energy tracks to power your workout',
        relaxing: 'Smooth and soothing tunes for unwinding',
        studying: 'Focus-enhancing music with minimal distractions',
        commuting: 'Great songs for your daily journey',
        party: 'Dance-worthy bangers for your celebration',
      };
      descriptions.push(activityDescs[context.activity]);
    }

    if (context.weather === 'rainy') {
      descriptions.push('Cozy vibes for a rainy day');
    } else if (context.weather === 'sunny') {
      descriptions.push('Bright and cheerful songs for sunny skies');
    }

    const timeDescs: Record<string, string> = {
      morning: 'Start your day with energy',
      afternoon: 'Keep the momentum going',
      evening: 'Transition into relaxation mode',
      night: 'Perfect for late-night listening',
    };
    descriptions.push(timeDescs[context.timeOfDay]);

    return descriptions.join('. ');
  }

  // Get weather (simplified - in production, use real weather API)
  private async getWeather(): Promise<PlaylistContext['weather'] | undefined> {
    // Check cache (valid for 30 minutes)
    const cacheValid = this.weatherCache && 
                      (Date.now() - this.weatherCache.timestamp) < 30 * 60 * 1000;
    
    if (cacheValid && this.weatherCache?.condition) {
      return this.weatherCache.condition as PlaylistContext['weather'];
    }

    try {
      // In a real app, you'd use a weather API like OpenWeatherMap
      // For demo, we'll simulate based on time
      const hour = new Date().getHours();
      let condition: PlaylistContext['weather'];
      
      if (hour >= 6 && hour < 18) {
        condition = 'sunny';
      } else {
        condition = 'cloudy';
      }

      this.weatherCache = {
        condition,
        timestamp: Date.now(),
      };

      return condition;
    } catch (error) {
      console.error('Failed to get weather:', error);
      return undefined;
    }
  }

  // Get all playlists
  getPlaylists(): SmartPlaylist[] {
    return this.playlists;
  }

  // Get playlist by ID
  getPlaylist(id: string): SmartPlaylist | undefined {
    return this.playlists.find((p) => p.id === id);
  }

  // Delete playlist
  deletePlaylist(id: string): boolean {
    const index = this.playlists.findIndex((p) => p.id === id);
    if (index !== -1) {
      this.playlists.splice(index, 1);
      this.saveToStorage();
      return true;
    }
    return false;
  }

  // Generate ID
  private generateId(): string {
    return `playlist_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  // Storage helpers
  private saveToStorage() {
    try {
      localStorage.setItem('groovex_smart_playlists', JSON.stringify(this.playlists));
    } catch (error) {
      console.error('Failed to save playlists:', error);
    }
  }

  private loadFromStorage() {
    try {
      const data = localStorage.getItem('groovex_smart_playlists');
      if (data) {
        this.playlists = JSON.parse(data);
      }
    } catch (error) {
      console.error('Failed to load playlists:', error);
    }
  }

  // Get activity suggestions based on time
  getActivitySuggestions(): Array<{ activity: string; label: string; emoji: string }> {
    const hour = new Date().getHours();
    const all = [
      { activity: 'working', label: 'Work / Study', emoji: '💼' },
      { activity: 'exercising', label: 'Workout', emoji: '💪' },
      { activity: 'relaxing', label: 'Relax', emoji: '😌' },
      { activity: 'studying', label: 'Focus', emoji: '📚' },
      { activity: 'commuting', label: 'Commute', emoji: '🚗' },
      { activity: 'party', label: 'Party', emoji: '🎉' },
    ];

    // Suggest relevant activities based on time
    if (hour >= 6 && hour < 9) {
      return all.filter((a) => ['commuting', 'working', 'exercising'].includes(a.activity));
    } else if (hour >= 9 && hour < 17) {
      return all.filter((a) => ['working', 'studying', 'relaxing'].includes(a.activity));
    } else if (hour >= 17 && hour < 22) {
      return all.filter((a) => ['exercising', 'relaxing', 'party'].includes(a.activity));
    } else {
      return all.filter((a) => ['relaxing', 'party'].includes(a.activity));
    }
  }
}

export const smartPlaylistService = new SmartPlaylistService();
