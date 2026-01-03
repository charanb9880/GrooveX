from playlist.playlist import Playlist
from playlist.song import Song
from .playback_engine import PlaybackHistory
from .skipped_tracker import RecentlySkippedTracker
from utils.auto_replay import AutoReplayManager
from favorites.favorite_queue import FavoriteQueue


class PlaybackController:
    def __init__(self):
        self.playlist = Playlist()
        self.history = PlaybackHistory()
        self.skipped_tracker = RecentlySkippedTracker()
        self.favorite_queue = FavoriteQueue()

        # prevents auto replay from looping forever
        self.auto_replayed = False

    def play_song(self, title, artist, duration, genre=None, song_id=None):
        """
        Play a song and add SAME song object to playlist + history.
        """
        song = Song(title, artist, duration, genre=genre, song_id=song_id)

        # add to playlist
        duplicate_result = self.playlist.add_existing_song(song)
        if duplicate_result is not None:
            # Song was a duplicate and rejected
            pass  # Continue with playback anyway

        # update count + history
        song.increment_play_count()
        self.history.record_played_song(song)
        
        # Record listen for favorites (if song is in favorites)
        if song.song_id:
            self.favorite_queue.record_listen(song.song_id, duration)

        return song

    def play_next(self, force_play_skipped=False):
        """
        Plays the next song in the playlist, respecting the skipped tracker unless forced.
        
        Args:
            force_play_skipped (bool): If True, will play songs even if they are in the skipped tracker
            
        Returns:
            Song or None: The played song, or None if no valid song found
        """
        if self.playlist.is_empty():
            return None
            
        next_song = self.playlist.pop_next()
        if not next_song:
            return None

        # Check if the song is recently skipped and we're not forcing play
        if not force_play_skipped and next_song.song_id and self.skipped_tracker.is_recently_skipped(next_song.song_id):
            # Skip this song and try to get the next one
            # For simplicity, we'll just return None here, but in a real implementation
            # you might want to continue looking for non-skipped songs
            return None

        next_song.increment_play_count()
        self.history.record_played_song(next_song)
        
        # Record listen for favorites (if song is in favorites)
        if next_song.song_id:
            self.favorite_queue.record_listen(next_song.song_id, next_song.duration)

        if self.playlist.is_empty():
            self._trigger_auto_replay()

        return next_song

    def skip_song(self, song_id: str) -> None:
        """
        Mark a song as skipped in the recently skipped tracker.
        
        Args:
            song_id (str): The ID of the song to mark as skipped
        """
        self.skipped_tracker.skip_song(song_id)

    def add_to_favorites(self, song_id: str, title: str, artist: str) -> None:
        """
        Add a song to the favorites queue.
        
        Args:
            song_id (str): Unique identifier for the song
            title (str): Song title
            artist (str): Song artist
        """
        self.favorite_queue.add_to_favorites(song_id, title, artist)

    def remove_from_favorites(self, song_id: str) -> None:
        """
        Remove a song from the favorites queue.
        
        Args:
            song_id (str): Unique identifier for the song
        """
        self.favorite_queue.remove_from_favorites(song_id)

    def get_top_favorites(self, n: int):
        """
        Get the top n favorite songs ordered by total listen time.
        
        Args:
            n (int): Number of top songs to return
            
        Returns:
            List of top n songs with their information
        """
        return self.favorite_queue.get_top_n(n)

    def _trigger_auto_replay(self):
        """
        Replay top-3 calming songs ONCE only.
        """
        if self.auto_replayed:
            return   # stop infinite loop forever

        self.auto_replayed = True

        all_songs = self.history.get_all_history()
        top3 = AutoReplayManager.top_k_calm_songs(all_songs, k=3)

        for s in top3:
            # Check if song is recently skipped before adding back to playlist
            if s.song_id and not self.skipped_tracker.is_recently_skipped(s.song_id):
                self.playlist.add_existing_song(s)

    def get_playlist_songs(self):
        return self.playlist.get_all_songs()

    def undo_last_play(self, playlist=None):
        """
        Undo the last played song by moving it back to the playlist.
        
        Args:
            playlist: Optional playlist to add the song to (defaults to controller's playlist)
            
        Returns:
            bool: True if successful, False if no song to undo
        """
        target_playlist = playlist if playlist is not None else self.playlist
        return self.history.undo_last_play(target_playlist)