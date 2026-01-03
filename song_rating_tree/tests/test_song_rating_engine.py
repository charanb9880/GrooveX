import unittest
from playlist.song import Song
from song_rating_tree.song_rating_engine import SongRatingEngine

class TestSongRatingEngine(unittest.TestCase):
    """
    Unit tests for the SongRatingEngine managing a BST of rating buckets.
    """

    def setUp(self):
        """
        Initializes a fresh SongRatingEngine before each test to ensure isolation.
        """
        self.engine = SongRatingEngine()

        # Example songs used in multiple tests
        self.song1 = Song("Imagine", "John Lennon", 183, song_id=1)
        self.song2 = Song("Bohemian Rhapsody", "Queen", 354, song_id=2)
        self.song3 = Song("Hey Jude", "The Beatles", 431, song_id=3)
        self.song4 = Song("Shape of You", "Ed Sheeran", 240, song_id=4)

    def test_insert_and_search_single_rating(self):
        """
        Test inserting multiple songs of the same rating and searching returns all.
        """
        self.engine.insert_song(self.song1, rating=5)
        self.engine.insert_song(self.song3, rating=5)

        songs = self.engine.search_by_rating(5)
        self.assertEqual(len(songs), 2)
        self.assertIn(self.song1, songs)
        self.assertIn(self.song3, songs)

    def test_search_by_rating_no_songs(self):
        """
        Searching a rating with no songs returns an empty list.
        """
        songs = self.engine.search_by_rating(1)  # No songs inserted
        self.assertEqual(songs, [])

    def test_insert_and_search_multiple_ratings(self):
        """
        Insert songs with different ratings and verify search returns correct buckets.
        """
        self.engine.insert_song(self.song1, rating=5)
        self.engine.insert_song(self.song2, rating=4)
        self.engine.insert_song(self.song4, rating=3)

        songs_5 = self.engine.search_by_rating(5)
        songs_4 = self.engine.search_by_rating(4)
        songs_3 = self.engine.search_by_rating(3)

        self.assertEqual(len(songs_5), 1)
        self.assertEqual(songs_5[0], self.song1)

        self.assertEqual(len(songs_4), 1)
        self.assertEqual(songs_4[0], self.song2)

        self.assertEqual(len(songs_3), 1)
        self.assertEqual(songs_3[0], self.song4)

    def test_delete_song_removes_from_correct_bucket(self):
        """
        Deleting a song should remove it from its rating bucket.
        """
        self.engine.insert_song(self.song1, rating=5)
        self.engine.insert_song(self.song3, rating=5)
        self.engine.insert_song(self.song2, rating=4)

        # Delete song3 by ID ("Hey Jude")
        self.engine.delete_song(3)

        songs_5 = self.engine.search_by_rating(5)
        self.assertNotIn(self.song3, songs_5)
        self.assertIn(self.song1, songs_5)

        songs_4 = self.engine.search_by_rating(4)
        self.assertIn(self.song2, songs_4)

    def test_delete_nonexistent_song_does_not_break(self):
        """
        Deleting a song_id not present in the tree should not cause errors.
        """
        self.engine.insert_song(self.song1, rating=5)
        try:
            self.engine.delete_song(999)  # Non-existent song_id
        except Exception as e:
            self.fail(f"delete_song raised Exception unexpectedly: {e}")

    def test_insert_songs_with_duplicate_ids(self):
        """
        Insert songs with duplicate song_ids in different buckets and verify storage.
        """
        duplicate_song = Song("Fake Title", "Fake Artist", 123, song_id=1)
        self.engine.insert_song(self.song1, rating=5)
        self.engine.insert_song(duplicate_song, rating=3)  # Same song_id as song1

        bucket_5 = self.engine.search_by_rating(5)
        bucket_3 = self.engine.search_by_rating(3)

        self.assertIn(self.song1, bucket_5)
        self.assertIn(duplicate_song, bucket_3)

    def test_insert_invalid_rating_ignored_or_handled(self):
        """
        Optionally test behavior if invalid rating (<1 or >5) is inserted.
        Modify based on your implementation.
        """
        with self.assertRaises(ValueError):
            self.engine.insert_song(self.song1, rating=6)  # Invalid rating > 5

        with self.assertRaises(ValueError):
            self.engine.insert_song(self.song2, rating=0)  # Invalid rating < 1

if __name__ == "__main__":
    unittest.main()
