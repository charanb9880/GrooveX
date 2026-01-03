#!/usr/bin/env python3
"""
Demo script showcasing the Recently Skipped Tracker feature.
"""

import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from playback_history.playback_controller import PlaybackController
from explorer.playlist_explorer import PlaylistExplorer
from recommend.recommender import SmartRecommender
from playback_history.skipped_tracker import RecentlySkippedTracker


def demo_recently_skipped_tracker():
    """Demonstrate the Recently Skipped Tracker feature."""
    print("=== PlayWise Music Engine - Recently Skipped Tracker Demo ===\n")
    
    # Create a playback controller
    controller = PlaybackController()
    
    # Add some songs to the playlist
    print("Adding songs to playlist:")
    song1 = controller.play_song("Bohemian Rhapsody", "Queen", 354, song_id="queen_001")
    song2 = controller.play_song("Stairway to Heaven", "Led Zeppelin", 482, song_id="lz_001")
    song3 = controller.play_song("Hotel California", "Eagles", 391, song_id="eagles_001")
    song4 = controller.play_song("Sweet Child O' Mine", "Guns N' Roses", 356, song_id="gnr_001")
    song5 = controller.play_song("Imagine", "John Lennon", 183, song_id="jl_001")
    
    print(f"  - {song1.title} (ID: {song1.song_id})")
    print(f"  - {song2.title} (ID: {song2.song_id})")
    print(f"  - {song3.title} (ID: {song3.song_id})")
    print(f"  - {song4.title} (ID: {song4.song_id})")
    print(f"  - {song5.title} (ID: {song5.song_id})")
    print()
    
    # Show initial playlist
    print("Initial playlist:")
    for i, song in enumerate(controller.get_playlist_songs()):
        print(f"  {i+1}. {song.title} by {song.artist}")
    print()
    
    # Skip some songs
    print("Skipping songs:")
    controller.skip_song("queen_001")  # Skip Bohemian Rhapsody
    controller.skip_song("eagles_001")  # Skip Hotel California
    print("  - Skipped 'Bohemian Rhapsody' (queen_001)")
    print("  - Skipped 'Hotel California' (eagles_001)")
    print()
    
    # Show recently skipped songs
    print("Recently skipped songs:")
    skipped = controller.skipped_tracker.get_recently_skipped()
    for song_id in skipped:
        print(f"  - {song_id}")
    print()
    
    # Try to play songs normally (should skip the skipped ones)
    print("Playing songs with autoplay (skipped songs will be avoided):")
    played_songs = []
    
    # Play first song (should be Stairway to Heaven since Bohemian Rhapsody is skipped)
    next_song = controller.play_next()
    if next_song:
        played_songs.append(next_song)
        print(f"  Playing: {next_song.title} by {next_song.artist}")
    
    # Play second song (should be Sweet Child O' Mine since Hotel California is skipped)
    next_song = controller.play_next()
    if next_song:
        played_songs.append(next_song)
        print(f"  Playing: {next_song.title} by {next_song.artist}")
    
    # Play third song (should be Imagine)
    next_song = controller.play_next()
    if next_song:
        played_songs.append(next_song)
        print(f"  Playing: {next_song.title} by {next_song.artist}")
    
    print()
    
    # Show remaining playlist
    print("Remaining playlist after autoplay:")
    remaining_songs = controller.get_playlist_songs()
    if remaining_songs:
        for i, song in enumerate(remaining_songs):
            print(f"  {i+1}. {song.title} by {song.artist}")
    else:
        print("  No songs remaining")
    print()
    
    # Demonstrate force play
    print("Force playing a skipped song:")
    # Add the skipped song back to playlist
    controller.playlist.add_song("Bohemian Rhapsody", "Queen", 354, song_id="queen_001")
    # Force play it
    next_song = controller.play_next(force_play_skipped=True)
    if next_song:
        print(f"  Force played: {next_song.title} by {next_song.artist}")
    print()
    
    # Show final stats
    print("Final stats:")
    print(f"  Recently skipped songs count: {len(controller.skipped_tracker.get_recently_skipped())}")
    print(f"  Songs in playlist: {len(controller.get_playlist_songs())}")


