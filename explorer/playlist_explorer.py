"""
Playlist Explorer module for PlayWise Music Engine.

Implements an n-ary tree that classifies songs hierarchically by Genre → Subgenre → Mood → Artist.
Provides traversal APIs (DFS/BFS) and search functionality.
"""

import re
from typing import Dict, Set, List, Optional, Generator, Callable, Any
from collections import deque


def normalize_text(text: str) -> str:
    """
    Normalize text by stripping, converting to lowercase, and collapsing whitespace.
    
    Args:
        text (str): Text to normalize
        
    Returns:
        str: Normalized text
    """
    if not text:
        return ""
    # Strip whitespace, convert to lowercase, and collapse multiple spaces to single space
    return re.sub(r'\s+', ' ', text.strip().lower())


class ExplorerNode:
    """
    Node in the Playlist Explorer tree.
    
    Each node represents a classification level (Genre/Subgenre/Mood/Artist) and contains:
    - A key identifying the node
    - Children nodes for further classification
    - A set of song_ids that belong exactly at this node
    """
    
    def __init__(self, key: str):
        """
        Initialize an ExplorerNode.
        
        Args:
            key (str): The key identifying this node (e.g., "Rock", "Alternative", "Melancholic", "Radiohead")
        """
        self.key = key
        self.children: Dict[str, 'ExplorerNode'] = {}
        self.songs: Set[str] = set()


