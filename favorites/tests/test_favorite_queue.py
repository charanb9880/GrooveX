"""
Unit tests for the FavoriteQueue module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from favorites.favorite_queue import FavoriteQueue, SongSummary


def test_add_and_remove_favorites():
    """Test adding and removing songs from favorites."""
    fav_queue = FavoriteQueue()
    
    # Initially empty
    top_songs = fav_queue.get_top_n(5)
    assert len(top_songs) == 0
    
    # Add songs to favorites
    fav_queue.add_to_favorites("1", "Song 1", "Artist 1")
    fav_queue.add_to_favorites("2", "Song 2", "Artist 2")
    fav_queue.add_to_favorites("3", "Song 3", "Artist 3")
    
    # Check they're tracked
    assert len(fav_queue.favorites) == 3
    
    # Remove one
    fav_queue.remove_from_favorites("2")
    assert len(fav_queue.favorites) == 2
    assert "2" not in fav_queue.favorites


def test_record_listen_and_top_n():
    """Test recording listens and getting top N songs."""
    fav_queue = FavoriteQueue()
    
    # Add songs to favorites
    fav_queue.add_to_favorites("1", "Song 1", "Artist 1")
    fav_queue.add_to_favorites("2", "Song 2", "Artist 2")
    fav_queue.add_to_favorites("3", "Song 3", "Artist 3")
    
    # Record listens
    fav_queue.record_listen("1", 100)  # Song 1: 100 seconds
    fav_queue.record_listen("2", 200)  # Song 2: 200 seconds
    fav_queue.record_listen("3", 150)  # Song 3: 150 seconds
    
    # Get top 2
    top_songs = fav_queue.get_top_n(2)
    assert len(top_songs) == 2
    assert top_songs[0].song_id == "2"  # Song 2 with 200 seconds
    assert top_songs[1].song_id == "3"  # Song 3 with 150 seconds
    
    # Record more listens for Song 1
    fav_queue.record_listen("1", 150)  # Song 1 now has 250 seconds
    
    # Get top 2 again
    top_songs = fav_queue.get_top_n(2)
    assert len(top_songs) == 2
    assert top_songs[0].song_id == "1"  # Song 1 now with 250 seconds
    assert top_songs[1].song_id == "2"  # Song 2 with 200 seconds


def test_lazy_update_heap():
    """Test that the lazy update mechanism works correctly."""
    fav_queue = FavoriteQueue()
    
    # Add songs to favorites
    fav_queue.add_to_favorites("1", "Song 1", "Artist 1")
    fav_queue.add_to_favorites("2", "Song 2", "Artist 2")
    
    # Record listens
    fav_queue.record_listen("1", 100)
    fav_queue.record_listen("2", 200)
    
    # Manually add a stale entry to the heap
    import heapq
    heapq.heappush(fav_queue.heap, (-50, 0.0, "1"))  # Stale entry with outdated time
    
    # Get top 2 - should filter out stale entry
    top_songs = fav_queue.get_top_n(2)
    assert len(top_songs) == 2
    assert top_songs[0].song_id == "2"  # Song 2 with 200 seconds
    assert top_songs[1].song_id == "1"  # Song 1 with 100 seconds (not 50 from stale)


def test_non_favorite_songs_ignored():
    """Test that non-favorite songs are ignored."""
    fav_queue = FavoriteQueue()
    
    # Add one song to favorites and record a listen
    fav_queue.add_to_favorites("1", "Song 1", "Artist 1")
    fav_queue.record_listen("1", 100)  # Record a listen so it appears in results
    
    # Record listens for a non-favorite song
    fav_queue.record_listen("2", 1000)  # This should be ignored
    
    # Get top songs - should only include favorite songs
    top_songs = fav_queue.get_top_n(5)
    assert len(top_songs) == 1
    assert top_songs[0].song_id == "1"
    assert top_songs[0].total_listen_time == 100  # Listen was recorded for favorite


def test_clear():
    """Test clearing all data."""
    fav_queue = FavoriteQueue()
    
    # Add songs and record listens
    fav_queue.add_to_favorites("1", "Song 1", "Artist 1")
    fav_queue.add_to_favorites("2", "Song 2", "Artist 2")
    fav_queue.record_listen("1", 100)
    fav_queue.record_listen("2", 200)
    
    # Verify data exists
    assert len(fav_queue.favorites) == 2
    assert len(fav_queue.song_listen_times) == 2
    assert len(fav_queue.heap) > 0
    
    # Clear all data
    fav_queue.clear()
    
    # Verify all data is cleared
    assert len(fav_queue.favorites) == 0
    assert len(fav_queue.song_listen_times) == 0
    assert len(fav_queue.heap) == 0
    
    # Get top songs should return empty list
    top_songs = fav_queue.get_top_n(5)
    assert len(top_songs) == 0


if __name__ == "__main__":
    pytest.main([__file__])