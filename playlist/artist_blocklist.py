"""
Artist Blocklist module for PlayWise Music Engine.

Implements a HashSet-based blocklist for permanently avoiding songs by certain artists.
"""

from typing import Set


class ArtistBlocklist:
    """
    Manages a blocklist of artists that should be permanently avoided.
    
    Uses a HashSet (Python set) for O(1) membership checking.
    
    Time Complexity:
        - add_artist: O(1) average case
        - remove_artist: O(1) average case
        - is_blocked: O(1) average case
        - get_blocked_artists: O(n) where n is the number of blocked artists
    
    Space Complexity:
        - O(n) where n is the number of blocked artists
    """
    
    def __init__(self):
        """Initialize an empty artist blocklist."""
        self._blocked_artists: Set[str] = set()
    
    def add_artist(self, artist: str) -> None:
        """
        Add an artist to the blocklist.
        
        Time Complexity: O(1) average case
        Space Complexity: O(1) if artist already exists, O(1) additional space if new
        
        Args:
            artist (str): The artist name to block
        """
        # Normalize the artist name for consistent matching
        normalized_artist = self._normalize_artist(artist)
        self._blocked_artists.add(normalized_artist)
    
    def remove_artist(self, artist: str) -> bool:
        """
        Remove an artist from the blocklist.
        
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        
        Args:
            artist (str): The artist name to remove from blocklist
            
        Returns:
            bool: True if artist was in blocklist and removed, False if not found
        """
        normalized_artist = self._normalize_artist(artist)
        if normalized_artist in self._blocked_artists:
            self._blocked_artists.discard(normalized_artist)
            return True
        return False
    
    def is_blocked(self, artist: str) -> bool:
        """
        Check if an artist is in the blocklist.
        
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        
        Args:
            artist (str): The artist name to check
            
        Returns:
            bool: True if artist is blocked, False otherwise
        """
        normalized_artist = self._normalize_artist(artist)
        return normalized_artist in self._blocked_artists
    
    def get_blocked_artists(self) -> Set[str]:
        """
        Get a copy of all blocked artists.
        
        Time Complexity: O(n) where n is the number of blocked artists
        Space Complexity: O(n) for the returned set
        
        Returns:
            Set[str]: A copy of the set of blocked artists
        """
        return self._blocked_artists.copy()
    
    def _normalize_artist(self, artist: str) -> str:
        """
        Normalize artist name for consistent matching.
        
        Args:
            artist (str): The artist name to normalize
            
        Returns:
            str: Normalized artist name
        """
        if not artist:
            return ""
        return artist.strip().lower()
    
    def clear(self) -> None:
        """
        Clear all artists from the blocklist.
        
        Time Complexity: O(1) amortized
        Space Complexity: O(1)
        """
        self._blocked_artists.clear()