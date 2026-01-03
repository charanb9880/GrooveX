import unittest
from playlist.song import Song
from playlist.playlist import Playlist
from playback_history.stack import Stack
from playback_history.playback_engine import PlaybackHistory
from playback_history.playback_controller import PlaybackController

class TestStack(unittest.TestCase):
    def setUp(self):
        """
        Create a fresh Stack before each test.
        """
        self.stack = Stack()

    def test_push_and_pop(self):
        """
        Test pushing and popping songs maintains correct order (LIFO).
        """
        song1 = Song("Song 1", "Artist 1", 200)
        song2 = Song("Song 2", "Artist 2", 180)
        self.stack.push(song1)
        self.stack.push(song2)

        self.assertEqual(self.stack.size, 2)
        top_song = self.stack.pop()
        self.assertEqual(top_song.title, "Song 2")
        self.assertEqual(self.stack.size, 1)
        next_song = self.stack.pop()
        self.assertEqual(next_song.title, "Song 1")
        self.assertTrue(self.stack.is_empty())

    def test_pop_empty_stack_returns_none(self):
        """
        Popping from empty stack returns None without error.
        """
        self.assertIsNone(self.stack.pop())

    def test_peek(self):
        """
        Peek returns the top song without removing it.
        """
        song = Song("Song Peek", "Artist Peek", 150)
        self.stack.push(song)
        self.assertEqual(self.stack.peek().title, "Song Peek")
        self.assertEqual(self.stack.size, 1)
        self.stack.pop()
        self.assertIsNone(self.stack.peek())

class TestPlaybackHistory(unittest.TestCase):
    def setUp(self):
        """
        Setup a new PlaybackHistory and a test Playlist before each test.
        """
        self.history = PlaybackHistory()
        self.playlist = Playlist()

    def test_record_and_undo_last_play(self):
        """
        Records songs and undoes last played by re-adding to playlist.
        """
        song = Song("Undo Song", "Undo Artist", 220)
        self.history.record_played_song(song)
        success = self.history.undo_last_play(self.playlist)
        self.assertTrue(success)

        songs = self.playlist.get_all_songs()
        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0].title, "Undo Song")

    def test_undo_last_play_empty_history(self):
        """
        Undoing with empty history stack returns False and does not fail.
        """
        self.assertFalse(self.history.undo_last_play(self.playlist))

class TestPlaybackController(unittest.TestCase):
    def setUp(self):
        self.controller = PlaybackController()

    def test_play_song_adds_to_playlist_and_history(self):
        """
        Play song adds song to playlist and playback history.
        """
        title, artist, duration = "Test Song", "Test Artist", 300
        self.controller.play_song(title, artist, duration)

        songs = self.controller.get_playlist_songs()
        self.assertEqual(len(songs), 1)
        self.assertEqual(songs[0].title, title)

    def test_undo_last_play_readds_song(self):
        """
        Undo last play should move last played song back to playlist.
        """
        self.controller.play_song("Song A", "Artist A", 180)
        self.controller.play_song("Song B", "Artist B", 200)

        # Undo last played (Song B)
        success = self.controller.undo_last_play()
        self.assertTrue(success)

        # Playlist now should have 3 songs: the two originals + the undo song
        songs = self.controller.get_playlist_songs()
        self.assertEqual(len(songs), 3)
        self.assertEqual(songs[-1].title, "Song B")

    def test_undo_last_play_empty_history(self):
        """
        Undo on empty history returns False without error.
        """
        controller = PlaybackController()
        self.assertFalse(controller.undo_last_play())

if __name__ == "__main__":
    unittest.main()
