import unittest
from playlist.playlist import Playlist
from playlist.song import Song

class TestPlaylistEngine(unittest.TestCase):
    def setUp(self):
        """
        Setup runs before each test method.
        Initializes a fresh Playlist instance for isolation.
        """
        self.playlist = Playlist()

    def test_add_song_should_increase_size_and_store_song(self):
        """
        Verify add_song appends songs.
        Check if playlist size increments and correct song is stored.
        """
        self.playlist.add_song("Song A", "Artist A", 200)
        songs = self.playlist.get_all_songs()
        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0].title, "Song A")
        self.assertEqual(songs[0].artist, "Artist A")
        self.assertEqual(songs[0].duration, 200)

    def test_delete_song_should_remove_song_at_index(self):
        """
        After deletion, verify song count decreases and correct song is removed.
        Also tests removal of head and tail nodes.
        """
        self.playlist.add_song("Song A", "Artist A", 200)
        self.playlist.add_song("Song B", "Artist B", 180)
        self.playlist.delete_song(0)  # Delete first song
        songs = self.playlist.get_all_songs()
        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0].title, "Song B")

    def test_delete_song_invalid_index_should_raise(self):
        """
        Attempt to delete song at invalid index must raise IndexError.
        Tests playlist bounds validation.
        """
        with self.assertRaises(IndexError):
            self.playlist.delete_song(0)  # Empty playlist

    def test_move_song_should_relocate_song(self):
        """
        Moving a song from one index to another should reorder playlist correctly.
        Validates internal linked list node rearrangement.
        """
        self.playlist.add_song("Song A", "Artist A", 200)
        self.playlist.add_song("Song B", "Artist B", 180)
        self.playlist.add_song("Song C", "Artist C", 220)
        self.playlist.move_song(0, 2)  # Move first song to end

        songs = self.playlist.get_all_songs()
        self.assertEqual([s.title for s in songs], ["Song B", "Song C", "Song A"])

    def test_move_song_invalid_index_should_raise(self):
        """
        Moving with invalid indices should raise IndexError.
        Ensures input validation on move_song method.
        """
        self.playlist.add_song("Song A", "Artist A", 200)
        with self.assertRaises(IndexError):
            self.playlist.move_song(1, 0)  # from_index out of range

    def test_reverse_playlist_should_reverse_order(self):
        """
        Reverse the playlist and ensure all songs are in reverse order.
        Tests correctness of reversing doubly linked list pointers.
        """
        self.playlist.add_song("Song A", "Artist A", 200)
        self.playlist.add_song("Song B", "Artist B", 180)
        self.playlist.add_song("Song C", "Artist C", 220)
        self.playlist.reverse_playlist()

        songs = self.playlist.get_all_songs()
        self.assertEqual([s.title for s in songs], ["Song C", "Song B", "Song A"])

    def test_reverse_empty_playlist_should_not_fail(self):
        """
        Reversing an empty playlist must not raise exceptions.
        Validates resilience against edge cases.
        """
        try:
            self.playlist.reverse_playlist()
        except Exception as e:
            self.fail(f"reverse_playlist() raised Exception unexpectedly: {e}")

if __name__ == '__main__':
    unittest.main()
