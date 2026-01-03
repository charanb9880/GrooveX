class RatingBucket:
    """
    Container for multiple Song objects sharing the same rating.
    """
    def __init__(self, rating):
        # Store the bucket's rating (int, e.g., 1-5)
        self.rating = rating

        # List of Song objects in this bucket
        self.songs = []

    def add_song(self, song):
        """
        Add a song to this rating bucket.

        :param song: Song object (must have .song_id attribute)
        """
        self.songs.append(song)

    def remove_song(self, song_id):
        """
        Remove a song from the bucket given its unique song_id.

        :param song_id: ID of the song to be removed
        """
        self.songs = [s for s in self.songs if s.song_id != song_id]

    def get_songs(self):
        """
        Return the list of all Song objects in this bucket.

        :return: List of Song objects
        """
        return self.songs.copy()