def demo_duplicate_cleaner():
    """Demonstrate the Duplicate Cleaner feature."""
    print("\n=== PlayWise Music Engine - Duplicate Cleaner Demo ===\n")
    
    # Create a playlist with duplicate cleaning enabled (default 'first' policy)
    from playlist.playlist import Playlist
    playlist_first = Playlist(enable_dedupe=True, dedupe_policy='first')
    
    print("Testing 'first' policy (keep first occurrence):")
    # Add first song
    result1 = playlist_first.add_song("Hello", "Artist", 180, song_id="1")
    print(f"  Added 'Hello' by 'Artist' (ID: 1) - Result: {result1}")
    
    # Try to add duplicate (should be rejected)
    result2 = playlist_first.add_song("Hello", "Artist", 200, song_id="2")
    print(f"  Tried to add duplicate 'Hello' by 'Artist' (ID: 2) - Result: {result2} (rejected, keeping first)")
    
    # Add a non-duplicate song
    result3 = playlist_first.add_song("Hello", "Different Artist", 180, song_id="3")
    print(f"  Added 'Hello' by 'Different Artist' (ID: 3) - Result: {result3}")
    
    print(f"  Final playlist size: {len(playlist_first.get_all_songs())}")
    for i, song in enumerate(playlist_first.get_all_songs()):
        print(f"    {i+1}. {song.title} by {song.artist} (ID: {song.song_id})")
    
    print("\nTesting 'latest' policy (keep latest occurrence):")
    # Create a playlist with 'latest' policy
    playlist_latest = Playlist(enable_dedupe=True, dedupe_policy='latest')
    
    # Add first song
    result1 = playlist_latest.add_song("Hello", "Artist", 180, song_id="1")
    print(f"  Added 'Hello' by 'Artist' (ID: 1) - Result: {result1}")
    
    # Try to add duplicate (should be accepted with 'latest' policy)
    result2 = playlist_latest.add_song("Hello", "Artist", 200, song_id="2")
    print(f"  Tried to add duplicate 'Hello' by 'Artist' (ID: 2) - Result: {result2}")
    
    print(f"  Final playlist size: {len(playlist_latest.get_all_songs())}")
    for i, song in enumerate(playlist_latest.get_all_songs()):
        print(f"    {i+1}. {song.title} by {song.artist} (ID: {song.song_id})")
    
    # Note: In a full implementation, the 'latest' policy would also remove the old song
    # from any catalogs or playlists, but for this demo we're just showing the registration behavior


def demo_favorite_queue():
    """Demonstrate the Favorite Queue feature."""
    print("\n=== PlayWise Music Engine - Favorite Queue Demo ===\n")
    
    # Create a playback controller
    controller = PlaybackController()
    
    # Add some songs
    song1 = controller.play_song("Bohemian Rhapsody", "Queen", 354, song_id="queen_001")
    song2 = controller.play_song("Stairway to Heaven", "Led Zeppelin", 482, song_id="lz_001")
    song3 = controller.play_song("Hotel California", "Eagles", 391, song_id="eagles_001")
    
    # Add songs to favorites
    print("Adding songs to favorites:")
    controller.add_to_favorites("queen_001", "Bohemian Rhapsody", "Queen")
    controller.add_to_favorites("lz_001", "Stairway to Heaven", "Led Zeppelin")
    controller.add_to_favorites("eagles_001", "Hotel California", "Eagles")
    print("  - Bohemian Rhapsody")
    print("  - Stairway to Heaven")
    print("  - Hotel California")
    print()
    
    # Simulate listens with different durations
    print("Simulating listens:")
    controller.favorite_queue.record_listen("queen_001", 100)  # 100 seconds
    controller.favorite_queue.record_listen("lz_001", 200)    # 200 seconds
    controller.favorite_queue.record_listen("eagles_001", 150) # 150 seconds
    
    controller.favorite_queue.record_listen("queen_001", 150)  # Another 150 seconds (total: 250)
    controller.favorite_queue.record_listen("lz_001", 50)     # Another 50 seconds (total: 250)
    controller.favorite_queue.record_listen("eagles_001", 200) # Another 200 seconds (total: 350)
    
    print("  - Bohemian Rhapsody: 100s + 150s = 250s total")
    print("  - Stairway to Heaven: 200s + 50s = 250s total")
    print("  - Hotel California: 150s + 200s = 350s total")
    print()
    
    # Get top 3 favorites
    print("Top 3 favorite songs:")
    top_favorites = controller.get_top_favorites(3)
    for i, song_summary in enumerate(top_favorites):
        print(f"  {i+1}. {song_summary.title} by {song_summary.artist} ({song_summary.total_listen_time}s)")


