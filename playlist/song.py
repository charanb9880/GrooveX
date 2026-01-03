class Song:
    """
    Represents a Song entity in the playlist.
    """
    def __init__(self, title, artist, duration, song_id=None, genre=None):
        self.song_id = song_id
        self.title = title
        self.artist = artist
        self.duration = duration

        # NEW fields
        self.genre = genre
        self.play_count = 0

    def increment_play_count(self):
        self.play_count += 1
