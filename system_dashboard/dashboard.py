from typing import Dict, List, Any
from playlist.song import Song
from playlist.playlist import Playlist
from playback_history.playback_controller import PlaybackController
from song_rating_tree.song_rating_engine import SongRatingEngine
from song_lookup_map.lookup_map import SongLookupMap
from playlist_sorting.sort_engine import SortEngine, SortCriteria

class SystemDashboard:
    """
    Live dashboard for PlayWise system statistics and debugging.
    Integrates multiple data structures to provide real-time insights.
    """
    
    def __init__(self, playlist: Playlist, playback_controller: PlaybackController,
                 rating_engine: SongRatingEngine, lookup_map: SongLookupMap):
        """
        Initialize dashboard with references to all core system components.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        self.playlist = playlist
        self.playback_controller = playback_controller
        self.rating_engine = rating_engine
        self.lookup_map = lookup_map
        self.sort_engine = SortEngine()
    
    def get_top_longest_songs(self, top_n: int = 5) -> List[Song]:
        """
        Get top N longest songs from playlist using sorting.
        
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        all_songs = self.playlist.get_all_songs()
        if not all_songs:
            return []
        
        sorted_songs = self.sort_engine.merge_sort(all_songs, SortCriteria.DURATION_DESC)
        return sorted_songs[:min(top_n, len(sorted_songs))]
    
    def get_recently_played_songs(self, count: int = 5) -> List[Song]:
        """
        Get most recently played songs from playback history.
        Works with linked list stack implementation.
    
        Time Complexity: O(n)
        Space Complexity: O(n)
    
        :param count: Number of recent songs to return
        :return: List of recently played songs (most recent first)
        """
        result = []
        current = None

        # Access the Stack instance
        if hasattr(self.playback_controller, 'history'):
            stack_obj = self.playback_controller.history.history_stack
        elif hasattr(self.playback_controller, 'history_stack'):
            stack_obj = self.playback_controller.history_stack
        elif hasattr(self.playback_controller, 'playback_history'):
            stack_obj = self.playback_controller.playback_history.history_stack
        else:
            return []

        # The stack instance is linked list based
        # Start from top node
        current = stack_obj.top if hasattr(stack_obj, 'top') else None

        # Traverse up to 'count' nodes
        while current and len(result) < count:
            result.append(current.song)
            current = current.next

        return result  # Already from newest to oldest

    
    def get_song_count_by_rating(self) -> Dict[int, int]:
        """
        Get count of songs for each rating using BST traversal.
        
        Time Complexity: O(n)
        Space Complexity: O(k) where k = number of unique ratings
        """
        rating_counts = {}
        
        def traverse_and_count(node):
            """Recursive in-order traversal to count songs per rating."""
            if node is None:
                return
            
            traverse_and_count(node.left)
            
            # Count songs in this rating bucket
            song_count = len(node.bucket.songs)
            rating_counts[node.rating] = song_count
            
            traverse_and_count(node.right)
        
        traverse_and_count(self.rating_engine.bst.root)
        return rating_counts
    
    def get_total_playlist_duration(self) -> int:
        """
        Calculate total duration of all songs.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        all_songs = self.playlist.get_all_songs()
        return sum(song.duration for song in all_songs)
    
    def get_playlist_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive playlist statistics.
        
        Time Complexity: O(n)
        Space Complexity: O(1)
        """
        all_songs = self.playlist.get_all_songs()
        
        if not all_songs:
            return {
                'total_songs': 0,
                'total_duration': 0,
                'avg_duration': 0,
                'shortest_song': None,
                'longest_song': None
            }
        
        durations = [song.duration for song in all_songs]
        
        return {
            'total_songs': len(all_songs),
            'total_duration': sum(durations),
            'avg_duration': sum(durations) // len(durations),
            'shortest_song': min(all_songs, key=lambda s: s.duration),
            'longest_song': max(all_songs, key=lambda s: s.duration)
        }
    
    def get_play_duration_visualization(self) -> Dict[str, Any]:
        """
        Get play duration visualization data including total playtime, longest song, and shortest song.
        
        This implements the Play Duration Visualizer feature using aggregation logic and min/max tracking.
        
        Time Complexity: O(n) where n is the number of songs
        Space Complexity: O(1)
        
        Returns:
            Dict[str, Any]: Visualization data including total, min, and max durations
        """
        all_songs = self.playlist.get_all_songs()
        
        if not all_songs:
            return {
                'total_playtime': 0,
                'longest_song': None,
                'shortest_song': None,
                'song_count': 0
            }
        
        # Use aggregation logic to calculate total playtime
        total_playtime = sum(song.duration for song in all_songs)
        
        # Use min/max tracking to find shortest and longest songs
        shortest_song = min(all_songs, key=lambda s: s.duration)
        longest_song = max(all_songs, key=lambda s: s.duration)
        
        return {
            'total_playtime': total_playtime,
            'longest_song': {
                'title': longest_song.title,
                'artist': longest_song.artist,
                'duration': longest_song.duration
            },
            'shortest_song': {
                'title': shortest_song.title,
                'artist': shortest_song.artist,
                'duration': shortest_song.duration
            },
            'song_count': len(all_songs)
        }
    
    def print_play_duration_visualization(self) -> None:
        """
        Print formatted play duration visualization to console.
        
        Time Complexity: O(n) where n is the number of songs
        Space Complexity: O(1)
        """
        viz_data = self.get_play_duration_visualization()
        
        print("\n" + "="*50)
        print("           PLAY DURATION VISUALIZATION")
        print("="*50)
        
        if viz_data['song_count'] == 0:
            print("No songs in playlist")
            print("="*50 + "\n")
            return
        
        # Display total playtime
        total_seconds = viz_data['total_playtime']
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        print(f"Total Playtime: {hours}h {minutes}m {seconds}s ({total_seconds} seconds)")
        
        # Display song count
        print(f"Total Songs: {viz_data['song_count']}")
        
        # Display longest song
        longest = viz_data['longest_song']
        print(f"\nLongest Song:")
        print(f"  • {longest['title']} by {longest['artist']} ({longest['duration']} seconds)")
        
        # Display shortest song
        shortest = viz_data['shortest_song']
        print(f"\nShortest Song:")
        print(f"  • {shortest['title']} by {shortest['artist']} ({shortest['duration']} seconds)")
        
        print("="*50 + "\n")
    
    def export_snapshot(self) -> Dict[str, Any]:
        """
        Export complete system snapshot for debugging and monitoring.
        
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        """
        top_longest = self.get_top_longest_songs(5)
        recently_played = self.get_recently_played_songs(5)
        rating_distribution = self.get_song_count_by_rating()
        stats = self.get_playlist_statistics()
        
        # Get history count safely
        try:
            history_count = len(self.playback_controller.history_stack.items)
        except:
            history_count = 0
        
        snapshot = {
            'timestamp': self._get_current_timestamp(),
            'system_overview': {
                'total_songs_in_playlist': stats['total_songs'],
                'total_duration_seconds': stats['total_duration'],
                'average_song_duration': stats['avg_duration'],
                'total_playback_history': history_count
            },
            'top_5_longest_songs': [
                {
                    'song_id': song.song_id,
                    'title': song.title,
                    'artist': song.artist,
                    'duration': song.duration
                }
                for song in top_longest
            ],
            'recently_played_songs': [
                {
                    'song_id': song.song_id,
                    'title': song.title,
                    'artist': song.artist,
                    'duration': song.duration
                }
                for song in recently_played
            ],
            'song_count_by_rating': rating_distribution,
            'extremes': {
                'shortest_song': {
                    'title': stats['shortest_song'].title if stats['shortest_song'] else None,
                    'duration': stats['shortest_song'].duration if stats['shortest_song'] else None
                },
                'longest_song': {
                    'title': stats['longest_song'].title if stats['longest_song'] else None,
                    'duration': stats['longest_song'].duration if stats['longest_song'] else None
                }
            }
        }
        
        return snapshot
    
    def _get_current_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def print_dashboard(self):
        """Print formatted dashboard to console."""
        snapshot = self.export_snapshot()
        
        print("\n" + "="*60)
        print("           PLAYWISE SYSTEM DASHBOARD")
        print("="*60)
        print(f"Snapshot Time: {snapshot['timestamp']}")
        print("-"*60)
        
        # System Overview
        print("\n📊 SYSTEM OVERVIEW")
        overview = snapshot['system_overview']
        print(f"  • Total Songs in Playlist: {overview['total_songs_in_playlist']}")
        print(f"  • Total Duration: {overview['total_duration_seconds']} seconds")
        print(f"  • Average Song Duration: {overview['average_song_duration']} seconds")
        print(f"  • Playback History Count: {overview['total_playback_history']}")
        
        # Top 5 Longest Songs
        print("\n🎵 TOP 5 LONGEST SONGS")
        if snapshot['top_5_longest_songs']:
            for idx, song in enumerate(snapshot['top_5_longest_songs'], 1):
                print(f"  {idx}. {song['title']} by {song['artist']} - {song['duration']}s")
        else:
            print("  No songs in playlist")
        
        # Recently Played
        print("\n⏮️  RECENTLY PLAYED (Most Recent First)")
        if snapshot['recently_played_songs']:
            for idx, song in enumerate(snapshot['recently_played_songs'], 1):
                print(f"  {idx}. {song['title']} by {song['artist']}")
        else:
            print("  No playback history")
        
        # Rating Distribution
        print("\n⭐ SONG COUNT BY RATING")
        if snapshot['song_count_by_rating']:
            for rating in sorted(snapshot['song_count_by_rating'].keys(), reverse=True):
                count = snapshot['song_count_by_rating'][rating]
                stars = "★" * rating
                print(f"  {stars} ({rating}): {count} songs")
        else:
            print("  No rated songs")
        
        # Extremes
        print("\n🔝 EXTREMES")
        extremes = snapshot['extremes']
        if extremes['shortest_song']['title']:
            print(f"  • Shortest: {extremes['shortest_song']['title']} ({extremes['shortest_song']['duration']}s)")
        if extremes['longest_song']['title']:
            print(f"  • Longest: {extremes['longest_song']['title']} ({extremes['longest_song']['duration']}s)")
        
        print("\n" + "="*60 + "\n")
