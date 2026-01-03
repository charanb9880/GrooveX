import unittest
import time
from playlist.song import Song
from playlist_sorting.sort_engine import SortEngine, SortCriteria

class TestSortEngine(unittest.TestCase):
    """
    Unit tests for the SortEngine class covering sorting songs
    by multiple criteria using the custom merge sort implementation.
    """

    def setUp(self):
        """
        Setup called before each test, initializes SortEngine and sample songs.
        """
        self.sort_engine = SortEngine()

        # Current timestamp for added_time (simulate recentness)
        now = int(time.time())

        # Create sample Song objects with varying attributes:
        self.song1 = Song("Imagine", "John Lennon", 183, song_id=1)
        self.song1.added_time = now - 100  # Added 100 seconds ago

        self.song2 = Song("Bohemian Rhapsody", "Queen", 354, song_id=2)
        self.song2.added_time = now - 200  # Added 200 seconds ago

        self.song3 = Song("Hey Jude", "The Beatles", 431, song_id=3)
        self.song3.added_time = now - 50   # Added 50 seconds ago (most recent)

        self.song4 = Song("All You Need Is Love", "The Beatles", 180, song_id=4)
        self.song4.added_time = now - 150  # Added 150 seconds ago

    def test_merge_sort_alpha_title(self):
        """
        Test merge sort sorts songs alphabetically by title (case insensitive).
        """
        songs = [self.song1, self.song2, self.song3, self.song4]
        sorted_songs = self.sort_engine.merge_sort(songs, SortCriteria.ALPHA_TITLE)
        titles = [s.title for s in sorted_songs]
        expected = ["All You Need Is Love", "Bohemian Rhapsody", "Hey Jude", "Imagine"]
        self.assertEqual(titles, expected)

    def test_merge_sort_duration_asc(self):
        """
        Test merge sort sorts songs by ascending duration (shortest first).
        """
        songs = [self.song1, self.song2, self.song3, self.song4]
        sorted_songs = self.sort_engine.merge_sort(songs, SortCriteria.DURATION_ASC)
        durations = [s.duration for s in sorted_songs]
        expected = sorted([s.duration for s in songs])
        self.assertEqual(durations, expected)

    def test_merge_sort_duration_desc(self):
        """
        Test merge sort sorts songs by descending duration (longest first).
        """
        songs = [self.song1, self.song2, self.song3, self.song4]
        sorted_songs = self.sort_engine.merge_sort(songs, SortCriteria.DURATION_DESC)
        durations = [s.duration for s in sorted_songs]
        expected = sorted([s.duration for s in songs], reverse=True)
        self.assertEqual(durations, expected)

    def test_merge_sort_recent(self):
        """
        Test merge sort sorts songs by recent addition (most recent first).
        """
        songs = [self.song1, self.song2, self.song3, self.song4]
        sorted_songs = self.sort_engine.merge_sort(songs, SortCriteria.RECENT)
        added_times = [s.added_time for s in sorted_songs]
        # Times should be sorted descending (most recent = highest timestamp first)
        self.assertEqual(added_times, sorted(added_times, reverse=True))

    def test_stability(self):
        """
        Test that merge sort is stable - maintains relative order of equal keys.
        Example: two songs with same duration should remain in input order.
        """
        song_a = Song("Song A", "Artist", 300, song_id=10)
        song_b = Song("Song B", "Artist", 300, song_id=11)
        songs = [song_b, song_a]  # song_b first, song_a second but same duration
        sorted_songs = self.sort_engine.merge_sort(songs, SortCriteria.DURATION_ASC)
        # Sorted by duration ascending, so order should be unchanged since durations equal
        self.assertEqual(sorted_songs, songs)

    def test_empty_list(self):
        """
        Test sorting an empty list returns an empty list.
        """
        sorted_songs = self.sort_engine.merge_sort([], SortCriteria.ALPHA_TITLE)
        self.assertEqual(sorted_songs, [])

    def test_single_element_list(self):
        """
        Test sorting a list of one song returns the same list.
        """
        sorted_songs = self.sort_engine.merge_sort([self.song1], SortCriteria.ALPHA_TITLE)
        self.assertEqual(sorted_songs, [self.song1])

if __name__ == "__main__":
    unittest.main()