def demo_playlist_explorer():
    """Demonstrate the Playlist Explorer Tree feature."""
    print("\n=== PlayWise Music Engine - Playlist Explorer Tree Demo ===\n")
    
    # Create playlist explorer
    explorer = PlaylistExplorer()
    
    # Add songs with hierarchical classification
    print("Adding songs to the explorer tree:")
    explorer.add_song("song1", "Rock", "Alternative", "Melancholic", "Radiohead")
    explorer.add_song("song2", "Rock", "Alternative", "Upbeat", "Arctic Monkeys")
    explorer.add_song("song3", "Pop", "Dance", "Energetic", "Dua Lipa")
    explorer.add_song("song4", "Rock", "Classic", None, "Queen")
    explorer.add_song("song5", "Jazz", "Smooth", "Relaxing", "Norah Jones")
    
    print("  - song1: Rock -> Alternative -> Melancholic -> Radiohead")
    print("  - song2: Rock -> Alternative -> Upbeat -> Arctic Monkeys")
    print("  - song3: Pop -> Dance -> Energetic -> Dua Lipa")
    print("  - song4: Rock -> Classic -> Queen")
    print("  - song5: Jazz -> Smooth -> Relaxing -> Norah Jones")
    print()
    
    # Demonstrate traversal
    print("Tree traversal (BFS):")
    for path, node in explorer.traverse(method='bfs'):
        indent = "  " * len(path)
        if path:
            print(f"{indent}- {node.key}")
        else:
            print("Root")
    
    print()
    
    # Demonstrate search
    print("Searching for Rock songs:")
    rock_songs = explorer.search({"genre": "Rock"})
    print(f"  Found {len(rock_songs)} Rock songs: {rock_songs}")
    
    print("\nSearching for Alternative Rock songs:")
    alt_rock_songs = explorer.search({"genre": "Rock", "subgenre": "Alternative"})
    print(f"  Found {len(alt_rock_songs)} Alternative Rock songs: {alt_rock_songs}")
    
    # Demonstrate get by path
    print("\nGetting songs by specific path (Rock -> Alternative -> Melancholic -> Radiohead):")
    radiohead_songs = explorer.get_by_path(["rock", "alternative", "melancholic", "radiohead"])
    print(f"  Songs at path: {radiohead_songs}")