class PlaylistExplorer:
    """
    Playlist Explorer Tree that classifies songs hierarchically.
    
    Classification hierarchy: Genre → Subgenre → Mood → Artist
    Uses an n-ary tree representation with DFS/BFS traversal capabilities.
    
    Time Complexity:
        - add_song: O(depth) ~ O(1) per add (small constant depth)
        - remove_song: O(N) where N is the number of nodes (with reverse map O(1))
        - get_by_path: O(depth) ~ O(1)
        - traverse: O(N) where N is the number of nodes
        - search: O(N) in worst case, but typically much faster with pruning
    
    Space Complexity:
        - O(N + S) where N is the number of nodes and S is the number of songs
    """
    
    def __init__(self):
        """Initialize the Playlist Explorer with an empty root node."""
        # Root node with empty key
        self.root = ExplorerNode("")
        # Reverse map: song_id -> list of node paths for efficient removal
        self.song_to_paths: Dict[str, List[List[str]]] = {}
    
    def add_song(self, song_id: str, genre: str, subgenre: Optional[str] = None, 
                 mood: Optional[str] = None, artist: str = "") -> None:
        """
        Add a song to the explorer tree following the hierarchy: genre -> subgenre -> mood -> artist.
        
        Time Complexity: O(depth) ~ O(1) per add (small constant depth)
        Space Complexity: O(1) additional space
        
        Args:
            song_id (str): Unique identifier for the song
            genre (str): Genre of the song
            subgenre (Optional[str]): Subgenre of the song
            mood (Optional[str]): Mood of the song
            artist (str): Artist of the song
        """
        # Normalize all strings
        norm_genre = normalize_text(genre)
        norm_subgenre = normalize_text(subgenre) if subgenre else ""
        norm_mood = normalize_text(mood) if mood else ""
        norm_artist = normalize_text(artist)
        
        # Build the path
        path = [norm_genre]
        if norm_subgenre:
            path.append(norm_subgenre)
        if norm_mood:
            path.append(norm_mood)
        if norm_artist:
            path.append(norm_artist)
        
        # Traverse/create nodes along the path
        current_node = self.root
        for key in path:
            if key not in current_node.children:
                current_node.children[key] = ExplorerNode(key)
            current_node = current_node.children[key]
        
        # Add song to the final node
        current_node.songs.add(song_id)
        
        # Update reverse map
        if song_id not in self.song_to_paths:
            self.song_to_paths[song_id] = []
        self.song_to_paths[song_id].append(path)
    
    def remove_song(self, song_id: str) -> None:
        """
        Remove a song from all nodes in the explorer tree.
        
        Time Complexity: O(P * depth) where P is the number of paths for this song
        Space Complexity: O(1) additional space
        
        Args:
            song_id (str): Unique identifier for the song to remove
        """
        if song_id not in self.song_to_paths:
            return
        
        # Remove song from all nodes where it's stored
        for path in self.song_to_paths[song_id]:
            current_node = self.root
            # Traverse to the node
            for key in path:
                if key in current_node.children:
                    current_node = current_node.children[key]
                else:
                    # Path doesn't exist, skip
                    break
            else:
                # Reached the target node, remove song
                current_node.songs.discard(song_id)
        
        # Remove from reverse map
        del self.song_to_paths[song_id]
    
    def get_by_path(self, path: List[str], include_subtree: bool = False) -> Set[str]:
        """
        Get all songs at a specific path in the explorer tree.
        
        Time Complexity: O(S + C) where S is songs at node and C is children nodes (if include_subtree)
        Space Complexity: O(S + C) for the returned set
        
        Args:
            path (List[str]): Path to the node (e.g., ["rock", "alternative", "melancholic"])
            include_subtree (bool): Whether to include songs from subtree nodes
            
        Returns:
            Set[str]: Set of song_ids at the specified path
        """
        # Normalize the path
        norm_path = [normalize_text(key) for key in path]
        
        # Traverse to the node
        current_node = self.root
        for key in norm_path:
            if key in current_node.children:
                current_node = current_node.children[key]
            else:
                # Path doesn't exist
                return set()
        
        # Collect songs
        result = set(current_node.songs)
        
        # Include subtree if requested
        if include_subtree:
            # BFS traversal of subtree
            queue = deque([current_node])
            while queue:
                node = queue.popleft()
                result.update(node.songs)
                queue.extend(node.children.values())
        
        return result
    
    def traverse(self, method: str = 'dfs', callback: Optional[Callable[[List[str], ExplorerNode], Any]] = None) -> Generator[tuple, None, None]:
        """
        Traverse the explorer tree using DFS or BFS.
        
        Time Complexity: O(N) where N is the number of nodes
        Space Complexity: O(depth) for DFS, O(max_width) for BFS
        
        Args:
            method (str): Traversal method ('dfs' or 'bfs')
            callback (Optional[Callable]): Optional callback to process each node
            
        Yields:
            tuple: (path, node) for each node in the tree
        """
        if method.lower() == 'bfs':
            # BFS traversal
            queue = deque([([], self.root)])  # (path, node)
            while queue:
                path, node = queue.popleft()
                # Call callback if provided
                if callback:
                    callback(path, node)
                # Yield the node
                yield (path, node)
                # Add children to queue
                for key, child in node.children.items():
                    queue.append((path + [key], child))
        else:
            # DFS traversal (default)
            stack = [([], self.root)]  # (path, node)
            while stack:
                path, node = stack.pop()
                # Call callback if provided
                if callback:
                    callback(path, node)
                # Yield the node
                yield (path, node)
                # Add children to stack (in reverse order to maintain left-to-right traversal)
                for key, child in reversed(list(node.children.items())):
                    stack.append((path + [key], child))
    
    def search(self, criteria: Dict[str, Optional[str]]) -> Set[str]:
        """
        Search for songs matching the given criteria.
        
        Time Complexity: O(N) in worst case, but typically much faster with pruning
        Space Complexity: O(S) where S is the number of matching songs
        
        Args:
            criteria (Dict[str, Optional[str]]): Search criteria with keys:
                - genre: Genre to match
                - subgenre: Subgenre to match (optional)
                - mood: Mood to match (optional)
                - artist: Artist to match (optional)
                Any value can be None to match any value at that level.
            
        Returns:
            Set[str]: Set of song_ids matching the criteria
        """
        # Normalize criteria
        norm_criteria = {}
        for key, value in criteria.items():
            if value is not None:
                norm_criteria[key] = normalize_text(value)
        
        # If no criteria provided, return empty set
        if not norm_criteria:
            return set()
        
        # Start from root
        current_node = self.root
        
        # Navigate down the tree based on criteria
        if 'genre' in norm_criteria:
            genre_key = norm_criteria['genre']
            if genre_key not in current_node.children:
                return set()
            current_node = current_node.children[genre_key]
            
            if 'subgenre' in norm_criteria:
                subgenre_key = norm_criteria['subgenre']
                if subgenre_key not in current_node.children:
                    return set()
                current_node = current_node.children[subgenre_key]
                
                if 'mood' in norm_criteria:
                    mood_key = norm_criteria['mood']
                    if mood_key not in current_node.children:
                        return set()
                    current_node = current_node.children[mood_key]
                    
                    if 'artist' in norm_criteria:
                        artist_key = norm_criteria['artist']
                        if artist_key not in current_node.children:
                            return set()
                        current_node = current_node.children[artist_key]
        
        # Collect all songs under the matching node (including subtree)
        result = set()
        queue = deque([current_node])
        while queue:
            node = queue.popleft()
            result.update(node.songs)
            queue.extend(node.children.values())
        
        return result