# **COMPLEXITY_ANALYSIS.md**

# PlayWise Music Engine - Space-Time Complexity Analysis

**Problem 6: Playback Optimization using Space-Time Analysis**

This document provides a comprehensive analysis of time and space complexity for all core methods across the PlayWise system (Problems 1-5), along with optimization recommendations.

---

## **Table of Contents**
1. [Problem 1: Playlist Engine](#problem-1-playlist-engine)
2. [Problem 2: Playback History](#problem-2-playback-history)
3. [Problem 3: Song Rating Tree](#problem-3-song-rating-tree)
4. [Problem 4: Song Lookup Map](#problem-4-song-lookup-map)
5. [Problem 5: Time-based Sorting](#problem-5-time-based-sorting)
6. [Problem 8: Recently Skipped Tracker](#problem-8-recently-skipped-tracker)
7. [Problem 9: Duplicate Cleaner](#problem-9-duplicate-cleaner)
8. [Problem 10: Favorite Songs Queue](#problem-10-favorite-songs-queue)
9. [Problem 11: Playlist Explorer Tree](#problem-11-playlist-explorer-tree)
10. [Problem 12: Smart Recommendations](#problem-12-smart-recommendations)
11. [Problem 13: Artist Blocklist](#problem-13-artist-blocklist)
12. [Problem 14: Play Duration Visualizer](#problem-14-play-duration-visualizer)
13. [System-wide Summary](#system-wide-summary)
14. [Optimization Recommendations](#optimization-recommendations)

***

## **Problem 1: Playlist Engine**

### **DoublyLinkedList Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `add_song(song)` | **O(1)** | **O(1)** | Append to tail using tail pointer; constant pointer manipulation |
| `delete_song(index)` | **O(n)** | **O(1)** | Must traverse to index position (n/2 on average), then unlink node |
| `move_song(from_idx, to_idx)` | **O(n)** | **O(1)** | Traverse to both positions, extract and reinsert node |
| `reverse_playlist()` | **O(n)** | **O(1)** | Iterate through all nodes, swap prev/next pointers |
| `get_all_songs()` | **O(n)** | **O(n)** | Traverse entire list, create new list of songs |

**Analysis:**
- **Strengths:** O(1) insertion at head/tail makes adding songs very efficient
- **Bottlenecks:** Index-based operations require traversal (no random access)
- **Memory:** In-place operations minimize extra space usage

### **Playlist Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `add_song(title, artist, duration)` | **O(1)** | **O(1)** | Creates Song object, delegates to DoublyLinkedList |
| `delete_song(index)` | **O(n)** | **O(1)** | Delegates to DoublyLinkedList.delete_song() |
| `move_song(from_idx, to_idx)` | **O(n)** | **O(1)** | Delegates to DoublyLinkedList.move_song() |
| `reverse_playlist()` | **O(n)** | **O(1)** | Delegates to DoublyLinkedList.reverse_playlist() |
| `get_all_songs()` | **O(n)** | **O(n)** | Delegates to DoublyLinkedList.get_all_songs() |

---

## **Problem 2: Playback History**

### **PlaybackHistory Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `push(song)` | **O(1)** | **O(1)** | Python list append is amortized O(1) |
| `pop()` | **O(1)** | **O(1)** | Remove and return last element from list |
| `peek()` | **O(1)** | **O(1)** | Access last element without removal |
| `is_empty()` | **O(1)** | **O(1)** | Check if length is zero |

**Analysis:**
- **Optimal:** All stack operations run in constant time
- **Memory:** Stack grows linearly with playback history; consider maximum size limit for production

### **PlaybackController Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `play_song(title, artist, duration)` | **O(1)** | **O(1)** | Add to playlist (O(1)) + push to stack (O(1)) |
| `undo_last_play()` | **O(1)** | **O(1)** | Pop from stack (O(1)) |
| `get_playlist_songs()` | **O(n)** | **O(n)** | Delegates to playlist.get_all_songs() |

***

## **Problem 3: Song Rating Tree**

### **RatingBucket Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `add_song(song)` | **O(1)** | **O(1)** | Append song to internal list |
| `remove_song(song_id)` | **O(m)** | **O(1)** | Linear search through m songs in bucket, then remove |
| `get_songs()` | **O(m)** | **O(m)** | Return copy of all m songs in bucket |

*where m = number of songs in this rating bucket*

### **BSTNode Class**
- No operations; just data structure

### **RatingBST Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `insert_song(song, rating)` | **O(log n)** avg<br>**O(n)** worst | **O(log n)** recursion | Binary search to find rating node, insert if not exists |
| `search_by_rating(rating)` | **O(log n)** avg<br>**O(n)** worst | **O(log n)** recursion | Binary search traversal to rating node |
| `delete_song(song_id)` | **O(n·m)** | **O(log n)** recursion | Must search all nodes (n) and within buckets (m) |

*where n = number of rating nodes, m = avg songs per rating*

**Analysis:**
- **Best Case:** Balanced tree with O(log n) search/insert
- **Worst Case:** Unbalanced tree degenerates to O(n) (linked list behavior)
- **Optimization Needed:** Consider self-balancing BST (AVL, Red-Black) for guaranteed O(log n)

### **SongRatingEngine Class**
- Delegates to RatingBST; same complexities

***

## **Problem 4: Song Lookup Map**

### **SongLookupMap Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `add_song(song)` | **O(1)** avg<br>**O(n)** worst | **O(1)** | Dictionary insertion; worst case with hash collisions |
| `remove_song(song_id)` | **O(1)** avg<br>**O(n)** worst | **O(1)** | Dictionary deletion from both maps |
| `lookup_song_by_id(song_id)` | **O(1)** avg<br>**O(n)** worst | **O(1)** | Dictionary key lookup |
| `lookup_song_by_title(title)` | **O(1)** avg<br>**O(n)** worst | **O(1)** | Dictionary key lookup |

**Analysis:**
- **Optimal Performance:** Python's dict uses efficient hashing with O(1) average
- **Collision Handling:** Python handles collisions internally; worst case rarely occurs
- **Memory Trade-off:** Maintains two dictionaries for dual-key access (2× space)
- **Scalability:** Excellent for large datasets; ideal for instant search

---

## **Problem 5: Time-based Sorting**

### **SortCriteria Class**
- Enum/constants; no operations

### **SortEngine Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `merge_sort(songs, criteria)` | **O(n log n)** | **O(n)** | Divide-and-conquer; creates temporary sublists |
| `_merge(left, right, criteria)` | **O(n)** | **O(n)** | Merge two sorted lists into one |
| `_compare(song_a, song_b, criteria)` | **O(1)** | **O(1)** | Simple attribute comparison |

**Analysis:**
- **Consistent Performance:** O(n log n) in all cases (best, average, worst)
- **Stability:** Merge sort preserves relative order of equal elements
- **Memory Cost:** Requires O(n) auxiliary space for merging
- **Alternative:** Could use in-place quicksort for O(log n) space, but loses stability

***

## **Problem 8: Recently Skipped Tracker**

### **RecentlySkippedTracker Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `skip_song(song_id)` | **O(1)** amortized | **O(1)** | Add to deque and set; automatic eviction |
| `is_recently_skipped(song_id)` | **O(1)** average | **O(1)** | Set membership check |
| `get_recently_skipped()` | **O(k)** | **O(k)** | Convert deque to list where k ≤ capacity |
| `clear_skipped()` | **O(1)** amortized | **O(1)** | Clear deque and set |
| `set_capacity(cap)` | **O(min(current, new))** | **O(min(current, new))** | Truncate if needed, recreate data structures |

*where k = number of tracked songs, capacity = maximum tracked songs (default 10)*

**Analysis:**
- **Optimal Performance:** All operations are O(1) except listing which is O(k)
- **Memory Efficiency:** Fixed space bound of O(capacity)
- **Automatic Eviction:** Deque with maxlen automatically handles FIFO eviction
- **Fast Lookups:** Set provides O(1) average case membership testing

**Benefits:**
- Prevents repetitive playback of skipped songs during autoplay
- Minimal performance impact on playback operations
- Configurable capacity for different use cases
- Thread-safe for single-operation access patterns

***

## **Problem 9: Duplicate Cleaner**

### **DuplicateCleaner Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `is_duplicate(title, artist)` | **O(1)** average | **O(1)** | Hash lookup with normalized composite key |
| `register(song_id, title, artist)` | **O(1)** average | **O(1)** | Hash insertion with normalized composite key |
| `deregister(song_id, title, artist)` | **O(1)** average | **O(1)** | Hash deletion with normalized composite key |
| `cleanup_on_add(song_obj)` | **O(1)** average | **O(1)** | Composite of is_duplicate + register operations |

**Analysis:**
- **Efficient Detection:** O(1) average case duplicate detection using composite key hashing
- **Normalization:** Strip, lowercase, and collapse whitespace for robust matching
- **Policy Support:** Handles both 'first' and 'latest' duplicate resolution policies
- **Memory Efficient:** O(S) space where S is the number of unique songs

**Benefits:**
- Automatic prevention of duplicate songs in catalogs and playlists
- Configurable policies for handling duplicates
- Minimal performance impact on song addition operations
- Robust text normalization for reliable matching

***

## **Problem 10: Favorite Songs Queue**

### **FavoriteQueue Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `add_to_favorites(song_id, title, artist)` | **O(1)** | **O(1)** | Dict insertion |
| `remove_from_favorites(song_id)` | **O(1)** | **O(1)** | Dict deletion |
| `record_listen(song_id, delta_seconds)` | **O(log m)** | **O(1)** amortized | Heap push operation where m = favorite songs |
| `get_top_n(n)` | **O(n log m)** amortized | **O(n)** | Heap pops with lazy update filtering |
| `clear()` | **O(1)** | **O(1)** | Clear all dicts and heap |

*where m = number of favorite songs*

**Algorithm Choice:**
- **Max-Heap with Lazy Updates:** Efficient ordering maintenance with stale entry filtering
- **Dual Data Structures:** Dict for O(1) lookups + heap for ordering
- **Lazy Deletion:** Avoid costly removal operations by filtering stale entries on access

**Analysis:**
- **Efficient Updates:** O(log m) for listen recordings with automatic ordering
- **Lazy Filtering:** Amortized cost for top-N queries with stale entry handling
- **Memory Bounded:** O(m) space where m is the number of favorite songs
- **Scalable:** Efficient for both small and large favorite lists

**Benefits:**
- Real-time favorite song ranking by listen time
- Efficient updates without full resorting
- Configurable top-N queries
- Automatic handling of stale data through lazy updates

***

## **System-wide Summary**

### **Overall Operation Complexity Table**

| Operation | Data Structure | Time (Best) | Time (Avg) | Time (Worst) | Space |
|-----------|---------------|-------------|------------|--------------|-------|
| Add song | DoublyLinkedList | O(1) | O(1) | O(1) | O(1) |
| Delete by index | DoublyLinkedList | O(1) | O(n) | O(n) | O(1) |
| Move song | DoublyLinkedList | O(n) | O(n) | O(n) | O(1) |
| Reverse playlist | DoublyLinkedList | O(n) | O(n) | O(n) | O(1) |
| Playback undo | Stack | O(1) | O(1) | O(1) | O(1) |
| Insert by rating | BST | O(log n) | O(log n) | O(n) | O(log n) |
| Search by rating | BST | O(log n) | O(log n) | O(n) | O(log n) |
| Lookup by ID/title | HashMap | O(1) | O(1) | O(n) | O(1) |
| Sort playlist | Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) |
| Skip song tracking | Circular Buffer | O(1) | O(1) | O(1) | O(10) |
| Duplicate detection | Composite Hash | O(1) | O(1) | O(n) | O(S) |
| Favorite ranking | Max-Heap | O(log m) | O(log m) | O(log m) | O(m) |
| Add to explorer | N-ary Tree | O(depth) | O(depth) | O(depth) | O(1) |
| Search explorer | N-ary Tree | O(1) | O(bucket_size) | O(N) | O(S) |
| Recommend songs | Sliding Window + Scoring | O(1) | O(k × M log N) | O(k × M log N) | O(N) |
| Artist blocklist check | HashSet | O(1) | O(1) | O(n) | O(n) |
| Play duration visualization | Aggregation + Min/Max | O(n) | O(n) | O(n) | O(1) |

***

## **Optimization Recommendations**

### **1. Lazy Reversal (DoublyLinkedList)**
**Current:** O(n) — physically swap all prev/next pointers  
**Optimized:** O(1) — toggle boolean flag, adjust traversal direction  

**Implementation:**
```python
# Maintain a reversed flag
self.is_reversed = False

def reverse_playlist(self):
    # Just flip the flag instead of physically reversing
    self.is_reversed = not self.is_reversed
    # Swap head and tail conceptually
    self.head, self.tail = self.tail, self.head
```

**Benefits:** 
- Instant reversal regardless of playlist size
- Traversal methods respect the flag

***

### **2. Size Caching (DoublyLinkedList)**
**Current:** O(n) — traverse entire list to count  
**Optimized:** O(1) — maintain size counter  

**Implementation:**
```python
self._size = 0

def add_song(self, song):
    # ... add logic ...
    self._size += 1

def delete_song(self, index):
    # ... delete logic ...
    self._size -= 1

def size(self):
    return self._size  # O(1) instead of O(n)
```

***

### **3. Balanced BST (RatingBST)**
**Current:** O(n) worst case for unbalanced tree  
**Optimized:** O(log n) guaranteed with AVL or Red-Black tree  

**Recommendation:**
- Implement self-balancing after insertions/deletions
- Or use library: `sortedcontainers.SortedDict` for production

***

### **4. Index Optimization (DoublyLinkedList)**
**Current:** O(n) for index-based access  
**Consideration:** 
- If frequent random access needed, consider hybrid: list of nodes
- Trade-off: More memory for O(1) index access

---

### **5. History Size Limit (PlaybackHistory)**
**Current:** Unlimited stack growth  
**Optimized:** Cap at maximum history size (e.g., 100 songs)  

**Implementation:**
```python
MAX_HISTORY = 100

def push(self, song):
    if len(self.history_stack) >= MAX_HISTORY:
        self.history_stack.pop(0)  # Remove oldest
    self.history_stack.append(song)
```

***

### **6. Skipped Tracker Persistence**
**Current:** In-memory only  
**Consideration:** For cross-session persistence, consider:
- Local storage (SQLite, pickle file)
- Redis for distributed systems
- Periodic snapshotting for recovery

**Implementation Note:**
```python
# TODO: Add persistence layer for cross-session skipped song tracking
# Consider using pickle, SQLite, or Redis for persistent storage
```

***

### **7. Duplicate Cleaner Persistence**
**Current:** In-memory only  
**Consideration:** For cross-session persistence, consider:
- Local storage (SQLite, pickle file)
- Redis for distributed systems
- Periodic snapshotting for recovery

**Implementation Note:**
```python
# TODO: Add persistence layer for cross-session duplicate tracking
# Consider using pickle, SQLite, or Redis for persistent storage
```

***

### **8. Favorite Queue Persistence**
**Current:** In-memory only  
**Consideration:** For cross-session persistence, consider:
- Local storage (SQLite, pickle file)
- Redis for distributed systems
- Periodic snapshotting for recovery

**Implementation Note:**
```python
# TODO: Add persistence layer for cross-session favorite tracking
# Consider using pickle, SQLite, or Redis for persistent storage
```

***

## **Problem 11: Playlist Explorer Tree**

### **PlaylistExplorer Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `add_song(song_id, genre, subgenre, mood, artist)` | **O(depth)** ~ **O(1)** | **O(1)** | Walk/create nodes for genre -> subgenre -> mood -> artist, add song to leaf node |
| `remove_song(song_id)` | **O(P × depth)** | **O(1)** | Remove song from all P paths where it's stored using reverse map |
| `get_by_path(path, include_subtree)` | **O(S + C)** | **O(S + C)** | Retrieve songs at specific path; S=songs at node, C=children nodes if include_subtree |
| `traverse(method, callback)` | **O(N)** | **O(depth)** for DFS, **O(max_width)** for BFS | Full tree traversal using DFS or BFS |
| `search(criteria)` | **O(N)** worst case | **O(S)** | Search songs matching criteria; typically faster with pruning |

**Analysis:**
- **Efficient Operations:** O(1) typical case for add/remove using path-based indexing
- **Flexible Retrieval:** Multiple traversal and search methods for different use cases
- **Hierarchical Organization:** Natural classification by genre/subgenre/mood/artist hierarchy
- **Memory Efficient:** Shared nodes for common prefixes, songs stored only at leaf-most nodes

***

## **Problem 12: Smart Recommendations**

### **SmartRecommender Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `record_play(song_id, played_at, play_duration, metadata)` | **O(1)** | **O(1)** | Add to sliding window and played set, update listen time |
| `recommend(seed_count, top_n, exclude_active_playlist)` | **O(k × M log N)** | **O(N)** | k=seeds, M=candidates per seed, N=top_n recommendations |
| `_get_similar_songs(seed_song_id)` | **O(bucket_size)** | **O(M)** | Retrieve similar songs via PlaylistExplorer search |
| `_calculate_similarity_score(seed_id, candidate_id)` | **O(1)** | **O(1)** | Compute weighted similarity score based on attributes |
| `get_popular_songs(exclude_recent, exclude_skipped, top_n)` | **O(S log S)** | **O(N)** | Sort songs by listen time; S=total songs, N=top_n |

**Analysis:**
- **Fast Recording:** O(1) play recording enables real-time recommendation updates
- **Scalable Recommendations:** Bounded complexity with configurable caps on seeds and candidates
- **Rich Similarity:** Multi-factor scoring with genre, subgenre, mood, duration, and BPM
- **Effective Filtering:** Exclude recently played, skipped, and active playlist songs
- **Fallback Strategy:** Popular songs recommendation when no similar songs found

***

## **Problem 13: Artist Blocklist**

### **ArtistBlocklist Class**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `add_artist(artist)` | **O(1)** average | **O(1)** | Add to internal set with normalized artist name |
| `remove_artist(artist)` | **O(1)** average | **O(1)** | Remove from internal set with normalized artist name |
| `is_blocked(artist)` | **O(1)** average | **O(1)** | Set membership check with normalized artist name |
| `get_blocked_artists()` | **O(n)** | **O(n)** | Return copy of all blocked artists where n = blocked count |
| `clear()` | **O(1)** amortized | **O(1)** | Clear internal set |

**Analysis:**
- **Optimal Performance:** All operations are O(1) average case using Python's set implementation
- **Normalization:** Artist names are normalized (stripped, lowercased) for consistent matching
- **Memory Efficiency:** O(n) space where n is the number of blocked artists
- **Scalability:** Excellent for large blocklists; ideal for instant checking

**Benefits:**
- Permanent exclusion of songs by specific artists across all playlists
- Minimal performance impact on song addition operations
- Configurable blocklist management with add/remove/clear operations
- Case-insensitive and whitespace-tolerant artist matching

***

## **Problem 14: Play Duration Visualizer**

### **SystemDashboard Class (Extended)**

| Method | Time Complexity | Space Complexity | Explanation |
|--------|----------------|------------------|-------------|
| `get_play_duration_visualization()` | **O(n)** | **O(1)** | Aggregate durations, find min/max across all songs |
| `print_play_duration_visualization()` | **O(n)** | **O(1)** | Call visualization method and format output |

**Analysis:**
- **Efficient Aggregation:** Single pass through playlist for total duration calculation
- **Min/Max Tracking:** Linear scan to identify shortest and longest songs
- **Memory Efficient:** O(1) additional space for computation
- **Scalability:** Linear time complexity scales well with playlist size

**Benefits:**
- Instant summary of playlist time investment
- Identification of content extremes (shortest/longest songs)
- Human-readable formatted output for user consumption
- Integrated with existing dashboard infrastructure

***

## **Key Takeaways**

1. **Know Your Data Structures:** Each has trade-offs between time and space
2. **Analyze Before Optimizing:** Profile to find actual bottlenecks
3. **Document Complexity:** Makes maintenance and scaling decisions clear
4. **Consider Use Cases:** Optimize for common operations, not edge cases
5. **Space-Time Trade-offs:** Sometimes using more memory saves time (and vice versa)

***

## **Conclusion**

This analysis demonstrates that the PlayWise system uses appropriate data structures for each problem:
- **O(1) operations** where speed is critical (add, undo, lookup)
- **O(log n) search** with BST for rating organization
- **O(n log n) sorting** with stable merge sort
- **O(1) tracking** with circular buffer for skipped songs
- **O(1) duplicate detection** with composite key hashing
- **O(log m) favorite ranking** with max-heap and lazy updates
- **O(depth) hierarchical classification** with n-ary tree for playlist exploration
- **O(k × M log N) intelligent recommendations** with sliding window and similarity scoring

Future optimizations should focus on:
- Lazy evaluation techniques
- Self-balancing trees
- Caching frequently accessed data
- Memory limits for unbounded growth
- Persistence for stateful features like skipped tracking, duplicate tracking, and favorites

**Engineering Mindset:** Always annotate complexity, measure performance, and optimize intelligently based on real-world usage patterns.

---

**Prepared by:** SALA ANIL KUMAR