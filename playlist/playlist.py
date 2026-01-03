from .playlist_engine import DoublyLinkedList, Node
from .song import Song
from song_lookup_map.lookup_map import SongLookupMap
from .artist_blocklist import ArtistBlocklist
from .action_logger import ActionLogger
from .constrained_shuffle import ConstrainedShuffler
from typing import Optional, List


class Playlist:
    """
    Wrapper around DoublyLinkedList with artist blocklist support and undo functionality.
    """
    def __init__(self, enable_dedupe: bool = True, dedupe_policy: str = 'first', max_undo_history: int = 50):
        self.playlist = DoublyLinkedList()
        self.lookup_map = SongLookupMap(enable_dedupe=enable_dedupe, dedupe_policy=dedupe_policy)
        self.artist_blocklist = ArtistBlocklist()
        self.action_logger = ActionLogger(max_history=max_undo_history)
        self.constrained_shuffler = ConstrainedShuffler()

    def add_song(self, title: str, artist: str, duration: int, genre=None, song_id=None) -> Optional[str]:
        """
        Add a song to the playlist.
        
        Args:
            title (str): Song title
            artist (str): Song artist
            duration (int): Song duration in seconds
            genre: Song genre (optional)
            song_id: Song ID (optional)
            
        Returns:
            Optional[str]: None if song added successfully, existing song_id if duplicate and policy is 'first'
        """
        # Check if artist is blocked
        if self.artist_blocklist.is_blocked(artist):
            return "BLOCKED_ARTIST"
        
        song = Song(title, artist, duration, song_id=song_id, genre=genre)
        # Try to add to lookup map (handles deduplication)
        duplicate_result = self.lookup_map.add_song(song)
        if duplicate_result is not None:
            # Duplicate found and policy is 'first', reject the new song
            return duplicate_result
        
        # Store the current size to know the index of the new song
        index = self.playlist.size
        
        # Add to playlist
        self.playlist.add_song(song)
        
        # Log action for undo
        def undo_add():
            self.delete_song(index)
        self.action_logger.log_action("add", undo_add)
        
        return None

    def add_existing_song(self, song: Song) -> Optional[str]:
        """
        Add an existing song object to the playlist.
        
        Args:
            song (Song): Song object to add
            
        Returns:
            Optional[str]: None if song added successfully, existing song_id if duplicate and policy is 'first'
        """
        # Check if artist is blocked
        if self.artist_blocklist.is_blocked(song.artist):
            return "BLOCKED_ARTIST"
        
        # Try to add to lookup map (handles deduplication)
        duplicate_result = self.lookup_map.add_song(song)
        if duplicate_result is not None:
            # Duplicate found and policy is 'first', reject the new song
            return duplicate_result
        
        # Add to playlist
        self.playlist.add_song(song)
        return None

    def delete_song(self, index: int) -> bool:
        """
        Delete a song from the playlist by index.
        
        Args:
            index (int): Index of song to delete
            
        Returns:
            bool: True if successful, False if index out of bounds
            
        Raises:
            IndexError: If index is out of bounds (for backward compatibility with tests)
        """
        # First get the song to get its ID for lookup map removal
        if index < 0 or index >= self.playlist.size:
            raise IndexError("Index out of bounds")
            
        # Navigate to the node
        current = self.playlist.head
        for _ in range(index):
            current = current.next
            
        # Store song info for undo
        song = current.song
        song_id = song.song_id
            
        # Remove from lookup map
        if song_id is not None:
            self.lookup_map.remove_song(song_id)
            
        # Remove from playlist
        self.playlist.delete_song(index)
        
        # Log action for undo
        def undo_delete():
            # Recreate the song object
            restored_song = Song(song.title, song.artist, song.duration, song_id=song_id, genre=getattr(song, 'genre', None))
            # Add it back at the same index
            self._insert_song_at_index(restored_song, index)
        self.action_logger.log_action("delete", undo_delete)
        
        return True

    def move_song(self, from_index: int, to_index: int):
        self.playlist.move_song(from_index, to_index)
        # Log action for undo
        def undo_move():
            self.playlist.move_song(to_index, from_index)
        self.action_logger.log_action("move", undo_move)

    def reverse_playlist(self):
        self.playlist.reverse_playlist()
        # Log action for undo
        def undo_reverse():
            self.playlist.reverse_playlist()
        self.action_logger.log_action("reverse", undo_reverse)

    def get_all_songs(self):
        songs = []
        node = self.playlist.head
        while node:
            songs.append(node.song)
            node = node.next
        return songs

    def is_empty(self):
        return self.playlist.head is None

    def pop_next(self):
        if self.playlist.head is None:
            return None
        s = self.playlist.head.song
        # Remove from lookup map
        if s.song_id is not None:
            self.lookup_map.remove_song(s.song_id)
        self.playlist.delete_song(0)
        return s
    
    def _insert_song_at_index(self, song: Song, index: int):
        """
        Insert a song at a specific index in the playlist.
        
        Args:
            song (Song): Song to insert
            index (int): Index to insert at
        """
        # Add to lookup map
        self.lookup_map.add_song(song)
        
        # Handle special cases
        if index == 0:
            # Insert at head
            new_node = Node(song)
            new_node.next = self.playlist.head
            if self.playlist.head:
                self.playlist.head.prev = new_node
            self.playlist.head = new_node
            if self.playlist.tail is None:
                self.playlist.tail = new_node
        elif index >= self.playlist.size:
            # Append to tail
            self.playlist.add_song(song)
            return
        else:
            # Insert in middle
            current = self.playlist.head
            for _ in range(index):
                current = current.next
            new_node = Node(song)
            new_node.prev = current.prev
            new_node.next = current
            if current.prev:
                current.prev.next = new_node
            else:
                self.playlist.head = new_node
            current.prev = new_node
        
        self.playlist.size += 1
    
    def undo_last_n_actions(self, n: int) -> List[str]:
        """
        Undo the last N playlist edits.
        
        Time Complexity: O(n) where n is the number of actions to undo
        Space Complexity: O(n) for the result list
        
        Args:
            n (int): Number of actions to undo
            
        Returns:
            List[str]: List of action types that were undone
        """
        return self.action_logger.undo_last_n_actions(n)
    
    def shuffle_with_artist_constraints(self) -> List[Song]:
        """
        Shuffle the playlist with constraints to prevent consecutive artists.
        
        Time Complexity: O(n) average case
        Space Complexity: O(n)
        
        Returns:
            List[Song]: Shuffled list of songs with no consecutive artists
        """
        songs = self.get_all_songs()
        shuffled_songs = self.constrained_shuffler.shuffle_with_constraints(songs)
        
        # Update the playlist with the shuffled order
        # First clear the playlist
        while not self.is_empty():
            self.delete_song(0)
        
        # Then add the shuffled songs
        for song in shuffled_songs:
            self.add_existing_song(song)
        
        return shuffled_songs
    
    def get_action_history(self) -> List[str]:
        """
        Get the history of playlist actions.
        
        Returns:
            List[str]: List of action types in chronological order
        """
        return self.action_logger.get_action_history()
    
    def clear_action_history(self) -> None:
        """
        Clear the action history.
        """
        self.action_logger.clear_history()
    
    def merge_alternately(self, other_playlist: 'Playlist') -> 'Playlist':
        """
        Merge this playlist with another playlist in an alternating fashion.
        """
        merged_playlist = Playlist()
        
        songs1 = self.get_all_songs()
        songs2 = other_playlist.get_all_songs()
        
        i, j = 0, 0
        while i < len(songs1) and j < len(songs2):
            merged_playlist.add_existing_song(songs1[i])
            i += 1
            
            merged_playlist.add_existing_song(songs2[j])
            j += 1
        
        while i < len(songs1):
            merged_playlist.add_existing_song(songs1[i])
            i += 1
        
        while j < len(songs2):
            merged_playlist.add_existing_song(songs2[j])
            j += 1
        
        return merged_playlist