from .linked_list import Node
from .song import Song

class DoublyLinkedList:
    """
    Doubly linked list implementation to represent the playlist.
    Supports insertion, deletion, moving nodes, and reversing the list.

    Time Complexity (operations):
    - add_song: O(1) (at tail)
    - delete_song: O(N)
    - move_song: O(N)
    - reverse_playlist: O(N)
    Space Complexity: O(N) for N songs in playlist
    """
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def add_song(self, song: Song):
        new_node = Node(song)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def delete_song(self, index: int):
        if index < 0 or index >= self.size:
            raise IndexError("Index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev
        self.size -= 1

    def move_song(self, from_index: int, to_index: int):
        if (from_index < 0 or from_index >= self.size or
            to_index < 0 or to_index >= self.size):
            raise IndexError("Index out of bounds")
        if from_index == to_index:
            return
        # Remove node at from_index
        current = self.head
        for _ in range(from_index):
            current = current.next
        # Disconnect node
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev

        # Insert node at to_index
        if to_index == 0:
            current.next = self.head
            if self.head:
                self.head.prev = current
            current.prev = None
            self.head = current
            if self.tail is None:
                self.tail = current
        else:
            target = self.head
            for _ in range(to_index - 1):
                target = target.next
            current.next = target.next
            if target.next:
                target.next.prev = current
            current.prev = target
            target.next = current

    def reverse_playlist(self):
        """
        Reverses the playlist in-place.
        Time Complexity: O(N)
        """
        current = self.head
        self.tail = self.head
        prev_node = None
        while current:
            next_node = current.next
            current.next = prev_node
            current.prev = next_node
            prev_node = current
            current = next_node
        self.head = prev_node
