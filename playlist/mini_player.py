"""
Memory-Efficient Mini Player module for PlayWise Music Engine.
"""

from collections import deque
from typing import List, Optional
from .song import Song


class MiniPlayer:
    """
    Memory-efficient mini player that preloads only the next N songs while playing.
    """
    
    def __init__(self, window_size: int = 5):
        """
        Initialize the mini player with a fixed window size.
        """
        self._window_size = window_size
        self._upcoming_songs = deque(maxlen=window_size)
        self._played_songs: List[Song] = []
        self._current_song: Optional[Song] = None
    
    def preload_songs(self, songs: List[Song]) -> None:
        """
        Preload songs into the player's buffer.
        """
        self._upcoming_songs.clear()
        self._played_songs.clear()
        self._current_song = None
        
        for song in songs[:self._window_size]:
            self._upcoming_songs.append(song)
    
    def play_next(self) -> Optional[Song]:
        """
        Play the next song and advance the player.
        """
        if self._current_song is not None:
            self._played_songs.append(self._current_song)
        
        if self._upcoming_songs:
            self._current_song = self._upcoming_songs.popleft()
            return self._current_song
        else:
            self._current_song = None
            return None
    
    def get_upcoming_songs(self) -> List[Song]:
        """
        Get the list of upcoming songs in the buffer.
        """
        return list(self._upcoming_songs)
    
    def get_played_songs(self) -> List[Song]:
        """
        Get the list of songs that have been played.
        """
        return self._played_songs.copy()
    
    def get_current_song(self) -> Optional[Song]:
        """
        Get the currently playing song.
        """
        return self._current_song
    
    def is_finished(self) -> bool:
        """
        Check if all songs have been played.
        """
        return self._current_song is None and len(self._upcoming_songs) == 0
    
    def get_window_size(self) -> int:
        """
        Get the current window size.
        """
        return self._window_size
    
    def set_window_size(self, window_size: int) -> None:
        """
        Set a new window size.
        """
        if window_size <= 0:
            raise ValueError("Window size must be positive")
        
        new_deque = deque(self._upcoming_songs, maxlen=window_size)
        self._upcoming_songs = new_deque
        self._window_size = window_size