#!/usr/bin/env python3
"""
Standalone demo for the Smart Recommender feature.
"""

import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from explorer.playlist_explorer import PlaylistExplorer
from playback_history.skipped_tracker import RecentlySkippedTracker
from recommend.recommender import SmartRecommender


class SimplePlaylist:
    """Simple playlist implementation for demo."""
    
    def __init__(self):
        self.songs = []
    
    def get_all_songs(self):
        """Get all songs in the playlist."""
        class MockSong:
            def __init__(self, song_id):
                self.song_id = song_id
        
        return [MockSong(song_id) for song_id in self.songs]


def demo_smart_recommender():
    """Demonstrate the Smart Recommender feature."""
    print("=== PlayWise Music Engine - Smart Recommender Demo ===\n")
    
    # Create real instances
    playlist_explorer = PlaylistExplorer()
    skipped_tracker = RecentlySkippedTracker()
    simple_playlist = SimplePlaylist()
    
    # Create recommender
    recommender = SmartRecommender(
        playlist_explorer=playlist_explorer,
        skipped_tracker=skipped_tracker,
        playlist_songs_getter=simple_playlist.get_all_songs,
        window_size=10,
        seed_count=3,
        top_n=5,
        duration_threshold=60,  # 1 minute threshold
        bpm_threshold=20        # 20 BPM threshold
    )
    
    # First, populate the playlist explorer with hierarchical data
    print("Setting up music catalog with hierarchical classification:")
    
    # Rock songs
    playlist_explorer.add_song("radiohead_creep", "Rock", "Alternative", "Melancholic", "Radiohead")
    playlist_explorer.add_song("coldplay_yellow", "Rock", "Alternative", "Melancholic", "Coldplay")
    playlist_explorer.add_song("arctic_monkeys_dancing", "Rock", "Alternative", "Upbeat", "Arctic Monkeys")
    playlist_explorer.add_song("queen_bohemian", "Rock", "Classic", "Epic", "Queen")
    playlist_explorer.add_song("led_zeppelin_stairway", "Rock", "Classic", "Epic", "Led Zeppelin")
    
    # Pop songs
    playlist_explorer.add_song("dua_lipa_physical", "Pop", "Dance", "Energetic", "Dua Lipa")
    playlist_explorer.add_song("bruno_mars_grenade", "Pop", "Ballad", "Emotional", "Bruno Mars")
    playlist_explorer.add_song("ariana_grande_thank_u", "Pop", "Dance", "Upbeat", "Ariana Grande")
    
    # Jazz songs
    playlist_explorer.add_song("norah_jones_come_away", "Jazz", "Smooth", "Relaxing", "Norah Jones")
    playlist_explorer.add_song("miles_davis_kind_of_blue", "Jazz", "Bebop", "Complex", "Miles Davis")
    
    print("  - Added 9 songs to catalog with full hierarchical metadata")
    print()
    
    # Add rich metadata for recommendation engine
    song_metadata = {
        "radiohead_creep": {
            "genre": "Rock", "subgenre": "Alternative", "mood": "Melancholic", "artist": "Radiohead",
            "duration": 236, "bpm": 80, "title": "Creep"
        },
        "coldplay_yellow": {
            "genre": "Rock", "subgenre": "Alternative", "mood": "Melancholic", "artist": "Coldplay",
            "duration": 267, "bpm": 85, "title": "Yellow"
        },
        "arctic_monkeys_dancing": {
            "genre": "Rock", "subgenre": "Alternative", "mood": "Upbeat", "artist": "Arctic Monkeys",
            "duration": 156, "bpm": 140, "title": "Dancing Shoes"
        },
        "queen_bohemian": {
            "genre": "Rock", "subgenre": "Classic", "mood": "Epic", "artist": "Queen",
            "duration": 354, "bpm": 72, "title": "Bohemian Rhapsody"
        },
        "led_zeppelin_stairway": {
            "genre": "Rock", "subgenre": "Classic", "mood": "Epic", "artist": "Led Zeppelin",
            "duration": 482, "bpm": 68, "title": "Stairway to Heaven"
        },
        "dua_lipa_physical": {
            "genre": "Pop", "subgenre": "Dance", "mood": "Energetic", "artist": "Dua Lipa",
            "duration": 193, "bpm": 148, "title": "Physical"
        },
        "bruno_mars_grenade": {
            "genre": "Pop", "subgenre": "Ballad", "mood": "Emotional", "artist": "Bruno Mars",
            "duration": 222, "bpm": 90, "title": "Grenade"
        },
        "ariana_grande_thank_u": {
            "genre": "Pop", "subgenre": "Dance", "mood": "Upbeat", "artist": "Ariana Grande",
            "duration": 207, "bpm": 145, "title": "Thank U, Next"
        },
        "norah_jones_come_away": {
            "genre": "Jazz", "subgenre": "Smooth", "mood": "Relaxing", "artist": "Norah Jones",
            "duration": 252, "bpm": 75, "title": "Come Away with Me"
        },
        "miles_davis_kind_of_blue": {
            "genre": "Jazz", "subgenre": "Bebop", "mood": "Complex", "artist": "Miles Davis",
            "duration": 330, "bpm": 110, "title": "So What"
        }
    }
    
    # Register metadata with recommender
    for song_id, metadata in song_metadata.items():
        recommender.song_metadata[song_id] = metadata
    
    # Simulate playing songs to build play history
    print("Simulating user listening history:")
    current_time = time.time()
    
    # Play Radiohead (seed song 1) - has similar song: Coldplay
    recommender.record_play("radiohead_creep", current_time, 236, song_metadata["radiohead_creep"])
    print("  - Played 'Creep' by Radiohead (236s, 80 BPM)")
    
    # Play Dua Lipa (seed song 2) - has similar song: Ariana Grande
    recommender.record_play("dua_lipa_physical", current_time - 300, 193, song_metadata["dua_lipa_physical"])
    print("  - Played 'Physical' by Dua Lipa (193s, 148 BPM)")
    
    # Play Queen (seed song 3) - has similar song: Led Zeppelin
    recommender.record_play("queen_bohemian", current_time - 600, 354, song_metadata["queen_bohemian"])
    print("  - Played 'Bohemian Rhapsody' by Queen (354s, 72 BPM)")
    
    print()
    
    # Mark some songs as skipped to show exclusion
    print("Marking some songs as recently skipped:")
    skipped_tracker.skip_song("led_zeppelin_stairway")  # Skip Led Zeppelin
    print("  - Skipped 'Stairway to Heaven' by Led Zeppelin")
    print()
    
    # Add some songs to active playlist to show exclusion
    print("Adding some songs to active playlist:")
    simple_playlist.songs.append("norah_jones_come_away")  # In active playlist
    print("  - 'Come Away with Me' by Norah Jones (currently in playlist)")
    print()
    
    # Generate recommendations
    print("Generating smart recommendations based on listening history:")
    recommendations = recommender.recommend(seed_count=3, top_n=5, exclude_active_playlist=True)
    
    if recommendations:
        print(f"  Found {len(recommendations)} personalized recommendations:")
        for i, rec in enumerate(recommendations, 1):
            # Get song title from metadata
            title = song_metadata.get(rec.song_id, {}).get('title', rec.song_id)
            artist = song_metadata.get(rec.song_id, {}).get('artist', 'Unknown Artist')
            print(f"    {i}. '{title}' by {artist}")
            print(f"       Score: {rec.score}, Reason: {rec.reason}")
    else:
        print("  No recommendations found. Showing popular songs as fallback:")
        popular_songs = recommender.get_popular_songs(top_n=3)
        for i, rec in enumerate(popular_songs, 1):
            title = song_metadata.get(rec.song_id, {}).get('title', rec.song_id)
            artist = song_metadata.get(rec.song_id, {}).get('artist', 'Unknown Artist')
            print(f"    {i}. '{title}' by {artist}")
            print(f"       Score: {rec.score}, Reason: {rec.reason}")
    
    print()
    
    # Show how the system adapts to different seeds
    print("Demonstrating adaptive recommendations:")
    print("  If we focused only on Pop music seeds...")
    
    # Clear previous history and simulate pop-focused listening
    # In a real system, we'd have a separate recommender instance or reset method
    pop_recommender = SmartRecommender(
        playlist_explorer=playlist_explorer,
        skipped_tracker=skipped_tracker,
        playlist_songs_getter=simple_playlist.get_all_songs,
        window_size=10,
        seed_count=2,
        top_n=3,
        duration_threshold=30,  # Tighter thresholds for pop
        bpm_threshold=10
    )
    
    # Record pop plays
    pop_recommender.record_play("dua_lipa_physical", current_time, 193, song_metadata["dua_lipa_physical"])
    pop_recommender.record_play("ariana_grande_thank_u", current_time - 200, 207, song_metadata["ariana_grande_thank_u"])
    
    pop_recommendations = pop_recommender.recommend(seed_count=2, top_n=3)
    if pop_recommendations:
        print("  Pop-focused recommendations:")
        for i, rec in enumerate(pop_recommendations, 1):
            title = song_metadata.get(rec.song_id, {}).get('title', rec.song_id)
            artist = song_metadata.get(rec.song_id, {}).get('artist', 'Unknown Artist')
            print(f"    {i}. '{title}' by {artist} (Score: {rec.score})")


if __name__ == "__main__":
    demo_smart_recommender()