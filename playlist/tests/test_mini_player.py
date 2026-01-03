"""
Unit tests for the MiniPlayer module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from playlist.mini_player import MiniPlayer
from playlist.song import Song


def test_initialize_mini_player():
    """Test initializing a mini player."""
    player = MiniPlayer()
    assert player.get_window_size() == 5
    assert player.get_current_song() is None
    assert player.is_finished() is True
    assert player.get_upcoming_songs() == []
    assert player.get_played_songs() == []


def test_preload_songs():
    """Test preloading songs into the player."""
    player = MiniPlayer(window_size=3)
    
    songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist B", 200),
        Song("Song 3", "Artist C", 190),
        Song("Song 4", "Artist D", 210),
        Song("Song 5", "Artist E", 195)
    ]
    
    player.preload_songs(songs)
    
    # Only first 3 songs should be in upcoming (due to window size)
    upcoming = player.get_upcoming_songs()
    assert len(upcoming) == 3
    assert upcoming[0].title == "Song 1"
    assert upcoming[1].title == "Song 2"
    assert upcoming[2].title == "Song 3"
    
    # No songs should be played yet
    assert player.get_played_songs() == []
    assert player.get_current_song() is None


def test_play_next():
    """Test playing songs sequentially."""
    player = MiniPlayer(window_size=3)
    
    songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist B", 200),
        Song("Song 3", "Artist C", 190)
    ]
    
    player.preload_songs(songs)
    
    # Play first song
    song1 = player.play_next()
    assert song1 is not None
    assert song1.title == "Song 1"
    assert player.get_current_song().title == "Song 1"
    assert player.get_played_songs() == []
    assert len(player.get_upcoming_songs()) == 2
    
    # Play second song
    song2 = player.play_next()
    assert song2 is not None
    assert song2.title == "Song 2"
    assert player.get_current_song().title == "Song 2"
    assert len(player.get_played_songs()) == 1
    assert player.get_played_songs()[0].title == "Song 1"
    
    # Play third song
    song3 = player.play_next()
    assert song3 is not None
    assert song3.title == "Song 3"
    assert player.get_current_song().title == "Song 3"
    assert len(player.get_played_songs()) == 2
    
    # Try to play when no more songs
    song4 = player.play_next()
    assert song4 is None
    assert player.get_current_song() is None
    assert player.is_finished() is True


def test_set_window_size():
    """Test changing the window size."""
    player = MiniPlayer(window_size=2)
    
    songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist B", 200),
        Song("Song 3", "Artist C", 190),
        Song("Song 4", "Artist D", 210)
    ]
    
    player.preload_songs(songs)
    
    # Initially only 2 songs should be in upcoming
    upcoming = player.get_upcoming_songs()
    assert len(upcoming) == 2
    assert upcoming[0].title == "Song 1"
    assert upcoming[1].title == "Song 2"
    
    # Increase window size
    player.set_window_size(4)
    upcoming = player.get_upcoming_songs()
    assert len(upcoming) == 2  # Should still be 2 since we didn't reload
    
    # Preload again with new window size
    player.preload_songs(songs)
    upcoming = player.get_upcoming_songs()
    assert len(upcoming) == 4  # Now all 4 songs should fit
    
    # Decrease window size
    player.set_window_size(2)
    upcoming = player.get_upcoming_songs()
    assert len(upcoming) == 2  # Should be truncated to 2


def test_invalid_window_size():
    """Test setting invalid window size."""
    player = MiniPlayer()
    
    with pytest.raises(ValueError):
        player.set_window_size(0)
    
    with pytest.raises(ValueError):
        player.set_window_size(-1)


if __name__ == "__main__":
    pytest.main([__file__])