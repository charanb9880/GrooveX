from song_rating_tree.bst_node import BSTNode

class RatingBST:
    """
    Binary Search Tree that organizes and enables fast access to
    buckets of songs grouped by rating value.
    """
    def __init__(self):
        # Root node of the BST (can be None if tree is empty)
        self.root = None

    def insert_song(self, song, rating):
        """
        Insert a Song into the correct rating bucket/node.

        :param song: Song object to insert
        :param rating: Int from 1 to 5 (the rating)
        :raises ValueError: If rating is outside 1 to 5
        """
        if rating < 1 or rating > 5:
            raise ValueError(f"Invalid rating {rating}: must be between 1 and 5 inclusive.")
        self.root = self._insert(self.root, song, rating)


    def _insert(self, node, song, rating):
        # If this subtree is empty, make a new BSTNode
        if node is None:
            new_node = BSTNode(rating)
            new_node.bucket.add_song(song)
            return new_node

        # If rating is lower, insert left; if higher, insert right
        if rating < node.rating:
            node.left = self._insert(node.left, song, rating)
        elif rating > node.rating:
            node.right = self._insert(node.right, song, rating)
        else:  # rating == node.rating, add song to the rating's bucket
            node.bucket.add_song(song)
        return node

    def search_by_rating(self, rating):
        """
        Retrieve all Song objects with a given rating.

        :param rating: Int rating to search for
        :return: List[Song]
        """
        node = self.root
        while node:
            if rating < node.rating:
                node = node.left
            elif rating > node.rating:
                node = node.right
            else:
                # Found the rating bucket; return copies of songs
                return node.bucket.get_songs()
        # If not found, return empty list
        return []

    def delete_song(self, song_id):
        """
        Remove a song (by song_id) from all buckets.

        :param song_id: Song's unique identifier
        """
        self._delete_song(self.root, song_id)

    def _delete_song(self, node, song_id):
        if node is not None:
            node.bucket.remove_song(song_id)
            # Recursively delete in left and right subtrees
            self._delete_song(node.left, song_id)
            self._delete_song(node.right, song_id)
