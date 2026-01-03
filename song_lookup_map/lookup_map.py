from playlist.song import Song
from typing import Optional
from .duplicate_cleaner import DuplicateCleaner


class SongLookupMap:
    """
    Hash map for constant-time song lookup by id or title.
    Synchronizes with playlist operations for immediate update.
    """
    def __init__(self, enable_dedupe: bool = True, dedupe_policy: str = 'first'):
        """
        Initialize the song lookup map.
        
        Args:
            enable_dedupe (bool): Whether to enable duplicate detection
            dedupe_policy (str): Duplicate handling policy ('first' or 'latest')
        """
        # Maps song_id to Song object
        self.id_map = {}
        # Maps song title to Song object
        self.title_map = {}
        # Duplicate cleaner
        self.enable_dedupe = enable_dedupe
        if enable_dedupe:
            self.duplicate_cleaner = DuplicateCleaner(keep=dedupe_policy)
        else:
            self.duplicate_cleaner = None

    def add_song(self, song: Song) -> Optional[str]:
        """
        Add (or update) a song in both id and title maps.
        
        Args:
            song (Song): Song object to add
            
        Returns:
            Optional[str]: None if song added successfully, existing song_id if duplicate and policy is 'first'
        """
        # Check for duplicates if enabled
        if self.enable_dedupe and self.duplicate_cleaner:
            duplicate_result = self.duplicate_cleaner.cleanup_on_add(song)
            if duplicate_result is not None:
                # Duplicate found and policy is 'first', reject the new song
                return duplicate_result
        
        # Add to maps
        if song.song_id is not None:
            self.id_map[song.song_id] = song
        # If multiple songs can have same title, use a list; here we assume unique
        self.title_map[song.title] = song
        
        # Register with duplicate cleaner if enabled
        if self.enable_dedupe and self.duplicate_cleaner:
            self.duplicate_cleaner.register(song.song_id, song.title, song.artist)
        
        return None

    def remove_song(self, song_id: str) -> bool:
        """
        Remove song from both maps by song_id.
        Returns True if successful, False if not found.
        """
        song = self.id_map.pop(song_id, None)
        if song and song.title in self.title_map:
            del self.title_map[song.title]
            # Deregister from duplicate cleaner if enabled
            if self.enable_dedupe and self.duplicate_cleaner:
                self.duplicate_cleaner.deregister(song_id, song.title, song.artist)
            return True
        return False

    def lookup_song_by_id(self, song_id: str) -> Optional[Song]:
        """
        Return the Song with given song_id, or None if not found.
        """
        return self.id_map.get(song_id, None)

    def lookup_song_by_title(self, title: str) -> Optional[Song]:
        """
        Return the Song with given title, or None if not found.
        """
        return self.title_map.get(title, None)