"""
Duplicate Cleaner module for PlayWise Music Engine.

Detects and handles duplicate songs based on normalized title+artist composite keys.
"""

import re
from typing import Dict, Optional, Literal
from playlist.song import Song


def normalize(text: str) -> str:
    """
    Normalize text by stripping, converting to lowercase, and collapsing whitespace.
    
    Args:
        text (str): Text to normalize
        
    Returns:
        str: Normalized text
    """
    if not text:
        return ""
    # Strip whitespace, convert to lowercase, and collapse multiple spaces to single space
    return re.sub(r'\s+', ' ', text.strip().lower())


class DuplicateCleaner:
    """
    Detects and handles duplicate songs based on normalized title+artist composite keys.
    
    Time Complexity:
        - is_duplicate: O(1) average case
        - register: O(1) average case
        - deregister: O(1) average case
        - cleanup_on_add: O(1) average case
    
    Space Complexity:
        - O(S) where S is the number of unique songs
    """
    
    def __init__(self, keep: Literal['first', 'latest'] = 'first'):
        """
        Initialize the duplicate cleaner.
        
        Args:
            keep (Literal['first', 'latest']): Policy for handling duplicates
                - 'first': Keep the first occurrence, reject subsequent duplicates
                - 'latest': Remove the old occurrence, keep the latest one
        """
        self.keep = keep
        # Map composite key to song_id for O(1) duplicate detection
        self.key_to_song_id: Dict[str, str] = {}
    
    def _make_key(self, title: str, artist: str) -> str:
        """
        Create a normalized composite key from title and artist.
        
        Args:
            title (str): Song title
            artist (str): Song artist
            
        Returns:
            str: Normalized composite key
        """
        return f"{normalize(title)}|{normalize(artist)}"
    
    def is_duplicate(self, title: str, artist: str) -> bool:
        """
        Check if a song with the given title and artist is already registered.
        
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        
        Args:
            title (str): Song title
            artist (str): Song artist
            
        Returns:
            bool: True if duplicate exists, False otherwise
        """
        key = self._make_key(title, artist)
        return key in self.key_to_song_id
    
    def register(self, song_id: str, title: str, artist: str) -> None:
        """
        Register a song with its composite key.
        
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        
        Args:
            song_id (str): Unique identifier for the song
            title (str): Song title
            artist (str): Song artist
        """
        key = self._make_key(title, artist)
        self.key_to_song_id[key] = song_id
    
    def deregister(self, song_id: str, title: str, artist: str) -> None:
        """
        Remove a song from the registry.
        
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        
        Args:
            song_id (str): Unique identifier for the song
            title (str): Song title
            artist (str): Song artist
        """
        key = self._make_key(title, artist)
        if key in self.key_to_song_id:
            del self.key_to_song_id[key]
    
    def cleanup_on_add(self, song_obj: Song) -> Optional[str]:
        """
        Handle duplicate detection and cleanup when adding a new song.
        
        Time Complexity: O(1) average case
        Space Complexity: O(1)
        
        Args:
            song_obj (Song): Song object to be added
            
        Returns:
            Optional[str]: None if song can be added, existing song_id if duplicate and keep='first'
        """
        # Check if this is a duplicate
        if self.is_duplicate(song_obj.title, song_obj.artist):
            key = self._make_key(song_obj.title, song_obj.artist)
            existing_song_id = self.key_to_song_id[key]
            
            if self.keep == 'first':
                # Reject the new song, return the existing one
                return existing_song_id
            elif self.keep == 'latest':
                # Remove the old song registration (caller should handle actual removal)
                # Just deregister the old one, caller will handle the rest
                pass
                
        # Register the new song
        self.register(song_obj.song_id, song_obj.title, song_obj.artist)
        return None