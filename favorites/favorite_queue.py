"""
Favorite Queue module for PlayWise Music Engine.

Maintains a sorted queue of favorite songs ordered by cumulative listen time.
Uses a max-heap with lazy updates for efficient ordering.
"""

import heapq
import time
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class SongSummary:
    """Simple data class to represent song information for the favorites list."""
    song_id: str
    title: str
    artist: str
    total_listen_time: int


class FavoriteQueue:
    """
    Maintains songs ordered by cumulative total_listen_time using a max-heap with lazy updates.
    
    Algorithm Choice:
    - Max-heap with lazy updates + dict for O(1) lookups
    - On record_listen: increment dict value, push (-total_listen_time, timestamp, song_id) onto heap
    - On get_top_n: pop from heap lazily until top entry matches dict[song_id] (not stale)
    
    Time Complexity:
        - record_listen: O(log m) where m = number of favorite songs
        - get_top_n(n): O(n log m) amortized due to lazy pops
        - add_to_favorites: O(1)
        - remove_song: O(1)
        - clear: O(1)
    
    Space Complexity:
        - O(m) where m is the number of favorite songs
    """
    
    def __init__(self):
        # Dict mapping song_id to total listen time
        self.song_listen_times: Dict[str, int] = {}
        # Max-heap: (-total_listen_time, timestamp, song_id)
        self.heap: List[Tuple[int, float, str]] = []
        # Dict to track favorite songs (song_id -> (title, artist))
        self.favorites: Dict[str, Tuple[str, str]] = {}
    
    def add_to_favorites(self, song_id: str, title: str, artist: str) -> None:
        """
        Add a song to the favorites tracking.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            song_id (str): Unique identifier for the song
            title (str): Song title
            artist (str): Song artist
        """
        if song_id not in self.favorites:
            self.favorites[song_id] = (title, artist)
            # Initialize listen time to 0 if not already tracked
            if song_id not in self.song_listen_times:
                self.song_listen_times[song_id] = 0
    
    def remove_from_favorites(self, song_id: str) -> None:
        """
        Remove a song from favorites tracking.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            song_id (str): Unique identifier for the song
        """
        if song_id in self.favorites:
            del self.favorites[song_id]
            # Note: We don't remove from song_listen_times or heap to avoid O(n) operation
            # The lazy update mechanism will handle stale entries
    
    def record_listen(self, song_id: str, delta_seconds: int) -> None:
        """
        Record a listen event for a song, updating its total listen time.
        
        Time Complexity: O(log m) where m is the number of favorite songs
        Space Complexity: O(1) amortized
        
        Args:
            song_id (str): Unique identifier for the song
            delta_seconds (int): Duration of the listen event in seconds
        """
        # Only track songs that are marked as favorites
        if song_id not in self.favorites:
            return
            
        # Update the total listen time
        if song_id in self.song_listen_times:
            self.song_listen_times[song_id] += delta_seconds
        else:
            self.song_listen_times[song_id] = delta_seconds
        
        # Push the updated value to the heap with timestamp to break ties
        # Use negative value for max-heap behavior
        heapq.heappush(
            self.heap, 
            (-self.song_listen_times[song_id], time.time(), song_id)
        )
    
    def get_top_n(self, n: int) -> List[SongSummary]:
        """
        Get the top n favorite songs ordered by total listen time.
        
        Time Complexity: O(n log m) amortized where m is the number of favorite songs
        Space Complexity: O(n)
        
        Args:
            n (int): Number of top songs to return
            
        Returns:
            List[SongSummary]: List of top n songs with their information
        """
        result = []
        temp_entries = []  # Store valid entries to push back later
        
        while len(result) < n and self.heap:
            # Pop the top entry
            neg_listen_time, timestamp, song_id = heapq.heappop(self.heap)
            listen_time = -neg_listen_time
            
            # Check if this entry is still valid (not stale)
            if (song_id in self.song_listen_times and 
                song_id in self.favorites and
                self.song_listen_times[song_id] == listen_time):
                # Valid entry, add to result
                title, artist = self.favorites[song_id]
                result.append(SongSummary(
                    song_id=song_id,
                    title=title,
                    artist=artist,
                    total_listen_time=listen_time
                ))
                # Save this entry to push back later
                temp_entries.append((neg_listen_time, timestamp, song_id))
            # If stale, just discard it (lazy deletion)
        
        # Push back the valid entries we popped
        for entry in temp_entries:
            heapq.heappush(self.heap, entry)
        
        return result
    
    def clear(self) -> None:
        """
        Clear all favorites and listen time data.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.song_listen_times.clear()
        self.heap.clear()
        self.favorites.clear()