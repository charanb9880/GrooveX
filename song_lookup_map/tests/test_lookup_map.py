import unittest
from playlist.song import Song
from song_lookup_map.lookup_map import SongLookupMap

class TestSongLookupMap(unittest.TestCase):
    """
    Unit test suite for the SongLookupMap hash map implementation.
    Covers addition, removal, and constant-time lookup by ID and title.
    """

    def setUp(self):
        """
        Prepare a fresh SongLookupMap and example songs for every test.
        Ensures no state carry-over between tests.
        """
        self.lookup = SongLookupMap()
        self.song1 = Song("Imagine", "John Lennon", 183, song_id=1)
        self.song2 = Song("Bohemian Rhapsody", "Queen", 354, song_id=2)
        self.song3 = Song("Hey Jude", "The Beatles", 431, song_id=3)

    def test_add_and_lookup_by_id(self):
        """
        Adding a song should allow O(1) lookup by its unique song_id.
        """
        self.lookup.add_song(self.song1)
        self.lookup.add_song(self.song2)

        # Look up each song by song_id and check attributes
        result1 = self.lookup.lookup_song_by_id(1)
        self.assertEqual(result1, self.song1)
        result2 = self.lookup.lookup_song_by_id(2)
        self.assertEqual(result2, self.song2)

    def test_add_and_lookup_by_title(self):
        """
        Adding a song should allow O(1) lookup by its unique title.
        """
        self.lookup.add_song(self.song1)
        result = self.lookup.lookup_song_by_title("Imagine")
        self.assertEqual(result, self.song1)

    def test_lookup_missing_id_returns_none(self):
        """
        Looking up a non-existent song_id should return None, not error.
        """
        result = self.lookup.lookup_song_by_id(999)
        self.assertIsNone(result)

    def test_lookup_missing_title_returns_none(self):
        """
        Looking up a non-existent song title should return None, not error.
        """
        result = self.lookup.lookup_song_by_title("Non Existent Title")
        self.assertIsNone(result)

    def test_remove_song_successful(self):
        """
        After removing a song, lookups by both id and title should fail.
        """
        self.lookup.add_song(self.song1)
        success = self.lookup.remove_song(self.song1.song_id)
        self.assertTrue(success)
        self.assertIsNone(self.lookup.lookup_song_by_id(self.song1.song_id))
        self.assertIsNone(self.lookup.lookup_song_by_title(self.song1.title))

    def test_remove_song_not_found(self):
        """
        Removing a song that's not present should not raise errors, returns False.
        """
        success = self.lookup.remove_song(999)
        self.assertFalse(success)

    def test_add_duplicate_song_id_overwrites(self):
        """
        Adding a new song with the same ID updates the mapping to the new song.
        """
        self.lookup.add_song(self.song1)
        # Create a different song with the same id
        song1_dup = Song("Imagine Remastered", "John Lennon", 200, song_id=1)
        self.lookup.add_song(song1_dup)
        # The result should now point to the new song
        result = self.lookup.lookup_song_by_id(1)
        self.assertEqual(result, song1_dup)
        self.assertNotEqual(result, self.song1)

    def test_add_duplicate_title_overwrites(self):
        """
        Adding a song with the same title updates the mapping in title_map.
        """
        self.lookup.add_song(self.song2)
        song2_alt = Song("Bohemian Rhapsody", "Queen Live", 400, song_id=22)
        self.lookup.add_song(song2_alt)
        result = self.lookup.lookup_song_by_title("Bohemian Rhapsody")
        self.assertEqual(result, song2_alt)

if __name__ == "__main__":
    unittest.main()