def demo_smart_recommender():
    """Demonstrate the Smart Recommender feature."""
    print("\n=== PlayWise Music Engine - Smart Recommender Demo ===\n")
    
    # Create real instances
    playlist_explorer = PlaylistExplorer()
    skipped_tracker = RecentlySkippedTracker()
    
    # Simple playlist implementation for demo
    class SimplePlaylist:
        def __init__(self):
            self.songs = []
        
        def get_all_songs(self):
            class MockSong:
                def __init__(self, song_id):
                    self.song_id = song_id
            
            return [MockSong(song_id) for song_id in self.songs]
    
    simple_playlist = SimplePlaylist()
    
    # Create recommender
    recommender = SmartRecommender(
        playlist_explorer=playlist_explorer,
        skipped_tracker=skipped_tracker,
        playlist_songs_getter=simple_playlist.get_all_songs,
        window_size=10,
        seed_count=3,
        top_n=5
    )
    
    # Add songs to the explorer with hierarchical classification
    playlist_explorer.add_song("song1", "Rock", "Alternative", "Melancholic", "Radiohead")
    playlist_explorer.add_song("song2", "Rock", "Alternative", "Melancholic", "Coldplay")
    playlist_explorer.add_song("song3", "Rock", "Classic", "Epic", "Queen")
    playlist_explorer.add_song("song4", "Pop", "Dance", "Energetic", "Dua Lipa")
    
    # Add rich metadata for recommendation engine
    song_metadata = {
        "song1": {
            "genre": "Rock", "subgenre": "Alternative", "mood": "Melancholic", "artist": "Radiohead",
            "duration": 200, "bpm": 120
        },
        "song2": {
            "genre": "Rock", "subgenre": "Alternative", "mood": "Melancholic", "artist": "Coldplay",
            "duration": 210, "bpm": 125
        },
        "song3": {
            "genre": "Rock", "subgenre": "Classic", "mood": "Epic", "artist": "Queen",
            "duration": 350, "bpm": 110
        },
        "song4": {
            "genre": "Pop", "subgenre": "Dance", "mood": "Energetic", "artist": "Dua Lipa",
            "duration": 180, "bpm": 130
        }
    }
    
    # Register metadata with recommender
    for song_id, metadata in song_metadata.items():
        recommender.song_metadata[song_id] = metadata
    
    # Simulate playing songs
    print("Simulating playback history:")
    current_time = time.time()
    
    # Play song1 (Radiohead)
    recommender.record_play("song1", current_time, 200, song_metadata["song1"])
    print("  - Played 'song1' (Radiohead) for 200 seconds")
    
    # Play song3 (Queen)
    recommender.record_play("song3", current_time - 300, 350, song_metadata["song3"])
    print("  - Played 'song3' (Queen) for 350 seconds")
    
    print()
    
    # Get recommendations
    print("Generating smart recommendations based on recent plays:")
    recommendations = recommender.recommend(seed_count=2, top_n=5)
    
    if recommendations:
        print(f"  Found {len(recommendations)} recommendations:")
        for i, rec in enumerate(recommendations, 1):
            print(f"    {i}. Song ID: {rec.song_id}, Score: {rec.score}, Reason: {rec.reason}")
    else:
        print("  No recommendations found. Showing popular songs as fallback:")
        popular_songs = recommender.get_popular_songs(top_n=3)
        for i, rec in enumerate(popular_songs, 1):
            print(f"    {i}. Song ID: {rec.song_id}, Score: {rec.score}, Reason: {rec.reason}")

