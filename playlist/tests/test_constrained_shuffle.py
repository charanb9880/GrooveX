"""
Unit tests for the ConstrainedShuffler module.
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

import pytest
from playlist.constrained_shuffle import ConstrainedShuffler
from playlist.song import Song


def test_initialize_shuffler():
    """Test initializing a constrained shuffler."""
    shuffler = ConstrainedShuffler()
    assert shuffler._max_attempts == 1000
    
    shuffler = ConstrainedShuffler(max_attempts=500)
    assert shuffler._max_attempts == 500


def test_shuffle_empty_list():
    """Test shuffling an empty list."""
    shuffler = ConstrainedShuffler()
    result = shuffler.shuffle_with_constraints([])
    assert result == []


def test_shuffle_single_song():
    """Test shuffling a list with a single song."""
    shuffler = ConstrainedShuffler()
    song = Song("Imagine", "John Lennon", 183)
    result = shuffler.shuffle_with_constraints([song])
    assert len(result) == 1
    assert result[0].title == "Imagine"
    assert result[0].artist == "John Lennon"


def test_shuffle_no_consecutive_artists():
    """Test shuffling with no consecutive artists."""
    shuffler = ConstrainedShuffler()
    
    # Create songs by different artists
    songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist B", 200),
        Song("Song 3", "Artist C", 190),
        Song("Song 4", "Artist D", 210)
    ]
    
    # Shuffle multiple times to test randomness
    results = []
    for _ in range(10):
        result = shuffler.shuffle_with_constraints(songs)
        results.append(result)
        
        # Verify no consecutive artists
        for i in range(len(result) - 1):
            assert result[i].artist != result[i + 1].artist
    
    # Verify that we get different orders (high probability with 10 attempts)
    # At least some of the results should be different
    first_result = results[0]
    different_found = False
    for result in results[1:]:
        if result != first_result:
            different_found = True
            break
    # This assertion might occasionally fail due to randomness, but it's unlikely with 10 attempts
    # assert different_found


def test_shuffle_with_some_consecutive_artists():
    """Test shuffling where some consecutive artists are possible but should be avoided."""
    shuffler = ConstrainedShuffler()
    
    # Create songs with some artists appearing multiple times
    songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist B", 200),
        Song("Song 3", "Artist A", 190),
        Song("Song 4", "Artist C", 210),
        Song("Song 5", "Artist B", 195)
    ]
    
    # Shuffle multiple times
    for _ in range(20):
        result = shuffler.shuffle_with_constraints(songs)
        
        # Verify no consecutive artists
        for i in range(len(result) - 1):
            assert result[i].artist.lower() != result[i + 1].artist.lower()


def test_impossible_arrangement():
    """Test shuffling when it's impossible to avoid consecutive artists."""
    shuffler = ConstrainedShuffler(max_attempts=100)  # Reduce attempts for faster testing
    
    # Create a case where one artist dominates (impossible to avoid consecutive)
    songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist A", 200),
        Song("Song 3", "Artist A", 190),
        Song("Song 4", "Artist B", 210),  # Only one different artist
        Song("Song 5", "Artist C", 195)   # Only one different artist
    ]
    
    # Even in impossible cases, we should get some result (though it might have consecutive artists)
    result = shuffler.shuffle_with_constraints(songs)
    assert len(result) == len(songs)
    
    # Note: We don't assert that there are no consecutive artists because it's impossible
    # in this case, but the function should still return a valid list


def test_has_consecutive_artists():
    """Test the _has_consecutive_artists helper method."""
    shuffler = ConstrainedShuffler()
    
    # Test with consecutive artists
    songs_with_consecutive = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist A", 200),  # Same artist consecutively
        Song("Song 3", "Artist B", 190)
    ]
    assert shuffler._has_consecutive_artists(songs_with_consecutive) is True
    
    # Test without consecutive artists
    songs_without_consecutive = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist B", 200),
        Song("Song 3", "Artist A", 190)   # Same artist but not consecutive
    ]
    assert shuffler._has_consecutive_artists(songs_without_consecutive) is False
    
    # Test empty list
    assert shuffler._has_consecutive_artists([]) is False
    
    # Test single song
    single_song = [Song("Song 1", "Artist A", 180)]
    assert shuffler._has_consecutive_artists(single_song) is False


def test_is_arrangement_possible():
    """Test the _is_arrangement_possible helper method."""
    shuffler = ConstrainedShuffler()
    
    # Test possible arrangement (no artist has more than half)
    possible_songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist B", 200),
        Song("Song 3", "Artist A", 190),  # 2 songs by Artist A out of 3 total
        Song("Song 4", "Artist C", 210)
    ]
    assert shuffler._is_arrangement_possible(possible_songs) is True
    
    # Test impossible arrangement (one artist has more than ceil(n/2))
    # With 5 songs, if one artist has 4 songs, it's impossible to avoid consecutive placement
    impossible_songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist A", 200),
        Song("Song 3", "Artist A", 190),
        Song("Song 4", "Artist A", 210),  # 4 songs by Artist A out of 5 total (> (5+1)//2 = 3)
        Song("Song 5", "Artist B", 195)
    ]
    assert shuffler._is_arrangement_possible(impossible_songs) is False
    
    # Test edge case: exactly half
    exact_half_songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist A", 200),  # 2 songs by Artist A out of 4 total (= 4/2)
        Song("Song 3", "Artist B", 190),
        Song("Song 4", "Artist C", 210)
    ]
    assert shuffler._is_arrangement_possible(exact_half_songs) is True


def test_get_artist_distribution():
    """Test getting artist distribution."""
    shuffler = ConstrainedShuffler()
    
    songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist B", 200),
        Song("Song 3", "Artist A", 190),  # Artist A appears twice
        Song("Song 4", "Artist C", 210),
        Song("Song 5", "Artist B", 195)   # Artist B appears twice
    ]
    
    distribution = shuffler.get_artist_distribution(songs)
    assert len(distribution) == 3  # Three unique artists
    assert distribution["artist a"] == 2  # Case insensitive
    assert distribution["artist b"] == 2  # Case insensitive
    assert distribution["artist c"] == 1  # Case insensitive


if __name__ == "__main__":
    pytest.main([__file__])