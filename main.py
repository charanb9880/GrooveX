"""
Integrated main.py demonstrating combined features of PlayWise backend engine:
- Problem 1: Playlist Engine (Doubly Linked List)
- Problem 2: Playback History (Stack with undo functionality)
This centralized script serves as an end-to-end example running core functionalities.
"""

import time
from playlist.playlist import Playlist
from playlist.song import Song
from playback_history.playback_controller import PlaybackController
from song_rating_tree.song_rating_engine import SongRatingEngine
from song_lookup_map.lookup_map import SongLookupMap
from playlist_sorting.sort_engine import SortCriteria
from playlist_sorting.sort_engine import SortEngine
from system_dashboard.dashboard import SystemDashboard
def demonstrate_problem_1():
    """
    Demonstrates Problem 1 features: creating playlist,
    adding, moving, reversing, deleting songs, and printing results.
    """
    print("=== Problem 1: Playlist Engine ===")

    playlist = Playlist()
    playlist.add_song("Imagine", "John Lennon", 183)
    playlist.add_song("Bohemian Rhapsody", "Queen", 354)
    playlist.add_song("Hey Jude", "The Beatles", 431)

    print("\nInitial Playlist:")
    for song in playlist.get_all_songs():
        print(f"- {song.title} by {song.artist} [{song.duration}s]")

    # Move first song to last position
    playlist.move_song(0, 2)
    print("\nPlaylist after moving the first song to last:")
    for song in playlist.get_all_songs():
        print(f"- {song.title} by {song.artist} [{song.duration}s]")

    # Reverse the playlist
    playlist.reverse_playlist()
    print("\nPlaylist after reversing:")
    for song in playlist.get_all_songs():
        print(f"- {song.title} by {song.artist} [{song.duration}s]")

    # Delete song at index 1
    playlist.delete_song(1)
    print("\nPlaylist after deleting the second song:")
    for song in playlist.get_all_songs():
        print(f"- {song.title} by {song.artist} [{song.duration}s]")

def demonstrate_problem_2():
    """
    Demonstrates Problem 2 features: playing songs (adding to playlist and history),
    undoing last played song, and printing playlist state after actions.
    """
    print("\n=== Problem 2: Playback History ===")

    controller = PlaybackController()

    # Play songs through controller (adds playlist + records history)
    controller.play_song("Shape of You", "Ed Sheeran", 240)
    controller.play_song("Blinding Lights", "The Weeknd", 200)
    controller.play_song("Levitating", "Dua Lipa", 210)

    print("\nPlaylist after playing songs:")
    for song in controller.get_playlist_songs():
        print(f"- {song.title} by {song.artist} [{song.duration}s]")

    # Undo last played song (re-add it back to playlist)
    if controller.undo_last_play(controller.playlist):
        print("\nUndo last play succeeded.")
    else:
        print("\nNo song to undo.")

    print("\nPlaylist after undoing last played song:")
    for song in controller.get_playlist_songs():
        print(f"- {song.title} by {song.artist} [{song.duration}s]")


def demonstrate_problem_3():
    """
    Demonstrates Problem 3 features: using a BST to index songs by ratings,
    showing fast insertion, search, and deletion in rating buckets.
    """
    print("\n=== Problem 3: Song Rating Tree (BST) ===")

    engine = SongRatingEngine()

    # Create Song objects (reuse Song class from playlist module!)
    song1 = Song(song_id=1, title="Imagine", artist="John Lennon", duration=183)
    song2 = Song(song_id=2, title="Bohemian Rhapsody", artist="Queen", duration=354)
    song3 = Song(song_id=3, title="Hey Jude", artist="The Beatles", duration=431)
    song4 = Song(song_id=4, title="Shape of You", artist="Ed Sheeran", duration=240)

    # Insert songs with different ratings
    engine.insert_song(song1, rating=5)
    engine.insert_song(song2, rating=4)
    engine.insert_song(song3, rating=5)
    engine.insert_song(song4, rating=3)

    print("\nSongs with rating 5:")
    songs_5 = engine.search_by_rating(5)
    for s in songs_5:
        print(f"- {s.song_id}: {s.title} by {s.artist} [{s.duration}s]")

    print("\nSongs with rating 4:")
    songs_4 = engine.search_by_rating(4)
    for s in songs_4:
        print(f"- {s.song_id}: {s.title} by {s.artist} [{s.duration}s]")

    # Delete a song from rating tree and show updated bucket
    engine.delete_song(3)  # Deletes "Hey Jude"
    print("\nSongs with rating 5 after deleting song_id 3 ('Hey Jude'):")
    songs_5_updated = engine.search_by_rating(5)
    for s in songs_5_updated:
        print(f"- {s.song_id}: {s.title} by {s.artist} [{s.duration}s]")