def demo_artist_blocklist():
    """Demonstrate the Artist Blocklist feature."""
    print("\n=== PlayWise Music Engine - Artist Blocklist Demo ===\n")
    
    # Create a playlist
    from playlist.playlist import Playlist
    playlist = Playlist()
    
    # Add some artists to the blocklist
    print("Blocking artists: The Beatles, Led Zeppelin")
    playlist.artist_blocklist.add_artist("The Beatles")
    playlist.artist_blocklist.add_artist("Led Zeppelin")
    
    # Try to add songs by blocked artists
    print("\nTrying to add songs by blocked artists:")
    result1 = playlist.add_song("Hey Jude", "The Beatles", 431)
    if result1 == "BLOCKED_ARTIST":
        print("  - Attempt to add 'Hey Jude' by The Beatles: REJECTED (blocked artist)")
    else:
        print("  - Attempt to add 'Hey Jude' by The Beatles: ACCEPTED")
    
    result2 = playlist.add_song("Stairway to Heaven", "Led Zeppelin", 482)
    if result2 == "BLOCKED_ARTIST":
        print("  - Attempt to add 'Stairway to Heaven' by Led Zeppelin: REJECTED (blocked artist)")
    else:
        print("  - Attempt to add 'Stairway to Heaven' by Led Zeppelin: ACCEPTED")
    
    # Try to add songs by allowed artists
    print("\nTrying to add songs by allowed artists:")
    result3 = playlist.add_song("Bohemian Rhapsody", "Queen", 354)
    if result3 == "BLOCKED_ARTIST":
        print("  - Attempt to add 'Bohemian Rhapsody' by Queen: REJECTED (blocked artist)")
    else:
        print("  - Attempt to add 'Bohemian Rhapsody' by Queen: ACCEPTED")
    
    result4 = playlist.add_song("Imagine", "John Lennon", 183)
    if result4 == "BLOCKED_ARTIST":
        print("  - Attempt to add 'Imagine' by John Lennon: REJECTED (blocked artist)")
    else:
        print("  - Attempt to add 'Imagine' by John Lennon: ACCEPTED")
    
    # Show current blocklist
    print("\nCurrent blocked artists:")
    blocked_artists = playlist.artist_blocklist.get_blocked_artists()
    if blocked_artists:
        for artist in blocked_artists:
            print(f"  - {artist}")
    else:
        print("  No blocked artists")
    
    # Remove an artist from blocklist
    print("\nRemoving 'Led Zeppelin' from blocklist...")
    removed = playlist.artist_blocklist.remove_artist("Led Zeppelin")
    if removed:
        print("  Successfully removed 'Led Zeppelin' from blocklist")
    else:
        print("  Failed to remove 'Led Zeppelin' (not in blocklist)")
    
    # Try adding the song again
    print("\nTrying to add 'Stairway to Heaven' by Led Zeppelin again:")
    result5 = playlist.add_song("Stairway to Heaven", "Led Zeppelin", 482)
    if result5 == "BLOCKED_ARTIST":
        print("  - Attempt to add 'Stairway to Heaven' by Led Zeppelin: REJECTED (blocked artist)")
    else:
        print("  - Attempt to add 'Stairway to Heaven' by Led Zeppelin: ACCEPTED")
    
    # Show final playlist
    print("\nFinal playlist:")
    songs = playlist.get_all_songs()
    if songs:
        for i, song in enumerate(songs, 1):
            print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    else:
        print("  No songs in playlist")

def demo_play_duration_visualizer():
    """Demonstrate the Play Duration Visualizer feature."""
    print("\n=== PlayWise Music Engine - Play Duration Visualizer Demo ===\n")
    
    # Create components
    from playlist.playlist import Playlist
    from playback_history.playback_controller import PlaybackController
    from song_rating_tree.song_rating_engine import SongRatingEngine
    from song_lookup_map.lookup_map import SongLookupMap
    from system_dashboard.dashboard import SystemDashboard
    
    playlist = Playlist()
    playback_controller = PlaybackController()
    rating_engine = SongRatingEngine()
    lookup_map = SongLookupMap()
    
    # Add songs with various durations
    print("Adding songs to playlist:")
    songs_data = [
        ("Imagine", "John Lennon", 183),
        ("Hey Jude", "The Beatles", 431),
        ("Bohemian Rhapsody", "Queen", 354),
        ("Stairway to Heaven", "Led Zeppelin", 482),
        ("Hotel California", "Eagles", 391),
        ("Yesterday", "The Beatles", 125)
    ]
    
    for title, artist, duration in songs_data:
        playlist.add_song(title, artist, duration)
        print(f"  - Added '{title}' by {artist} [{duration}s]")
    
    # Create dashboard
    dashboard = SystemDashboard(playlist, playback_controller, rating_engine, lookup_map)
    
    # Print play duration visualization
    dashboard.print_play_duration_visualization()

