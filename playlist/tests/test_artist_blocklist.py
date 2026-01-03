"""
Unit tests for the ArtistBlocklist module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from playlist.artist_blocklist import ArtistBlocklist


def test_initialize_blocklist():
    """Test initializing an empty artist blocklist."""
    blocklist = ArtistBlocklist()
    assert len(blocklist.get_blocked_artists()) == 0


def test_add_artist():
    """Test adding artists to the blocklist."""
    blocklist = ArtistBlocklist()
    
    # Add single artist
    blocklist.add_artist("The Beatles")
    blocked = blocklist.get_blocked_artists()
    assert len(blocked) == 1
    assert "the beatles" in blocked
    
    # Add another artist
    blocklist.add_artist("Queen")
    blocked = blocklist.get_blocked_artists()
    assert len(blocked) == 2
    assert "the beatles" in blocked
    assert "queen" in blocked
    
    # Add duplicate artist (should not increase count)
    blocklist.add_artist("THE BEATLES")
    blocked = blocklist.get_blocked_artists()
    assert len(blocked) == 2  # Should still be 2


def test_remove_artist():
    """Test removing artists from the blocklist."""
    blocklist = ArtistBlocklist()
    
    # Add some artists
    blocklist.add_artist("The Beatles")
    blocklist.add_artist("Queen")
    blocklist.add_artist("Led Zeppelin")
    
    # Remove existing artist
    result = blocklist.remove_artist("Queen")
    assert result is True
    blocked = blocklist.get_blocked_artists()
    assert len(blocked) == 2
    assert "the beatles" in blocked
    assert "queen" not in blocked
    assert "led zeppelin" in blocked
    
    # Remove non-existent artist
    result = blocklist.remove_artist("Non Existent")
    assert result is False
    assert len(blocklist.get_blocked_artists()) == 2


def test_is_blocked():
    """Test checking if an artist is blocked."""
    blocklist = ArtistBlocklist()
    
    # Add some artists
    blocklist.add_artist("The Beatles")
    blocklist.add_artist("Queen")
    
    # Check blocked artists
    assert blocklist.is_blocked("The Beatles") is True
    assert blocklist.is_blocked("THE BEATLES") is True
    assert blocklist.is_blocked("the beatles") is True
    assert blocklist.is_blocked("Queen") is True
    
    # Check non-blocked artists
    assert blocklist.is_blocked("Led Zeppelin") is False
    assert blocklist.is_blocked("Non Existent") is False


def test_normalize_artist():
    """Test artist name normalization."""
    blocklist = ArtistBlocklist()
    
    # Test various formats
    blocklist.add_artist("  The Beatles  ")
    assert blocklist.is_blocked("The Beatles") is True
    assert blocklist.is_blocked("the beatles") is True
    assert blocklist.is_blocked("THE BEATLES") is True
    
    # Test empty string
    blocklist.add_artist("")
    assert blocklist.is_blocked("") is True
    
    # Test None (converted to empty string)
    blocklist.add_artist(None)
    assert blocklist.is_blocked("") is True


def test_clear_blocklist():
    """Test clearing all artists from the blocklist."""
    blocklist = ArtistBlocklist()
    
    # Add some artists
    blocklist.add_artist("The Beatles")
    blocklist.add_artist("Queen")
    blocklist.add_artist("Led Zeppelin")
    
    assert len(blocklist.get_blocked_artists()) == 3
    
    # Clear the blocklist
    blocklist.clear()
    assert len(blocklist.get_blocked_artists()) == 0


def test_get_blocked_artists_returns_copy():
    """Test that get_blocked_artists returns a copy, not the original set."""
    blocklist = ArtistBlocklist()
    blocklist.add_artist("The Beatles")
    
    blocked = blocklist.get_blocked_artists()
    blocked.add("queen")  # Modify the returned set
    
    # Original set should not be affected
    original_blocked = blocklist.get_blocked_artists()
    assert len(original_blocked) == 1
    assert "the beatles" in original_blocked
    assert "queen" not in original_blocked


if __name__ == "__main__":
    pytest.main([__file__])