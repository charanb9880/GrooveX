import unittest
from playlist.playlist import Playlist
from playlist.song import Song
from playback_history.playback_controller import PlaybackController
from song_rating_tree.song_rating_engine import SongRatingEngine
from song_lookup_map.lookup_map import SongLookupMap
from system_dashboard.dashboard import SystemDashboard


class TestSystemDashboard(unittest.TestCase):
    """
    Unit tests for SystemDashboard class.
    Tests integration of all PlayWise modules through the dashboard.
    """
    
    def setUp(self):
        """
        Set up test fixtures with sample data.
        Creates playlist, playback controller, rating engine, and lookup map.
        """
        # Initialize all components
        self.playlist = Playlist()
        self.playback_controller = PlaybackController()
        self.rating_engine = SongRatingEngine()
        self.lookup_map = SongLookupMap()
        
        # Add sample songs with (title, artist, duration, rating)
        songs_data = [
            ("Imagine", "John Lennon", 183, 5),
            ("Bohemian Rhapsody", "Queen", 354, 5),
            ("Hey Jude", "The Beatles", 431, 4),
            ("Yesterday", "The Beatles", 125, 4),
            ("Stairway to Heaven", "Led Zeppelin", 482, 5)
        ]
        
        # Track song_id counter for proper ID assignment
        song_id_counter = 1
        
        for title, artist, duration, rating in songs_data:
            # Add to playlist
            self.playlist.add_song(title, artist, duration)
            
            # Create song with proper song_id
            song = Song(title, artist, duration, song_id=song_id_counter)
            song_id_counter += 1
            
            # Add to rating engine
            self.rating_engine.insert_song(song, rating)
            
            # Add to lookup map
            self.lookup_map.add_song(song)
            
            # Record in playback history
            self.playback_controller.play_song(title, artist, duration)
        
        # Initialize dashboard with all components
        self.dashboard = SystemDashboard(
            self.playlist,
            self.playback_controller,
            self.rating_engine,
            self.lookup_map
        )
    
    def test_dashboard_initialization(self):
        """
        Test that dashboard initializes correctly with all components.
        """
        self.assertIsNotNone(self.dashboard)
        self.assertIsNotNone(self.dashboard.playlist)
        self.assertIsNotNone(self.dashboard.playback_controller)
        self.assertIsNotNone(self.dashboard.rating_engine)
        self.assertIsNotNone(self.dashboard.lookup_map)
    
    def test_get_top_longest_songs(self):
        """
        Test retrieval of top longest songs sorted by duration.
        """
        top_songs = self.dashboard.get_top_longest_songs(3)
        
        # Should return 3 songs
        self.assertEqual(len(top_songs), 3)
        
        # Verify they're sorted by duration descending
        self.assertGreaterEqual(top_songs[0].duration, top_songs[1].duration)
        self.assertGreaterEqual(top_songs[1].duration, top_songs[2].duration)
        
        # First should be "Stairway to Heaven" (482s)
        self.assertEqual(top_songs[0].title, "Stairway to Heaven")
        self.assertEqual(top_songs[0].duration, 482)
    
    def test_get_recently_played_songs(self):
        """
        Test retrieval of recently played songs from stack.
        """
        recent = self.dashboard.get_recently_played_songs(3)
        
        # Should return 3 songs
        self.assertEqual(len(recent), 3)
        
        # Most recent should be "Stairway to Heaven" (last played)
        self.assertEqual(recent[0].title, "Stairway to Heaven")
        
        # Second most recent should be "Yesterday"
        self.assertEqual(recent[1].title, "Yesterday")
    
    def test_get_song_count_by_rating(self):
        """
        Test song count aggregation by rating using BST traversal.
        """
        counts = self.dashboard.get_song_count_by_rating()
        
        # Verify rating counts
        self.assertEqual(counts[5], 3)  # 3 songs with rating 5
        self.assertEqual(counts[4], 2)  # 2 songs with rating 4
        
        # Verify all ratings are present
        self.assertIn(5, counts)
        self.assertIn(4, counts)
    
    def test_get_total_playlist_duration(self):
        """
        Test calculation of total playlist duration.
        """
        total_duration = self.dashboard.get_total_playlist_duration()
        
        # Sum of all durations: 183 + 354 + 431 + 125 + 482 = 1575
        expected_duration = 183 + 354 + 431 + 125 + 482
        self.assertEqual(total_duration, expected_duration)
    
    def test_get_playlist_statistics(self):
        """
        Test comprehensive playlist statistics.
        """
        stats = self.dashboard.get_playlist_statistics()
        
        # Verify stats structure
        self.assertIn('total_songs', stats)
        self.assertIn('total_duration', stats)
        self.assertIn('avg_duration', stats)
        self.assertIn('shortest_song', stats)
        self.assertIn('longest_song', stats)
        
        # Verify values
        self.assertEqual(stats['total_songs'], 5)
        self.assertEqual(stats['shortest_song'].title, "Yesterday")
        self.assertEqual(stats['shortest_song'].duration, 125)
        self.assertEqual(stats['longest_song'].title, "Stairway to Heaven")
        self.assertEqual(stats['longest_song'].duration, 482)
    
    def test_export_snapshot(self):
        """
        Test complete snapshot export with all dashboard sections.
        """
        snapshot = self.dashboard.export_snapshot()
        
        # Verify all required sections exist
        self.assertIn('timestamp', snapshot)
        self.assertIn('system_overview', snapshot)
        self.assertIn('top_5_longest_songs', snapshot)
        self.assertIn('recently_played_songs', snapshot)
        self.assertIn('song_count_by_rating', snapshot)
        self.assertIn('extremes', snapshot)
        
        # Verify system overview
        overview = snapshot['system_overview']
        self.assertEqual(overview['total_songs_in_playlist'], 5)
        self.assertGreater(overview['total_duration_seconds'], 0)
        
        # Verify top songs
        self.assertEqual(len(snapshot['top_5_longest_songs']), 5)
        
        # Verify rating distribution
        self.assertEqual(snapshot['song_count_by_rating'][5], 3)
        self.assertEqual(snapshot['song_count_by_rating'][4], 2)
        
        # Verify extremes
        self.assertEqual(snapshot['extremes']['shortest_song']['title'], "Yesterday")
        self.assertEqual(snapshot['extremes']['longest_song']['title'], "Stairway to Heaven")
    
    def test_empty_dashboard(self):
        """
        Test dashboard behavior with empty data structures.
        """
        # Create empty dashboard
        empty_playlist = Playlist()
        empty_controller = PlaybackController()
        empty_rating = SongRatingEngine()
        empty_lookup = SongLookupMap()
        
        empty_dashboard = SystemDashboard(
            empty_playlist,
            empty_controller,
            empty_rating,
            empty_lookup
        )
        
        # Test empty state
        self.assertEqual(len(empty_dashboard.get_top_longest_songs(5)), 0)
        self.assertEqual(len(empty_dashboard.get_recently_played_songs(5)), 0)
        self.assertEqual(len(empty_dashboard.get_song_count_by_rating()), 0)
        
        # Test snapshot with empty data
        snapshot = empty_dashboard.export_snapshot()
        self.assertEqual(snapshot['system_overview']['total_songs_in_playlist'], 0)


if __name__ == '__main__':
    unittest.main()
