"""
Constrained Shuffle module for PlayWise Music Engine.

Implements shuffle algorithms with constraints to prevent consecutive artists.
"""

import random
from typing import List, Dict
from playlist.song import Song


class ConstrainedShuffler:
    """
    Implements shuffle algorithms with constraints to prevent consecutive artists.
    
    Uses array/list traversal and HashMap for efficient artist tracking.
    
    Time Complexity:
        - shuffle_with_constraints: O(n) average case, O(∞) worst case (if no valid arrangement exists)
        - _has_consecutive_artists: O(n)
    
    Space Complexity:
        - O(n) for the shuffled list
        - O(k) for the artist frequency map where k is the number of unique artists
    """
    
    def __init__(self, max_attempts: int = 1000):
        """
        Initialize the constrained shuffler.
        
        Args:
            max_attempts (int): Maximum number of shuffle attempts before giving up (default: 1000)
        """
        self._max_attempts = max_attempts
    
    def shuffle_with_constraints(self, songs: List[Song]) -> List[Song]:
        """
        Shuffle songs with the constraint that the same artist doesn't appear consecutively.
        
        This implementation uses a randomized approach with reshuffling if violations occur.
        It tries up to max_attempts times to find a valid arrangement.
        
        Time Complexity: 
            - Best/Average case: O(n) where n is the number of songs
            - Worst case: O(max_attempts * n) if a valid arrangement is hard to find
        Space Complexity: O(n)
        
        Args:
            songs (List[Song]): List of songs to shuffle
            
        Returns:
            List[Song]: Shuffled list of songs with no consecutive artists,
                       or original list if no valid arrangement found within max_attempts
            
        Note:
            If it's impossible to arrange the songs without consecutive artists
            (e.g., one artist has more than half the songs), the original list is returned.
        """
        if len(songs) <= 1:
            return songs.copy()
        
        # Check if it's theoretically possible to avoid consecutive artists
        if not self._is_arrangement_possible(songs):
            # Return a simple shuffle if arrangement isn't possible
            result = songs.copy()
            random.shuffle(result)
            return result
        
        # Try to find a valid arrangement
        for _ in range(self._max_attempts):
            # Create a shuffled copy
            shuffled = songs.copy()
            random.shuffle(shuffled)
            
            # Check if this arrangement violates the constraint
            if not self._has_consecutive_artists(shuffled):
                return shuffled
        
        # If we couldn't find a valid arrangement, return original order with warning
        # This could happen with pathological cases
        return songs.copy()
    
    def _has_consecutive_artists(self, songs: List[Song]) -> bool:
        """
        Check if the song list has consecutive songs by the same artist.
        
        Time Complexity: O(n) where n is the number of songs
        Space Complexity: O(1)
        
        Args:
            songs (List[Song]): List of songs to check
            
        Returns:
            bool: True if there are consecutive songs by the same artist, False otherwise
        """
        for i in range(len(songs) - 1):
            if songs[i].artist.lower() == songs[i + 1].artist.lower():
                return True
        return False
    
    def _is_arrangement_possible(self, songs: List[Song]) -> bool:
        """
        Check if it's theoretically possible to arrange songs without consecutive artists.
        
        Based on the pigeonhole principle: if any artist has more than ceil(n/2) songs,
        it's impossible to avoid consecutive placement.
        
        Time Complexity: O(n + k) where n is number of songs and k is number of unique artists
        Space Complexity: O(k) for the artist count map
        
        Args:
            songs (List[Song]): List of songs to check
            
        Returns:
            bool: True if arrangement is possible, False otherwise
        """
        if len(songs) <= 1:
            return True
        
        # Count songs per artist
        artist_counts: Dict[str, int] = {}
        for song in songs:
            artist_key = song.artist.lower()
            artist_counts[artist_key] = artist_counts.get(artist_key, 0) + 1
        
        # Find the maximum count
        max_count = max(artist_counts.values())
        
        # According to the pigeonhole principle, if the most frequent artist
        # has more than ceil(n/2) songs, consecutive placement is inevitable
        # For n songs, if any artist has more than (n+1)//2 songs, arrangement is impossible
        return max_count <= (len(songs) + 1) // 2
    
    def get_artist_distribution(self, songs: List[Song]) -> Dict[str, int]:
        """
        Get the distribution of songs by artist.
        
        Time Complexity: O(n) where n is the number of songs
        Space Complexity: O(k) where k is the number of unique artists
        
        Args:
            songs (List[Song]): List of songs
            
        Returns:
            Dict[str, int]: Map of artist names to song counts
        """
        distribution: Dict[str, int] = {}
        for song in songs:
            artist_key = song.artist.lower()
            distribution[artist_key] = distribution.get(artist_key, 0) + 1
        return distribution