def demo_undo_last_n_edits():
    """Demonstrate the Undo Last N Playlist Edits feature."""
    print("\n=== PlayWise Music Engine - Undo Last N Playlist Edits Demo ===\n")
    
    from playlist.playlist import Playlist
    
    playlist = Playlist()
    
    # Add some songs
    print("Adding songs to playlist:")
    playlist.add_song("Song 1", "Artist A", 180)
    print("  - Added 'Song 1' by Artist A")
    playlist.add_song("Song 2", "Artist B", 200)
    print("  - Added 'Song 2' by Artist B")
    playlist.add_song("Song 3", "Artist A", 190)
    print("  - Added 'Song 3' by Artist A")
    playlist.add_song("Song 4", "Artist C", 210)
    print("  - Added 'Song 4' by Artist C")
    
    # Show initial playlist
    print("\nInitial playlist:")
    songs = playlist.get_all_songs()
    for i, song in enumerate(songs, 1):
        print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    
    # Show action history
    print("\nAction history:", playlist.get_action_history())
    
    # Perform some edits
    print("\nPerforming edits:")
    playlist.move_song(0, 2)  # Move Song 1 from index 0 to index 2
    print("  - Moved song from index 0 to 2")
    playlist.delete_song(1)    # Delete song at index 1
    print("  - Deleted song at index 1")
    
    # Show playlist after edits
    print("\nPlaylist after edits:")
    songs = playlist.get_all_songs()
    for i, song in enumerate(songs, 1):
        print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    
    # Show action history
    print("\nAction history:", playlist.get_action_history())
    
    # Undo last 2 actions
    print("\nUndoing last 2 actions:")
    undone = playlist.undo_last_n_actions(2)
    print(f"  Undone actions: {undone}")
    
    # Show final playlist
    print("\nFinal playlist after undo:")
    songs = playlist.get_all_songs()
    for i, song in enumerate(songs, 1):
        print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    
    # Show action history
    print("\nAction history after undo:", playlist.get_action_history())

def demo_shuffle_with_constraints():
    """Demonstrate the Shuffle with Constraints feature."""
    print("\n=== PlayWise Music Engine - Shuffle with Constraints Demo ===\n")
    
    from playlist.playlist import Playlist
    
    playlist = Playlist()
    
    # Add songs with some artists appearing multiple times
    print("Adding songs to playlist:")
    songs_data = [
        ("Song 1", "Artist A", 180),
        ("Song 2", "Artist B", 200),
        ("Song 3", "Artist A", 190),
        ("Song 4", "Artist C", 210),
        ("Song 5", "Artist B", 195),
        ("Song 6", "Artist D", 205)
    ]
    
    for title, artist, duration in songs_data:
        playlist.add_song(title, artist, duration)
        print(f"  - Added '{title}' by {artist} [{duration}s]")
    
    # Show initial playlist
    print("\nInitial playlist:")
    songs = playlist.get_all_songs()
    for i, song in enumerate(songs, 1):
        print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    
    # Show artist distribution
    from playlist.constrained_shuffle import ConstrainedShuffler
    shuffler = ConstrainedShuffler()
    distribution = shuffler.get_artist_distribution(songs)
    print("\nArtist distribution:")
    for artist, count in distribution.items():
        print(f"  - {artist}: {count} song(s)")
    
    # Shuffle with constraints
    print("\nShuffling with artist constraints (no consecutive same artists):")
    shuffled_songs = playlist.shuffle_with_artist_constraints()
    
    # Show shuffled playlist
    print("\nShuffled playlist:")
    songs = playlist.get_all_songs()
    for i, song in enumerate(songs, 1):
        print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    
    # Verify no consecutive artists
    print("\nVerifying no consecutive artists:")
    has_consecutive = False
    for i in range(len(songs) - 1):
        if songs[i].artist.lower() == songs[i + 1].artist.lower():
            print(f"  WARNING: Consecutive songs by {songs[i].artist}")
            has_consecutive = True
    if not has_consecutive:
        print("  SUCCESS: No consecutive songs by the same artist")

