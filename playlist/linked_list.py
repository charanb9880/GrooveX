class Node:
    """
    Doubly Linked List Node representing a song node in the playlist.
    Attributes:
        song (Song): The song data stored in the node.
        prev (Node): Reference to the previous node.
        next (Node): Reference to the next node.
    """
    def __init__(self, song):
        self.song = song
        self.prev = None
        self.next = None
