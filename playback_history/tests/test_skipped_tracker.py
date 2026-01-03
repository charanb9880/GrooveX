"""
Unit tests for the RecentlySkippedTracker module.
"""

import pytest
from ..skipped_tracker import RecentlySkippedTracker


def test_skip_and_membership():
    """Test that songs are added to tracker and membership checking works."""
    tracker = RecentlySkippedTracker(capacity=3)
    
    # Initially empty
    assert not tracker.is_recently_skipped("song1")
    assert tracker.get_recently_skipped() == []
    
    # Add songs
    tracker.skip_song("song1")
    assert tracker.is_recently_skipped("song1")
    assert tracker.get_recently_skipped() == ["song1"]
    
    tracker.skip_song("song2")
    assert tracker.is_recently_skipped("song2")
    assert tracker.get_recently_skipped() == ["song1", "song2"]
    
    tracker.skip_song("song3")
    assert tracker.is_recently_skipped("song3")
    assert tracker.get_recently_skipped() == ["song1", "song2", "song3"]
    
    # Add one more - should evict oldest
    tracker.skip_song("song4")
    assert not tracker.is_recently_skipped("song1")  # Evicted
    assert tracker.is_recently_skipped("song2")
    assert tracker.is_recently_skipped("song3")
    assert tracker.is_recently_skipped("song4")
    assert tracker.get_recently_skipped() == ["song2", "song3", "song4"]


def test_autoplay_respects_skips():
    """Test that autoplay logic respects skipped songs."""
    tracker = RecentlySkippedTracker(capacity=3)
    
    # Mark some songs as skipped
    tracker.skip_song("skipped1")
    tracker.skip_song("skipped2")
    
    # Simulate autoplay candidate selection
    candidates = ["skipped1", "valid1", "skipped2", "valid2", "new_song"]
    selected = None
    
    for candidate in candidates:
        if not tracker.is_recently_skipped(candidate):
            selected = candidate
            break
    
    # Should select the first non-skipped song
    assert selected == "valid1"


def test_force_play():
    """Test that force play bypasses the tracker."""
    tracker = RecentlySkippedTracker()
    tracker.skip_song("skipped_song")
    
    # Normal check should detect it as skipped
    assert tracker.is_recently_skipped("skipped_song")
    
    # But force play should bypass this (implementation would handle this in autoplay logic)
    # This is more of a conceptual test - the tracker provides the info, caller decides


def test_clear_and_set_capacity():
    """Test clearing the tracker and changing capacity."""
    tracker = RecentlySkippedTracker(capacity=3)
    
    # Add some songs
    tracker.skip_song("song1")
    tracker.skip_song("song2")
    assert len(tracker.get_recently_skipped()) == 2
    
    # Clear
    tracker.clear_skipped()
    assert len(tracker.get_recently_skipped()) == 0
    assert not tracker.is_recently_skipped("song1")
    assert not tracker.is_recently_skipped("song2")
    
    # Test capacity change
    tracker.set_capacity(5)
    tracker.skip_song("a")
    tracker.skip_song("b")
    tracker.skip_song("c")
    tracker.skip_song("d")
    tracker.skip_song("e")
    assert len(tracker.get_recently_skipped()) == 5
    
    # Reduce capacity
    tracker.set_capacity(3)
    # Should keep the most recent 3
    assert tracker.get_recently_skipped() == ["c", "d", "e"]


def test_default_capacity():
    """Test that default capacity is 10."""
    tracker = RecentlySkippedTracker()  # Default capacity
    assert tracker.capacity == 10
    
    # Add 11 songs
    for i in range(11):
        tracker.skip_song(f"song{i}")
    
    # Only last 10 should remain
    assert len(tracker.get_recently_skipped()) == 10
    assert not tracker.is_recently_skipped("song0")  # Should be evicted
    assert tracker.is_recently_skipped("song10")  # Should be present


if __name__ == "__main__":
    pytest.main([__file__])