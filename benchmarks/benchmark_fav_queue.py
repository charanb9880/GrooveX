#!/usr/bin/env python3
"""
Benchmark script for the FavoriteQueue performance.
"""

import sys
import os
import time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from favorites.favorite_queue import FavoriteQueue


def benchmark_favorite_queue():
    """Benchmark the FavoriteQueue performance."""
    print("=== FavoriteQueue Performance Benchmark ===\n")
    
    fav_queue = FavoriteQueue()
    
    # Add 1000 songs to favorites
    print("Adding 1000 songs to favorites...")
    start_time = time.time()
    for i in range(1000):
        fav_queue.add_to_favorites(f"song_{i}", f"Song {i}", f"Artist {i}")
    end_time = time.time()
    print(f"  Time to add 1000 songs: {end_time - start_time:.4f} seconds")
    
    # Simulate 10000 listen events
    print("\nSimulating 10000 listen events...")
    start_time = time.time()
    for i in range(10000):
        song_id = f"song_{i % 1000}"
        fav_queue.record_listen(song_id, 30)  # 30 seconds per listen
    end_time = time.time()
    print(f"  Time to record 10000 listens: {end_time - start_time:.4f} seconds")
    
    # Get top 10 favorites 100 times
    print("\nGetting top 10 favorites 100 times...")
    start_time = time.time()
    for i in range(100):
        top_songs = fav_queue.get_top_n(10)
    end_time = time.time()
    print(f"  Time to get top 10 songs 100 times: {end_time - start_time:.4f} seconds")
    
    # Show final results
    print("\nFinal Results:")
    top_songs = fav_queue.get_top_n(5)
    print("  Top 5 favorite songs:")
    for i, song_summary in enumerate(top_songs):
        print(f"    {i+1}. {song_summary.title} by {song_summary.artist} ({song_summary.total_listen_time}s)")
    
    print(f"\nTotal benchmark time: {time.time() - start_time:.4f} seconds")


if __name__ == "__main__":
    benchmark_favorite_queue()