# PlayWise Music Engine

A modular backend engine for personalized playlist management and instant music search, designed for education, hackathons, and scalable music platforms.

***

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Concepts & Data Structures](#concepts--data-structures)
- [Folder Structure](#folder-structure)
- [Getting Started](#getting-started)
- [How to Run (With VS Code or CLI)](#how-to-run-with-vs-code-or-cli)
- [Testing](#testing)
- [Author and License](#author-and-license)

***

## Project Overview

PlayWise helps users experience music like never before by combining data structures, algorithms, and clean code to deliver:

- Dynamic playlist management  
- Playback history and undo  
- Song rating and recommendations  
- Instant lookup by song ID or title (even on huge lists!)
- Time-based sorting with custom merge sort
- Recently skipped tracker to prevent replay during autoplay
- Auto-cleaner for duplicate songs based on title+artist
- Sorted queue of favorite songs ordered by cumulative listen time
- Performance optimization through complexity analysis
- Live system dashboard for debugging and monitoring

This repo is a teaching-grade demo of how core CS concepts can power real-world systems.

***

## Features

| Problem # | Feature                              | Core Functionality                                                                 |
|-----------|--------------------------------------|------------------------------------------------------------------------------------|
| 1         | Playlist Engine (Doubly Linked List) | Add, move, reverse, delete songs efficiently                                       |
| 2         | Playback History (Stack)             | Record playback order, allow undo/re-add last played song                          |
| 3         | Song Rating Tree (BST)               | Index/search/delete songs by rating; each rating = a bucket in binary search tree  |
| 4         | Instant Song Lookup (HashMap)        | O(1) retrieval of song by song ID or title; map is kept synced with playlist       |
| 5         | Time-based Sorting (Merge Sort)      | Sort playlists by title, duration, or recently added using custom merge sort       |
| 6         | Playback Optimization (Analysis)     | Annotate methods with time/space complexity; identify optimization opportunities   |
| 7         | System Snapshot Dashboard            | Live debugging interface showing top songs, recent plays, and rating distribution  |
| 8         | Recently Skipped Tracker             | Track recently skipped songs to prevent replay during autoplay                     |
| 9         | Duplicate Cleaner                    | Auto-detect and handle duplicate songs based on title+artist composite key         |
| 10        | Favorite Songs Queue                 | Maintain sorted queue of favorite songs by cumulative listen time                  |
| 11        | Playlist Explorer Tree               | Hierarchical classification of songs by Genre → Subgenre → Mood → Artist          |
| 12        | Smart Recommendations                | Intelligent song recommendations based on play history and similarity scoring      |
| 13        | Artist Blocklist                     | Permanently block songs by specific artists across all playlists                   |
| 14        | Play Duration Visualizer             | Summary of total playtime, longest song, and shortest song in a playlist           |
| 15        | Undo Last N Playlist Edits           | Record every playlist edit as a reversible action using stack-based undo           |
| 16        | Shuffle with Constraints             | Shuffle a playlist such that the same artist doesn't repeat consecutively           |
| 17        | Merge Two Playlists Alternately      | Interleave two linked lists song-by-song                                          |
| 18        | Memory-Efficient Mini Player Mode    | Maintain a queue of 5 upcoming songs, discard as each is played                    |

***

## Concepts & Data Structures

- **Doubly Linked List:** Used for fast and flexible playlist operations.
- **Stack:** Supports undo in playback history (LIFO pattern).
- **Binary Search Tree (BST):** Bins songs into rating buckets (nodes), for O(log n) search by user rating.
- **Hash Map (dict):** Enables constant-time lookup by song ID or title—critical for scalable search.
- **Merge Sort:** Divide-and-conquer sorting algorithm with O(n log n) time complexity for flexible playlist ordering.
- **Circular Buffer/Deque:** Efficient fixed-size FIFO queue for tracking recently skipped songs with O(1) operations.
- **Composite Key Hashing:** Normalize and combine title+artist for duplicate detection with O(1) operations.
- **Max-Heap with Lazy Updates:** Maintain favorite songs ordered by listen time with efficient updates.
- **N-ary Tree:** Hierarchical classification of songs by genre/subgenre/mood/artist for playlist exploration.
- **Sliding Window + Similarity Scoring:** Recommend songs based on recent plays with multi-factor similarity metrics.
- **HashSet:** O(1) membership checking for artist blocklist functionality.
- **Aggregation Logic:** Compute total playtime using summation across all songs.
- **Min/Max Tracking:** Identify shortest and longest songs using linear scan with tracking variables.
- **Action Logger:** Stack-based undo functionality using the Command pattern.
- **Conditional Rearrangement:** Shuffle algorithms with artist constraint checking.
- **Linked List Traversal:** Interleave two linked lists for playlist merging.
- **Queue-based Buffering:** Sliding window approach for memory-efficient song preloading.
- **Complexity Analysis:** Time and space analysis for all core operations to ensure optimal performance.
- **System Integration:** Dashboard aggregates data from all modules using sorting, BST traversal, and hash map lookups.

All modules are extensible and use Python OOP best practices.

***

## Recently Skipped Tracker

The Recently Skipped Tracker is a feature that maintains a fixed-size history (default 10) of recently skipped songs to prevent them from being replayed during autoplay. The tracker uses a combination of a deque with maxlen and a set for O(1) operations:

- When autoplay selects the next song, it automatically skips any song whose ID is currently in the skipped tracker
- Users can force play a song even if it's in the tracker by using the `force_play_skipped=True` parameter
- The tracker exposes APIs for skipping songs, checking if a song is recently skipped, retrieving the list of skipped songs, clearing the tracker, and adjusting capacity

This feature enhances the user experience by preventing repetitive playback of songs the user has explicitly skipped.

***

## Duplicate Cleaner

The Duplicate Cleaner automatically detects and handles duplicate songs based on a normalized composite key of title and artist. It offers two policies for handling duplicates:

- **'first' policy:** Keep the first occurrence of a song and reject subsequent duplicates
- **'latest' policy:** Remove the old occurrence and keep the latest one

The cleaner uses efficient hashing for O(1) duplicate detection and provides APIs for checking duplicates, registering songs, and deregistering songs.

***

## Favorite Songs Queue

The Favorite Songs Queue maintains a sorted list of songs based on their cumulative listen time. It uses a max-heap with lazy updates for efficient ordering and provides APIs for:

- Adding songs to favorites
- Recording listen events
- Getting the top N favorite songs
- Removing songs from favorites
- Clearing all favorites data

***

## Playlist Explorer Tree

The Playlist Explorer Tree provides hierarchical classification of songs by Genre → Subgenre → Mood → Artist. It uses an n-ary tree data structure for efficient organization and retrieval:

- **Tree Structure:** N-ary tree with nodes representing classification levels
- **Traversal APIs:** Depth-first (DFS) and breadth-first (BFS) traversal methods
- **Search Functionality:** Criteria-based search by genre/subgenre/mood/artist
- **Path-based Retrieval:** Get songs by specific classification paths
- **Efficient Operations:** O(1) typical case for add/remove using path indexing

This feature enables powerful playlist exploration and organization capabilities.

***

## Smart Recommendations

The Smart Recommendations feature provides intelligent song suggestions based on play history and similarity scoring:

- **Sliding Window:** Maintains recent play history for recommendation seeding
- **Hierarchical Matching:** Finds similar songs using Playlist Explorer's classification
- **Multi-factor Scoring:** Considers genre, subgenre, mood, duration, and BPM for similarity
- **Intelligent Filtering:** Excludes recently played, skipped, and active playlist songs
- **Popular Fallback:** Returns popular songs when no similar songs are found
- **Configurable Parameters:** Adjustable thresholds and candidate limits

This feature enhances user experience by suggesting relevant songs they haven't heard recently.

***

## Artist Blocklist

The Artist Blocklist feature allows users to permanently avoid songs by certain artists across all playlists. It implements a HashSet-based blocklist for efficient O(1) membership checking:

- **HashSet Implementation:** Uses Python set for O(1) average-case membership checking
- **Artist Normalization:** Normalizes artist names for consistent matching (case-insensitive, trimmed)
- **Integration with Playlist:** Automatically checks blocklist during song addition
- **Dynamic Management:** Add, remove, and clear blocked artists at runtime
- **Return Codes:** Returns "BLOCKED_ARTIST" when attempting to add songs by blocked artists

This feature ensures users never hear from artists they've chosen to avoid, enhancing personalization.

***

## Play Duration Visualizer

The Play Duration Visualizer provides a summary of total playtime, longest song, and shortest song in a playlist. It uses aggregation logic and min/max tracking for efficient computation:

- **Total Playtime:** Computes sum of all song durations in O(n) time
- **Longest/Shortest Songs:** Identifies extreme values using linear scan with tracking
- **Formatted Output:** Presents data in human-readable format (hours/minutes/seconds)
- **Edge Cases:** Handles empty playlists and zero-duration songs gracefully
- **Integration with Dashboard:** Extends System Dashboard with new visualization methods

This feature gives users insight into their music library's time investment and content distribution.

***

## Undo Last N Playlist Edits

The Undo Last N Playlist Edits feature allows users to reverse the last N edits made to a playlist (add, delete, move operations). It implements the Command pattern with stack-based undo functionality:

- **Action Logger:** Records every playlist edit as a reversible action
- **Command Pattern:** Encapsulates actions and their undo operations
- **Stack-based Undo:** Uses a stack for O(1) push/pop operations
- **Configurable History:** Adjustable maximum history size with automatic eviction
- **Multiple Action Undo:** Undo any number of recent actions in one call

This feature enhances user experience by allowing recovery from accidental edits.

***

## Shuffle with Constraints

The Shuffle with Constraints feature shuffles a playlist such that the same artist doesn't repeat consecutively. It implements conditional rearrangement algorithms with constraint checking:

- **Constraint Checking:** Ensures no consecutive songs by the same artist
- **Reshuffle Algorithm:** Automatically retries if constraint violations occur
- **HashMap Tracking:** Efficient artist tracking for constraint validation
- **Theoretical Validation:** Checks if arrangement is theoretically possible
- **Fallback Behavior:** Simple shuffle if constrained arrangement is impossible

This feature improves playlist variety by preventing repetitive artist sequences.

***

## Merge Two Playlists Alternately

The Merge Two Playlists Alternately feature allows users to interleave two playlists in an alternating fashion (song-by-song). It implements linked list traversal and manipulation techniques:

- **Linked List Interleaving:** Takes songs from each playlist alternately to create a new merged playlist
- **Handling Unequal Lengths:** If one playlist is longer, the remaining songs are appended at the end
- **Preserves Order:** Maintains the original order of songs within each playlist
- **Efficient Implementation:** O(n + m) time complexity where n and m are the sizes of the two playlists
- **Memory Efficient:** Creates a new playlist without modifying the original playlists

This feature is useful for combining playlists from different sources while maintaining variety.

***

## Memory-Efficient Mini Player Mode

The Memory-Efficient Mini Player Mode feature is designed for low-memory devices by preloading only the next N songs while playing. It implements a sliding window approach with queue-based buffering:

- **Sliding Window:** Maintains a fixed-size queue of upcoming songs (default: 5 songs)
- **Queue-based Buffering:** Uses a circular buffer for efficient memory management
- **On-demand Loading:** Discards each song as it's played to conserve memory
- **Configurable Window Size:** Adjustable buffer size to balance memory usage and performance
- **Memory Efficiency:** O(window_size) space complexity regardless of total playlist size
- **Fast Operations:** O(1) amortized time for playing next song

This feature enables smooth playback on resource-constrained devices while maintaining a responsive user experience.

***

## Folder Structure

```
playwise_engine/
│
├── playlist/              # Problem 1: Playlist Engine modules
│   ├── playlist.py
│   ├── song.py
│   ├── artist_blocklist.py
│   ├── action_logger.py
│   ├── constrained_shuffle.py
│   ├── mini_player.py
│   └── tests/
│
├── playback_history/      # Problem 2: Playback History Stack
│   ├── playback_controller.py
│   ├── playback_engine.py
│   ├── stack.py
│   ├── skipped_tracker.py  # Recently Skipped Tracker
│   └── tests/
│
├── song_rating_tree/      # Problem 3: Rating BST
│   ├── song_rating_engine.py
│   ├── rating_bst.py
│   ├── rating_bucket.py
│   └── tests/
│
├── song_lookup_map/       # Problem 4: HashMap Lookup
│   ├── lookup_map.py
│   ├── duplicate_cleaner.py  # Duplicate Cleaner
│   └── tests/
│
├── favorites/             # Problem 10: Favorite Songs Queue
│   ├── favorite_queue.py
│   └── tests/
│
├── playlist_sorting/      # Problem 5: Time-based Sorting
│   ├── sort_engine.py
│   └── tests/
│
├── system_dashboard/      # Problem 7: Live Dashboard
│   ├── dashboard.py
│   └── tests/
│
├── explorer/              # Problem 11: Playlist Explorer Tree
│   ├── playlist_explorer.py
│   └── tests/
│
├── recommend/             # Problem 12: Smart Recommendations
│   ├── recommender.py
│   └── tests/
│
├── COMPLEXITY_ANALYSIS.md # Problem 6: Complexity documentation
├── main.py                # Master demonstration of all features
└── requirements.txt       # Install dependencies here
```

***

## Getting Started

### 1. Clone the Repository

```sh
git clone https://github.com/<your-username>/playwise_engine.git
cd playwise_engine
```

### 2. Set Up Your Virtual Environment

```sh
python -m venv venv
# On Windows
venv\Scripts\activate
# On Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

***

## How to Run (With VS Code or CLI)

From the root folder:

```sh
python main.py
```

- This runs an end-to-end demo covering all problems and features sequentially.
- Each module and feature prints its functionality—follow the on-screen output!
- The final dashboard displays live system statistics and exports JSON snapshot.

***

## Testing

Tests are written using Python's built-in `unittest` (and compatible with pytest).

To run all tests:
```sh
python -m unittest discover -s playlist/tests
python -m unittest discover -s playback_history/tests
python -m unittest discover -s song_rating_tree/tests
python -m unittest discover -s song_lookup_map/tests
python -m unittest discover -s playlist_sorting/tests
python -m unittest discover -s system_dashboard/tests
python -m unittest discover -s explorer/tests
python -m unittest discover -s recommend/tests
```

Or, to run ALL tests at once:
```sh
python -m unittest discover
```

***

## Dashboard Features

The System Snapshot Dashboard (Problem 7) provides:

- **System Overview:** Total songs, duration, average length, playback history count
- **Top 5 Longest Songs:** Sorted by duration using merge sort
- **Recently Played:** Last 5 songs from playback stack
- **Song Count by Rating:** Distribution using BST traversal
- **Extremes:** Shortest and longest songs in playlist
- **JSON Export:** Complete system snapshot for external analysis

Access the dashboard programmatically:
```python
from system_dashboard.dashboard import SystemDashboard

dashboard = SystemDashboard(playlist, playback_controller, rating_engine, lookup_map)
dashboard.print_dashboard()  # Pretty-printed console output
snapshot = dashboard.export_snapshot()  # JSON export
```

***

## Web UI Integration

The PlayWise Music Engine now includes a professional web interface built with React + TypeScript + Tailwind CSS and a FastAPI REST wrapper:

### Features
- **Dashboard:** Real-time system statistics and visualization
- **Playlists:** Manage songs with add, delete, move, and reverse operations
- **Player:** Mini-player UI with play, skip, and undo functionality
- **Explorer:** Hierarchical song exploration by genre/subgenre/mood/artist
- **Recommendations:** Smart song recommendations based on listening history
- **Favorites:** Top favorite songs ordered by listen time
- **Settings:** Configure deduplication policy and skipped tracker capacity

### Tech Stack
- **Frontend:** React + TypeScript + Tailwind CSS
- **Backend API:** FastAPI REST wrapper
- **Deployment:** Docker + docker-compose

### Running the Application

#### Option 1: Using Docker Compose (Recommended)
```bash
docker-compose up --build
```

Then visit:
- Web UI: http://localhost:3000
- API Docs: http://localhost:8000/docs

#### Option 2: Running Locally

**API Server:**
```bash
cd api
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

**Web Client:**
```bash
cd web
npm install
npm run dev
```

Then visit:
- Web UI: http://localhost:3000
- API Docs: http://localhost:8000/docs

### API Endpoints

The FastAPI wrapper exposes the following endpoints:

- `GET /health` - Health check
- `GET /playlists` - List playlists (id, name, length)
- `GET /playlists/{playlist_id}` - Get playlist details (ordered list of songs)
- `POST /playlists/{playlist_id}/songs` - Add song to playlist (body: title, artist, duration) -> returns song_id or error (honor duplicate-cleaner policy)
- `DELETE /playlists/{playlist_id}/songs/{index}` - Delete song by index
- `POST /playlists/{playlist_id}/move` - Move song between indices (body: {from_index, to_index})
- `POST /playlists/{playlist_id}/reverse` - Reverse playlist
- `POST /playback/play` - Play song (body: {playlist_id, index?}) -> triggers play and returns song metadata
- `POST /playback/skip` - Skip song (body: {song_id, playlist_id?}) -> skip and record in RecentlySkippedTracker
- `POST /history/undo` - Undo last play
- `GET /snapshot` - Get system snapshot (export_snapshot() JSON)
- `GET /explorer/search` - Search songs by criteria (query params for genre, subgenre, mood, artist) -> returns song list
- `GET /recommend` - Get recommendations using default params -> returns list
- `GET /favorites/top?n=10` - Get top favorites from FavoriteQueue -> return top favorites

### Development

Use the provided Makefile for common development tasks:

```bash
make dev        # Run development environment
make build      # Build docker images
make up         # Start services
make down       # Stop services
make logs       # View logs
make test-api   # Run API tests
```


## Contributing

Pull requests and improvements are welcome! This project serves as an educational resource for:
- Data Structures and Algorithms courses
- Hackathon preparation
- System design practice
- Performance optimization learning
