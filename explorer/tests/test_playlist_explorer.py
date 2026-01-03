"""
Unit tests for the PlaylistExplorer module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from explorer.playlist_explorer import PlaylistExplorer, normalize_text


def test_normalize_text():
    """Test the normalize_text function."""
    # Test basic normalization
    assert normalize_text("  Hello World  ") == "hello world"
    assert normalize_text("HELLO  WORLD") == "hello world"
    assert normalize_text("Hello\tWorld") == "hello world"
    assert normalize_text("Hello\nWorld") == "hello world"
    assert normalize_text("  HELLO   WORLD  ") == "hello world"
    
    # Test edge cases
    assert normalize_text("") == ""
    assert normalize_text("   ") == ""
    assert normalize_text(None) == ""


def test_add_and_traverse():
    """Test adding songs and traversing the explorer tree."""
    explorer = PlaylistExplorer()
    
    # Add songs in different branches
    explorer.add_song("song1", "Rock", "Alternative", "Melancholic", "Radiohead")
    explorer.add_song("song2", "Rock", "Alternative", "Upbeat", "Arctic Monkeys")
    explorer.add_song("song3", "Pop", "Dance", "Energetic", "Dua Lipa")
    explorer.add_song("song4", "Rock", "Classic", None, "Queen")
    
    # Test DFS traversal
    dfs_nodes = list(explorer.traverse(method='dfs'))
    assert len(dfs_nodes) > 0  # Should have multiple nodes
    
    # Test BFS traversal
    bfs_nodes = list(explorer.traverse(method='bfs'))
    assert len(bfs_nodes) > 0  # Should have multiple nodes
    
    # Verify root node is first in BFS
    root_path, root_node = bfs_nodes[0]
    assert root_path == []
    assert root_node.key == ""


def test_get_by_path():
    """Test getting songs by path."""
    explorer = PlaylistExplorer()
    
    # Add songs
    explorer.add_song("song1", "Rock", "Alternative", "Melancholic", "Radiohead")
    explorer.add_song("song2", "Rock", "Alternative", "Upbeat", "Arctic Monkeys")
    explorer.add_song("song3", "Pop", "Dance", "Energetic", "Dua Lipa")
    
    # Test getting songs at specific paths
    rock_songs = explorer.get_by_path(["rock"])
    assert len(rock_songs) == 0  # No songs directly at genre level
    
    rock_alt_songs = explorer.get_by_path(["rock", "alternative"])
    assert len(rock_alt_songs) == 0  # No songs directly at subgenre level
    
    radiohead_songs = explorer.get_by_path(["rock", "alternative", "melancholic", "radiohead"])
    assert "song1" in radiohead_songs
    assert "song2" not in radiohead_songs
    
    # Test with subtree inclusion
    rock_alt_with_subtree = explorer.get_by_path(["rock", "alternative"], include_subtree=True)
    assert "song1" in rock_alt_with_subtree
    assert "song2" in rock_alt_with_subtree


def test_remove_song():
    """Test removing songs from the explorer."""
    explorer = PlaylistExplorer()
    
    # Add songs
    explorer.add_song("song1", "Rock", "Alternative", "Melancholic", "Radiohead")
    explorer.add_song("song2", "Rock", "Alternative", "Upbeat", "Arctic Monkeys")
    
    # Verify songs are added
    radiohead_songs = explorer.get_by_path(["rock", "alternative", "melancholic", "radiohead"])
    assert "song1" in radiohead_songs
    
    # Remove song
    explorer.remove_song("song1")
    
    # Verify song is removed
    radiohead_songs = explorer.get_by_path(["rock", "alternative", "melancholic", "radiohead"])
    assert "song1" not in radiohead_songs
    
    # Verify reverse map is cleaned up
    assert "song1" not in explorer.song_to_paths


def test_search():
    """Test searching for songs with criteria."""
    explorer = PlaylistExplorer()
    
    # Add songs
    explorer.add_song("song1", "Rock", "Alternative", "Melancholic", "Radiohead")
    explorer.add_song("song2", "Rock", "Alternative", "Upbeat", "Arctic Monkeys")
    explorer.add_song("song3", "Pop", "Dance", "Energetic", "Dua Lipa")
    explorer.add_song("song4", "Rock", "Classic", None, "Queen")
    
    # Search by genre only
    rock_songs = explorer.search({"genre": "Rock"})
    # Should include songs from all Rock subgenres
    assert "song1" in rock_songs
    assert "song2" in rock_songs
    assert "song4" in rock_songs
    assert "song3" not in rock_songs  # Pop song should not be included
    
    # Search by genre and subgenre
    alt_rock_songs = explorer.search({"genre": "Rock", "subgenre": "Alternative"})
    assert "song1" in alt_rock_songs
    assert "song2" in alt_rock_songs
    assert "song3" not in alt_rock_songs
    assert "song4" not in alt_rock_songs  # Classic Rock should not be included
    
    # Search by genre that doesn't exist
    jazz_songs = explorer.search({"genre": "Jazz"})
    assert len(jazz_songs) == 0
    
    # Search with no criteria
    all_songs = explorer.search({})
    assert len(all_songs) == 0


def test_case_insensitive_and_normalization():
    """Test that the explorer handles case and whitespace normalization correctly."""
    explorer = PlaylistExplorer()
    
    # Add song with irregular casing and spacing
    explorer.add_song("song1", "  ROCK  ", " alternative ", " melancholic ", " radiohead ")
    
    # Search with different casing and spacing should still work
    songs = explorer.search({"genre": "rock", "subgenre": "ALTERNATIVE"})
    assert "song1" in songs
    
    # Get by path with different casing should work
    songs = explorer.get_by_path(["ROCK", "ALTERNATIVE", "MELANCHOLIC", "RADIOHEAD"])
    assert "song1" in songs


if __name__ == "__main__":
    pytest.main([__file__])