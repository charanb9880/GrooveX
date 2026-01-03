"""
Unit tests for the merge playlists functionality.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from playlist.playlist import Playlist
from playlist.song import Song


def test_merge_empty_playlists():
    """Test merging two empty playlists."""
    playlist1 = Playlist()
    playlist2 = Playlist()
    
    merged = playlist1.merge_alternately(playlist2)
    
    assert merged.is_empty() is True
    assert len(merged.get_all_songs()) == 0


def test_merge_with_empty_playlist():
    """Test merging a playlist with an empty playlist."""
    playlist1 = Playlist()
    playlist1.add_song("Song 1", "Artist A", 180)
    playlist1.add_song("Song 2", "Artist B", 200)
    
    playlist2 = Playlist()
    
    merged = playlist1.merge_alternately(playlist2)
    
    songs = merged.get_all_songs()
    assert len(songs) == 2
    assert songs[0].title == "Song 1"
    assert songs[1].title == "Song 2"


def test_merge_empty_with_nonempty_playlist():
    """Test merging an empty playlist with a non-empty playlist."""
    playlist1 = Playlist()
    
    playlist2 = Playlist()
    playlist2.add_song("Song 1", "Artist A", 180)
    playlist2.add_song("Song 2", "Artist B", 200)
    
    merged = playlist1.merge_alternately(playlist2)
    
    songs = merged.get_all_songs()
    assert len(songs) == 2
    assert songs[0].title == "Song 1"
    assert songs[1].title == "Song 2"


def test_merge_equal_length_playlists():
    """Test merging two playlists of equal length."""
    playlist1 = Playlist()
    playlist1.add_song("Song A1", "Artist A", 180)
    playlist1.add_song("Song A2", "Artist A", 200)
    playlist1.add_song("Song A3", "Artist A", 190)
    
    playlist2 = Playlist()
    playlist2.add_song("Song B1", "Artist B", 210)
    playlist2.add_song("Song B2", "Artist B", 195)
    playlist2.add_song("Song B3", "Artist B", 205)
    
    merged = playlist1.merge_alternately(playlist2)
    
    songs = merged.get_all_songs()
    assert len(songs) == 6
    
    # Check alternating pattern
    assert songs[0].title == "Song A1"  # First from playlist1
    assert songs[1].title == "Song B1"  # First from playlist2
    assert songs[2].title == "Song A2"  # Second from playlist1
    assert songs[3].title == "Song B2"  # Second from playlist2
    assert songs[4].title == "Song A3"  # Third from playlist1
    assert songs[5].title == "Song B3"  # Third from playlist2


def test_merge_unequal_length_playlists():
    """Test merging two playlists of unequal length."""
    playlist1 = Playlist()
    playlist1.add_song("Song A1", "Artist A", 180)
    playlist1.add_song("Song A2", "Artist A", 200)
    playlist1.add_song("Song A3", "Artist A", 190)
    playlist1.add_song("Song A4", "Artist A", 210)
    playlist1.add_song("Song A5", "Artist A", 195)
    
    playlist2 = Playlist()
    playlist2.add_song("Song B1", "Artist B", 210)
    playlist2.add_song("Song B2", "Artist B", 195)
    
    merged = playlist1.merge_alternately(playlist2)
    
    songs = merged.get_all_songs()
    assert len(songs) == 7
    
    # Check alternating pattern for first 4 songs
    assert songs[0].title == "Song A1"  # First from playlist1
    assert songs[1].title == "Song B1"  # First from playlist2
    assert songs[2].title == "Song A2"  # Second from playlist1
    assert songs[3].title == "Song B2"  # Second from playlist2
    assert songs[4].title == "Song A3"  # Third from playlist1 (remaining from playlist1)
    assert songs[5].title == "Song A4"  # Fourth from playlist1 (remaining from playlist1)
    assert songs[6].title == "Song A5"  # Fifth from playlist1 (remaining from playlist1)


def test_merge_single_song_playlists():
    """Test merging playlists with single songs."""
    playlist1 = Playlist()
    playlist1.add_song("Song 1", "Artist A", 180)
    
    playlist2 = Playlist()
    playlist2.add_song("Song 2", "Artist B", 200)
    
    merged = playlist1.merge_alternately(playlist2)
    
    songs = merged.get_all_songs()
    assert len(songs) == 2
    assert songs[0].title == "Song 1"
    assert songs[1].title == "Song 2"


if __name__ == "__main__":
    pytest.main([__file__])