"""
Recently Skipped Tracker module for PlayWise Music Engine.

Implements a fixed-size FIFO queue to track recently skipped songs to prevent
them from being replayed during autoplay unless explicitly forced.
"""

from collections import deque
from typing import List, Set


class RecentlySkippedTracker:
    """
    Tracks recently skipped songs using a fixed-size deque and set for O(1) operations.
    
    Uses a deque with maxlen for automatic eviction of oldest items and a set for
    O(1) membership checking. When items are evicted from the deque, they are
    also removed from the set.
    
    Time Complexity: O(1) for all operations
    Space Complexity: O(capacity) where capacity is the maximum number of tracked songs
    """

    def __init__(self, capacity: int = 10):
        """
        Initialize the skipped tracker with a fixed capacity.
        
        Args:
            capacity (int): Maximum number of songs to track (default: 10)
        """
        self.capacity = capacity
        self._deque = deque(maxlen=capacity)
        self._set: Set[str] = set()

    def skip_song(self, song_id: str) -> None:
        """
        Add a song to the skipped tracker.
        
        If the deque is at maximum capacity, the oldest song is automatically
        evicted and also removed from the set.
        
        Time Complexity: O(1) amortized
        Space Complexity: O(1) additional space
        
        Args:
            song_id (str): The ID of the song to mark as skipped
        """
        # If deque is at capacity, the oldest item will be automatically evicted
        # We need to remove it from our set as well
        if len(self._deque) == self.capacity and self._deque:
            # Remove the oldest item from the set
            oldest = self._deque[0]
            self._set.discard(oldest)
        
        # Add the new song to both deque and set
        self._deque.append(song_id)
        self._set.add(song_id)

    def is_recently_skipped(self, song_id: str) -> bool:
        """
        Check if a song is in the recently skipped list.
        
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        
        Args:
            song_id (str): The ID of the song to check
            
        Returns:
            bool: True if the song is recently skipped, False otherwise
        """
        return song_id in self._set

    def get_recently_skipped(self) -> List[str]:
        """
        Get the list of recently skipped songs in insertion order (oldest to newest).
        
        Time Complexity: O(k) where k is the number of tracked songs
        Space Complexity: O(k) for the returned list
        
        Returns:
            List[str]: List of song IDs in order from oldest to newest
        """
        return list(self._deque)

    def clear_skipped(self) -> None:
        """
        Clear all tracked skipped songs.
        
        Time Complexity: O(1) amortized
        Space Complexity: O(1)
        """
        self._deque.clear()
        self._set.clear()

    def set_capacity(self, cap: int) -> None:
        """
        Change the capacity of the tracker. If new capacity is smaller,
        older entries will be evicted.
        
        Time Complexity: O(min(current_size, new_capacity))
        Space Complexity: O(min(current_size, new_capacity))
        
        Args:
            cap (int): New capacity for the tracker
        """
        # If reducing capacity, we need to truncate the deque and rebuild the set
        if cap < self.capacity:
            # Keep only the most recent 'cap' items
            if len(self._deque) > cap:
                # Remove excess items from the set
                items_to_remove = len(self._deque) - cap
                for _ in range(items_to_remove):
                    if self._deque:
                        removed_item = self._deque.popleft()
                        self._set.discard(removed_item)
        
        # Update capacity and recreate deque with new maxlen
        self.capacity = cap
        self._deque = deque(self._deque, maxlen=cap)
        # Rebuild set from deque to ensure consistency
        self._set = set(self._deque)