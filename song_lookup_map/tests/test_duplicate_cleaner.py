"""
Unit tests for the DuplicateCleaner module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from song_lookup_map.duplicate_cleaner import DuplicateCleaner, normalize
from playlist.song import Song


def test_normalize():
    """Test the normalize function."""
    # Test basic normalization
    assert normalize("  Hello World  ") == "hello world"
    assert normalize("HELLO  WORLD") == "hello world"
    assert normalize("Hello\tWorld") == "hello world"
    assert normalize("Hello\nWorld") == "hello world"
    assert normalize("  HELLO   WORLD  ") == "hello world"
    
    # Test edge cases
    assert normalize("") == ""
    assert normalize("   ") == ""
    # Note: normalize(None) would cause an error, so we don't test it


def test_duplicate_cleaner_first_policy():
    """Test DuplicateCleaner with 'first' policy."""
    cleaner = DuplicateCleaner(keep='first')
    
    # Add first song
    song1 = Song("Hello", "Artist", 180, song_id="1")
    result = cleaner.cleanup_on_add(song1)
    assert result is None  # No duplicate, song can be added
    
    # Try to add duplicate
    song2 = Song("Hello", "Artist", 200, song_id="2")
    result = cleaner.cleanup_on_add(song2)
    assert result == "1"  # Should return existing song ID
    
    # Add another non-duplicate song
    song3 = Song("Hello", "Different Artist", 180, song_id="3")
    result = cleaner.cleanup_on_add(song3)
    assert result is None  # No duplicate, song can be added
    
    # Test case insensitivity
    song4 = Song("HELLO", "ARTIST", 180, song_id="4")
    result = cleaner.cleanup_on_add(song4)
    assert result == "1"  # Should return existing song ID


def test_duplicate_cleaner_latest_policy():
    """Test DuplicateCleaner with 'latest' policy."""
    cleaner = DuplicateCleaner(keep='latest')
    
    # Add first song
    song1 = Song("Hello", "Artist", 180, song_id="1")
    result = cleaner.cleanup_on_add(song1)
    assert result is None  # No duplicate, song can be added
    
    # Try to add duplicate
    song2 = Song("Hello", "Artist", 200, song_id="2")
    result = cleaner.cleanup_on_add(song2)
    assert result is None  # With 'latest' policy, new song is accepted
    
    # Verify the key still exists but now maps to the new song
    key = cleaner._make_key("Hello", "Artist")
    assert key in cleaner.key_to_song_id
    assert cleaner.key_to_song_id[key] == "2"  # Should now map to the new song ID


def test_is_duplicate():
    """Test the is_duplicate method."""
    cleaner = DuplicateCleaner()
    
    # Initially no duplicates
    assert not cleaner.is_duplicate("Song", "Artist")
    
    # Register a song
    cleaner.register("1", "Song", "Artist")
    
    # Now it should be a duplicate
    assert cleaner.is_duplicate("Song", "Artist")
    assert cleaner.is_duplicate("  SONG  ", "  ARTIST  ")  # Test normalization
    
    # Different song should not be duplicate
    assert not cleaner.is_duplicate("Different Song", "Artist")


def test_register_and_deregister():
    """Test register and deregister methods."""
    cleaner = DuplicateCleaner()
    
    # Register a song
    cleaner.register("1", "Song", "Artist")
    assert cleaner.is_duplicate("Song", "Artist")
    
    # Deregister the song
    cleaner.deregister("1", "Song", "Artist")
    assert not cleaner.is_duplicate("Song", "Artist")
    
    # Deregister non-existent song should not fail
    cleaner.deregister("2", "Non-existent", "Song")
    assert not cleaner.is_duplicate("Non-existent", "Song")


if __name__ == "__main__":
    pytest.main([__file__])