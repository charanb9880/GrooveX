"""
Unit tests for the Play Duration Visualizer feature in SystemDashboard.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from system_dashboard.dashboard import SystemDashboard
from playlist.playlist import Playlist
from playback_history.playback_controller import PlaybackController
from song_rating_tree.song_rating_engine import SongRatingEngine
from song_lookup_map.lookup_map import SongLookupMap
from playlist.song import Song


def test_empty_playlist_visualization():
    """Test play duration visualization with empty playlist."""
    playlist = Playlist()
    playback_controller = PlaybackController()
    rating_engine = SongRatingEngine()
    lookup_map = SongLookupMap()
    
    dashboard = SystemDashboard(playlist, playback_controller, rating_engine, lookup_map)
    viz_data = dashboard.get_play_duration_visualization()
    
    assert viz_data['total_playtime'] == 0
    assert viz_data['longest_song'] is None
    assert viz_data['shortest_song'] is None
    assert viz_data['song_count'] == 0


def test_single_song_visualization():
    """Test play duration visualization with single song."""
    playlist = Playlist()
    playback_controller = PlaybackController()
    rating_engine = SongRatingEngine()
    lookup_map = SongLookupMap()
    
    # Add one song
    playlist.add_song("Imagine", "John Lennon", 183)
    
    dashboard = SystemDashboard(playlist, playback_controller, rating_engine, lookup_map)
    viz_data = dashboard.get_play_duration_visualization()
    
    assert viz_data['total_playtime'] == 183
    assert viz_data['song_count'] == 1
    
    # With only one song, longest and shortest should be the same
    assert viz_data['longest_song']['title'] == "Imagine"
    assert viz_data['longest_song']['artist'] == "John Lennon"
    assert viz_data['longest_song']['duration'] == 183
    
    assert viz_data['shortest_song']['title'] == "Imagine"
    assert viz_data['shortest_song']['artist'] == "John Lennon"
    assert viz_data['shortest_song']['duration'] == 183


def test_multiple_songs_visualization():
    """Test play duration visualization with multiple songs."""
    playlist = Playlist()
    playback_controller = PlaybackController()
    rating_engine = SongRatingEngine()
    lookup_map = SongLookupMap()
    
    # Add multiple songs with different durations
    playlist.add_song("Short Song", "Artist A", 120)      # 2 minutes
    playlist.add_song("Medium Song", "Artist B", 240)     # 4 minutes
    playlist.add_song("Long Song", "Artist C", 360)       # 6 minutes
    
    dashboard = SystemDashboard(playlist, playback_controller, rating_engine, lookup_map)
    viz_data = dashboard.get_play_duration_visualization()
    
    # Check total playtime
    assert viz_data['total_playtime'] == 720  # 120 + 240 + 360
    assert viz_data['song_count'] == 3
    
    # Check longest song
    assert viz_data['longest_song']['title'] == "Long Song"
    assert viz_data['longest_song']['artist'] == "Artist C"
    assert viz_data['longest_song']['duration'] == 360
    
    # Check shortest song
    assert viz_data['shortest_song']['title'] == "Short Song"
    assert viz_data['shortest_song']['artist'] == "Artist A"
    assert viz_data['shortest_song']['duration'] == 120


def test_visualization_with_zero_duration_song():
    """Test visualization with a song that has zero duration."""
    playlist = Playlist()
    playback_controller = PlaybackController()
    rating_engine = SongRatingEngine()
    lookup_map = SongLookupMap()
    
    # Add songs including one with zero duration
    playlist.add_song("Zero Duration", "Artist A", 0)
    playlist.add_song("Normal Song", "Artist B", 180)
    
    dashboard = SystemDashboard(playlist, playback_controller, rating_engine, lookup_map)
    viz_data = dashboard.get_play_duration_visualization()
    
    # Check total playtime
    assert viz_data['total_playtime'] == 180  # 0 + 180
    assert viz_data['song_count'] == 2
    
    # Zero duration song should be the shortest
    assert viz_data['shortest_song']['title'] == "Zero Duration"
    assert viz_data['shortest_song']['duration'] == 0
    
    # Normal song should be the longest
    assert viz_data['longest_song']['title'] == "Normal Song"
    assert viz_data['longest_song']['duration'] == 180


if __name__ == "__main__":
    pytest.main([__file__])