def demonstrate_problem_4():
    print("\n=== Problem 4: Instant Song Lookup (HashMap) ===")
    lookup = SongLookupMap()
    
    # Create and add songs to the map
    song1 = Song(song_id=1, title="Imagine", artist="John Lennon", duration=183)
    song2 = Song(song_id=2, title="Bohemian Rhapsody", artist="Queen", duration=354)
    song3 = Song(song_id=3, title="Hey Jude", artist="The Beatles", duration=431)
    song4 = Song(song_id=4, title="Shape of You", artist="Ed Sheeran", duration=240)

    # Add songs to the lookup structure
    lookup.add_song(song1)
    lookup.add_song(song2)
    lookup.add_song(song3)
    lookup.add_song(song4)

    # Instant lookup by song_id
    print("\nLookup by song ID (song_id=2):")
    result = lookup.lookup_song_by_id(2)
    if result:
        print(f"Found: {result.song_id}: {result.title} by {result.artist} [{result.duration}s]")
    else:
        print("Song not found.")

    # Instant lookup by song title
    print("\nLookup by song title ('Hey Jude'):")
    result = lookup.lookup_song_by_title("Hey Jude")
    if result:
        print(f"Found: {result.song_id}: {result.title} by {result.artist} [{result.duration}s]")
    else:
        print("Song not found.")

    # Remove a song and show that lookup fails
    lookup.remove_song(3)
    print("\nLookup by song ID (song_id=3) after removal:")
    result = lookup.lookup_song_by_id(3)
    print("Found." if result else "Song not found.")

def demonstrate_problem_5():
    print("\n=== Problem 5: Time-based Sorting (Merge Sort) ===")
    sorter = SortEngine()

    # Create sample songs with added_time attribute (simulate recentness)
    now = int(time.time())
    song1 = Song("Imagine", "John Lennon", 183, song_id=1)
    song1.added_time = now - 300
    song2 = Song("Bohemian Rhapsody", "Queen", 354, song_id=2)
    song2.added_time = now - 400
    song3 = Song("Hey Jude", "The Beatles", 431, song_id=3)
    song3.added_time = now - 200
    song4 = Song("All You Need Is Love", "The Beatles", 180, song_id=4)
    song4.added_time = now - 350

    songs = [song1, song2, song3, song4]

    # Sort alphabetically by Title
    sorted_by_title = sorter.merge_sort(songs, SortCriteria.ALPHA_TITLE)
    print("\nSorted by Title (Alphabetical):")
    for s in sorted_by_title:
        print(f"- {s.title} by {s.artist}")

    # Sort by Duration Ascending
    sorted_by_duration_asc = sorter.merge_sort(songs, SortCriteria.DURATION_ASC)
    print("\nSorted by Duration (Ascending):")
    for s in sorted_by_duration_asc:
        print(f"- {s.title} by {s.artist} [{s.duration}s]")

    # Sort by Duration Descending
    sorted_by_duration_desc = sorter.merge_sort(songs, SortCriteria.DURATION_DESC)
    print("\nSorted by Duration (Descending):")
    for s in sorted_by_duration_desc:
        print(f"- {s.title} by {s.artist} [{s.duration}s]")

    # Sort by Recently Added
    sorted_by_recent = sorter.merge_sort(songs, SortCriteria.RECENT)
    print("\nSorted by Recently Added:")
    for s in sorted_by_recent:
        print(f"- {s.title} by {s.artist} [Added {now - s.added_time}s ago]")

def demonstrate_problem_7():
    print("\n=== Problem 7: System Snapshot Dashboard ===")
    
    # Set up complete system
    playlist = Playlist()
    playback_controller = PlaybackController()
    rating_engine = SongRatingEngine()
    lookup_map = SongLookupMap()
    
    # Add diverse songs
    songs_data = [
        ("Imagine", "John Lennon", 183, 5),
        ("Bohemian Rhapsody", "Queen", 354, 5),
        ("Hey Jude", "The Beatles", 431, 4),
        ("Yesterday", "The Beatles", 125, 4),
        ("Stairway to Heaven", "Led Zeppelin", 482, 5),
        ("Hotel California", "Eagles", 391, 4),
        ("Smells Like Teen Spirit", "Nirvana", 301, 3)
    ]
    
    for title, artist, duration, rating in songs_data:
        playlist.add_song(title, artist, duration)
        song = Song(title, artist, duration, song_id=len(playlist.get_all_songs()))
        rating_engine.insert_song(song, rating)
        lookup_map.add_song(song)
        playback_controller.play_song(title, artist, duration)
    
    # Create and display dashboard
    dashboard = SystemDashboard(playlist, playback_controller, rating_engine, lookup_map)
    dashboard.print_dashboard()
    
    # Export snapshot to JSON
    import json
    snapshot = dashboard.export_snapshot()
    print("Snapshot JSON:")
    print(json.dumps(snapshot, indent=2))

def main():
    """
    Main driver executing demonstrations of all problem features sequentially.
    """
    demonstrate_problem_1()
    demonstrate_problem_2()
    demonstrate_problem_3()
    demonstrate_problem_4()
    demonstrate_problem_5()
    demonstrate_problem_7()

if __name__ == "__main__":
    main()
