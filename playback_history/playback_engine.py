from .stack import Stack
from playlist.song import Song

class PlaybackHistory:
    """
    Stack-based playback history.
    """

    def __init__(self):
        self.history_stack = Stack()

    def record_played_song(self, song: Song):
        self.history_stack.push(song)

    def undo_last_play(self, playlist):
        last_song = self.history_stack.pop()
        if last_song is None:
            return False
        playlist.add_existing_song(last_song)
        return True

    def get_all_history(self):
        """Traverse linked-list stack and return all songs."""
        result = []
        node = self.history_stack.top
        while node:
            result.append(node.song)
            node = node.next
        return result