def demo_merge_playlists():
    """Demonstrate the Merge Two Playlists Alternately feature."""
    print("\n=== PlayWise Music Engine - Merge Two Playlists Alternately Demo ===\n")
    
    from playlist.playlist import Playlist
    
    # Create first playlist
    playlist1 = Playlist()
    playlist1.add_song("Song A1", "Artist A", 180)
    playlist1.add_song("Song A2", "Artist A", 200)
    playlist1.add_song("Song A3", "Artist A", 190)
    playlist1.add_song("Song A4", "Artist A", 210)
    
    # Create second playlist
    playlist2 = Playlist()
    playlist2.add_song("Song B1", "Artist B", 210)
    playlist2.add_song("Song B2", "Artist B", 195)
    playlist2.add_song("Song B3", "Artist B", 205)
    
    print("Playlist 1:")
    songs1 = playlist1.get_all_songs()
    for i, song in enumerate(songs1, 1):
        print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    
    print("\nPlaylist 2:")
    songs2 = playlist2.get_all_songs()
    for i, song in enumerate(songs2, 1):
        print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    
    # Merge playlists alternately
    print("\nMerging playlists alternately:")
    merged_playlist = playlist1.merge_alternately(playlist2)
    
    print("\nMerged playlist:")
    merged_songs = merged_playlist.get_all_songs()
    for i, song in enumerate(merged_songs, 1):
        print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    
    # Verify alternating pattern
    print("\nVerifying alternating pattern:")
    expected_pattern = ["A", "B", "A", "B", "A", "B", "A"]
    actual_pattern = [song.artist.split()[-1][0] for song in merged_songs]  # Extract first letter of last word
    
    if actual_pattern[:6] == ["A", "B", "A", "B", "A", "B"]:
        print("  SUCCESS: Correct alternating pattern")
    else:
        print(f"  ERROR: Expected {expected_pattern[:6]}, got {actual_pattern[:6]}")

def demo_mini_player():
    """Demonstrate the Memory-Efficient Mini Player Mode feature."""
    print("\n=== PlayWise Music Engine - Memory-Efficient Mini Player Mode Demo ===\n")
    
    from playlist.mini_player import MiniPlayer
    from playlist.song import Song
    
    # Create songs (limited to window size for this demo)
    songs = [
        Song("Song 1", "Artist A", 180),
        Song("Song 2", "Artist B", 200),
        Song("Song 3", "Artist C", 190)
    ]
    
    # Create mini player with window size of 3
    player = MiniPlayer(window_size=3)
    player.preload_songs(songs)
    
    print(f"Preloaded {len(songs)} songs with window size {player.get_window_size()}")
    print("Upcoming songs in buffer:")
    upcoming = player.get_upcoming_songs()
    for i, song in enumerate(upcoming, 1):
        print(f"  {i}. {song.title} by {song.artist} [{song.duration}s]")
    
    # Play songs one by one
    print("\nPlaying songs:")
    while not player.is_finished():
        current_song = player.play_next()
        if current_song:
            print(f"  Playing: {current_song.title} by {current_song.artist} [{current_song.duration}s]")
            
            # Show upcoming songs
            upcoming = player.get_upcoming_songs()
            if upcoming:
                print(f"    Upcoming: {[song.title for song in upcoming]}")
            else:
                print("    No more upcoming songs")
        
        # Show played songs
        played = player.get_played_songs()
        if played:
            print(f"    Played: {[song.title for song in played]}")
    
    print("\nAll songs played. Player finished.")
    print(f"Total played songs: {len(player.get_played_songs())}")


if __name__ == "__main__":
    demo_recently_skipped_tracker()
    demo_duplicate_cleaner()
    demo_favorite_queue()
    demo_playlist_explorer()
    demo_smart_recommender()
    demo_artist_blocklist()
    demo_play_duration_visualizer()
    demo_undo_last_n_edits()
    demo_shuffle_with_constraints()
    demo_merge_playlists()
    demo_mini_player()