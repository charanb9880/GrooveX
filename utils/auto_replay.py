import heapq

class AutoReplayManager:
    CALM_GENRES = {"lo-fi", "lofi", "jazz", "chill", "ambient"}

    @classmethod
    def is_calm(cls, genre):
        if not genre:
            return False
        return genre.lower() in cls.CALM_GENRES

    @staticmethod
    def top_k_calm_songs(songs, k=3):
        calming = [s for s in songs if s.genre and AutoReplayManager.is_calm(s.genre)]
        if not calming:
            return []

        return heapq.nlargest(k, calming, key=lambda s: s.play_count)
