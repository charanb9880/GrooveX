from song_rating_tree.rating_bst import RatingBST

class SongRatingEngine:
    """
    High-level interface to interact with the rating BST for song operations.
    """
    def __init__(self):
        # The core BST managing song ratings
        self.bst = RatingBST()

    def insert_song(self, song, rating):
        """
        Insert a Song into the BST, grouped by rating.

        :param song: Song object (import from playlist.song)
        :param rating: Int from 1–5
        """
        self.bst.insert_song(song, rating)

    def search_by_rating(self, rating):
        """
        Retrieve all songs at a specific rating level.

        :param rating: Int from 1–5
        :return: List of Song objects
        """
        return self.bst.search_by_rating(rating)

    def delete_song(self, song_id):
        """
        Remove a song throughout the BST by its song_id.

        :param song_id: String/int, unique ID of the song
        """
        self.bst.delete_song(song_id)
