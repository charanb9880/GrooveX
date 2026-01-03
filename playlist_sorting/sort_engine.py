from playlist.song import Song


class SortCriteria:
    """
    Enumeration class to define different sorting criteria.
    """
    ALPHA_TITLE = 'alpha_title'      # Alphabetical ascending on song title
    DURATION_ASC = 'duration_asc'    # Duration ascending
    DURATION_DESC = 'duration_desc'  # Duration descending
    RECENT = 'recent'                # Most recently added first


class SortEngine:
    """
    Implements custom Merge Sort algorithm to sort a list of Song objects
    based on various criteria such as title, duration, or recent addition.
    Provides educational insight into sorting algorithms and time/space tradeoffs.
    """

    def merge_sort(self, songs, criteria=SortCriteria.ALPHA_TITLE):
        """
        Public method to perform a merge sort on the list of songs according to the provided criteria.

        :param songs: List[Song] - List of Song objects to sort
        :param criteria: str - Sorting criteria specified by the SortCriteria class
        :return: List[Song] - New sorted list of songs by specified criteria
        """
        if len(songs) <= 1:
            # Base case: A list of zero or one song is already sorted
            return songs.copy()

        # Find the middle index to split the list
        mid = len(songs) // 2
        left_part = self.merge_sort(songs[:mid], criteria)   # Recursively sort left half
        right_part = self.merge_sort(songs[mid:], criteria)  # Recursively sort right half

        # Merge sorted halves back together
        return self._merge(left_part, right_part, criteria)

    def _merge(self, left, right, criteria):
        """
        Internal helper method to merge two sorted sublists of songs into one sorted list.

        :param left: List[Song] - Sorted sublist of Song objects
        :param right: List[Song] - Sorted sublist of Song objects
        :param criteria: str - Sorting criteria to use for comparisons
        :return: List[Song] - Merged sorted list
        """
        merged = []  # Result list to store sorted songs
        i = j = 0    # Pointers to traverse left and right lists

        # Iterate until one of the sublists is exhausted
        while i < len(left) and j < len(right):
            # Decide which song should be appended next based on the criteria
            if self._compare(left[i], right[j], criteria):
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        # Append any remaining songs from the left sublist
        merged.extend(left[i:])
        # Append any remaining songs from the right sublist
        merged.extend(right[j:])

        return merged

    def _compare(self, song_a, song_b, criteria):
        """
        Compares two Song objects based on the selected criteria.

        :param song_a: Song - First Song object to compare
        :param song_b: Song - Second Song object to compare
        :param criteria: str - Sorting criteria as per SortCriteria
        :return: bool - True if song_a should come before or equal to song_b
        """
        if criteria == SortCriteria.ALPHA_TITLE:
            # Compare titles in case-insensitive alphabetical order
            return song_a.title.lower() <= song_b.title.lower()
        elif criteria == SortCriteria.DURATION_ASC:
            # Compare durations in ascending order (shorter first)
            return song_a.duration <= song_b.duration
        elif criteria == SortCriteria.DURATION_DESC:
            # Compare durations in descending order (longer first)
            return song_a.duration >= song_b.duration
        elif criteria == SortCriteria.RECENT:
            # Compare based on added_time (timestamp), more recent first
            # Assume Song has attribute 'added_time'; default to 0 if missing
            return getattr(song_a, 'added_time', 0) >= getattr(song_b, 'added_time', 0)
        else:
            # Fallback: alphabetical by title
            return song_a.title.lower() <= song_b.title.lower()
