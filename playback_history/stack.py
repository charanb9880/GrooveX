class StackNode:
    """
    Node class for linked list stack implementation.

    Attributes:
        song (Song): Song data stored in the node.
        next (StackNode): Reference to next node in stack.
    """
    def __init__(self, song):
        self.song = song
        self.next = None


class Stack:
    """
    Linked list based stack for managing recently played songs.

    Time Complexity (push, pop, peek): O(1)
    Space Complexity: O(N) for N songs in stack
    """
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, song):
        """
        Push a song onto the stack.
        """
        new_node = StackNode(song)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        """
        Pop and return the top song from the stack.
        Returns None if stack is empty.
        """
        if not self.top:
            return None
        popped_song = self.top.song
        self.top = self.top.next
        self.size -= 1
        return popped_song

    def peek(self):
        """
        Return the top song without removing.
        Returns None if empty.
        """
        return self.top.song if self.top else None

    def is_empty(self):
        return self.top is None
