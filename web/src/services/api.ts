// API service for PlayWise Music Engine

const API_BASE_URL = '/api';

interface Song {
  index?: number;
  song_id?: string;
  title: string;
  artist: string;
  duration: number;
}

interface Playlist {
  id: string;
  songs: Song[];
}

interface Snapshot {
  timestamp: string;
  system_overview: {
    total_songs_in_playlist: number;
    total_duration_seconds: number;
    average_song_duration: number;
    total_playback_history: number;
  };
  top_5_longest_songs: Song[];
  recently_played_songs: Song[];
  song_count_by_rating: Record<number, number>;
  extremes: {
    shortest_song: {
      title: string | null;
      duration: number | null;
    };
    longest_song: {
      title: string | null;
      duration: number | null;
    };
  };
}

interface Recommendation {
  song_id: string;
  title: string;
  artist: string;
  score: number;
  reason: string;
}

interface Favorite {
  song_id: string;
  title: string;
  artist: string;
  total_listen_time: number;
}

// Generic API call helper
async function apiCall<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;
  
  const response = await fetch(url, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  });
  
  if (!response.ok) {
    throw new Error(`API call failed: ${response.status} ${response.statusText}`);
  }
  
  return response.json();
}

// Health check
export async function healthCheck(): Promise<{ status: string }> {
  return apiCall('/health');
}

// Playlist endpoints
export async function listPlaylists(): Promise<Array<{ id: string; name: string; length: number }>> {
  return apiCall('/playlists');
}

export async function getPlaylist(playlistId: string): Promise<Playlist> {
  return apiCall(`/playlists/${playlistId}`);
}

export async function addSongToPlaylist(playlistId: string, song: Omit<Song, 'index' | 'song_id'>): Promise<{ song_id: string; result: string | null }> {
  return apiCall(`/playlists/${playlistId}/songs`, {
    method: 'POST',
    body: JSON.stringify(song),
  });
}

export async function deleteSongFromPlaylist(playlistId: string, index: number): Promise<{ message: string }> {
  return apiCall(`/playlists/${playlistId}/songs/${index}`, {
    method: 'DELETE',
  });
}

export async function moveSongInPlaylist(playlistId: string, fromIndex: number, toIndex: number): Promise<{ message: string }> {
  return apiCall(`/playlists/${playlistId}/move`, {
    method: 'POST',
    body: JSON.stringify({ from_index: fromIndex, to_index: toIndex }),
  });
}

export async function reversePlaylist(playlistId: string): Promise<{ message: string }> {
  return apiCall(`/playlists/${playlistId}/reverse`, {
    method: 'POST',
  });
}

// Playback endpoints
export async function playSong(playlistId: string, index?: number): Promise<Song> {
  return apiCall('/playback/play', {
    method: 'POST',
    body: JSON.stringify({ playlist_id: playlistId, index }),
  });
}

export async function skipSong(songId: string, playlistId?: string): Promise<{ message: string }> {
  return apiCall('/playback/skip', {
    method: 'POST',
    body: JSON.stringify({ song_id: songId, playlist_id: playlistId }),
  });
}

export async function undoLastPlay(): Promise<{ message: string }> {
  return apiCall('/history/undo', {
    method: 'POST',
  });
}

// Snapshot endpoint
export async function getSnapshot(): Promise<Snapshot> {
  return apiCall('/snapshot');
}

// Explorer endpoints
export async function searchSongs(params: {
  genre?: string;
  subgenre?: string;
  mood?: string;
  artist?: string;
}): Promise<Song[]> {
  const queryParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined) {
      queryParams.append(key, value);
    }
  });
  
  return apiCall(`/explorer/search?${queryParams.toString()}`);
}

// Recommendation endpoint
export async function getRecommendations(): Promise<Recommendation[]> {
  return apiCall('/recommend');
}

// Favorites endpoint
export async function getTopFavorites(n: number = 10): Promise<Favorite[]> {
  return apiCall(`/favorites/top?n=${n}`);
}