"""
Smart Recommender module for PlayWise Music Engine.

Returns candidate songs that were NOT played recently but are similar to user's recently played songs
using simple, fast similarity checks (genre + numeric thresholds for duration/BPM).
"""

from typing import Dict, List, Set, Optional, Tuple, Any
from collections import deque, defaultdict
from dataclasses import dataclass
from playlist.song import Song


@dataclass
class Recommendation:
    """Data class to represent a recommendation with score and reason."""
    song_id: str
    score: float
    reason: str


class SmartRecommender:
    """
    Smart Recommender that suggests unplayed but similar songs based on play history.
    
    Algorithm:
    1. Maintain a sliding window of last W played song_ids (default W=50)
    2. For recommendation:
       a. Take the last k played songs (e.g., k=5)
       b. For each seed song, compute candidate pool via PlaylistExplorer
       c. Filter out recently played, skipped, and active playlist songs
       d. Apply similarity scoring (genre, subgenre, mood, duration, BPM)
       e. Aggregate scores across seeds
       f. Return top N candidates sorted by score
    
    Time Complexity:
        - record_play: O(1)
        - recommend: O(k * M log N) where k=seed_count, M=candidates per seed, N=top_n
    
    Space Complexity:
        - O(W + S) where W=window size, S=total songs
    """
    
    def __init__(self, playlist_explorer, skipped_tracker, playlist_songs_getter, 
                 window_size: int = 50, seed_count: int = 5, top_n: int = 10,
                 duration_threshold: int = 120, bpm_threshold: int = 10,
                 max_candidates_per_seed: int = 200):
        """
        Initialize the Smart Recommender.
        
        Args:
            playlist_explorer: PlaylistExplorer instance for hierarchical song lookup
            skipped_tracker: RecentlySkippedTracker instance for filtering skipped songs
            playlist_songs_getter: Function to get current playlist songs
            window_size (int): Size of sliding window for recent plays (default: 50)
            seed_count (int): Number of recent songs to use as seeds (default: 5)
            top_n (int): Number of recommendations to return (default: 10)
            duration_threshold (int): Threshold for duration similarity in seconds (default: 120)
            bpm_threshold (int): Threshold for BPM similarity (default: 10)
            max_candidates_per_seed (int): Max candidates to consider per seed (default: 200)
        """
        # Dependencies
        self.playlist_explorer = playlist_explorer
        self.skipped_tracker = skipped_tracker
        self.playlist_songs_getter = playlist_songs_getter
        
        # Configuration
        self.window_size = window_size
        self.seed_count = seed_count
        self.top_n = top_n
        self.duration_threshold = duration_threshold
        self.bpm_threshold = bpm_threshold
        self.max_candidates_per_seed = max_candidates_per_seed
        
        # State
        self.play_window = deque(maxlen=window_size)  # Sliding window of (song_id, timestamp)
        self.played_set: Set[str] = set()  # For O(1) lookup of recently played songs
        self.song_metadata: Dict[str, Dict[str, Any]] = {}  # song_id -> metadata
        self.total_listen_time: Dict[str, int] = defaultdict(int)  # song_id -> total seconds
    
    def record_play(self, song_id: str, played_at: float, play_duration: int, 
                    metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Record a play event to update sliding window and play stats.
        
        Time Complexity: O(1)
        Space Complexity: O(1) amortized
        
        Args:
            song_id (str): Unique identifier for the song
            played_at (float): Timestamp when song was played
            play_duration (int): Duration of the play in seconds
            metadata (Optional[Dict]): Song metadata (genre, subgenre, mood, duration, bpm, etc.)
        """
        # Add to sliding window
        self.play_window.append((song_id, played_at))
        
        # Add to played set
        self.played_set.add(song_id)
        
        # Update total listen time
        self.total_listen_time[song_id] += play_duration
        
        # Store metadata if provided
        if metadata:
            self.song_metadata[song_id] = metadata
    
    def _get_similar_songs(self, seed_song_id: str) -> Set[str]:
        """
        Get similar songs to a seed song using PlaylistExplorer.
        
        Time Complexity: O(bucket_size) typically
        Space Complexity: O(M) where M is number of candidates
        
        Args:
            seed_song_id (str): ID of the seed song
            
        Returns:
            Set[str]: Set of similar song IDs
        """
        # Get seed song metadata
        if seed_song_id not in self.song_metadata:
            return set()
        
        seed_meta = self.song_metadata[seed_song_id]
        genre = seed_meta.get('genre')
        subgenre = seed_meta.get('subgenre')
        mood = seed_meta.get('mood')
        artist = seed_meta.get('artist')
        
        # If we have genre, search by genre hierarchy
        # We exclude the artist to find songs by OTHER artists in the same genre/subgenre/mood
        if genre:
            criteria = {'genre': genre}
            if subgenre:
                criteria['subgenre'] = subgenre
            if mood:
                criteria['mood'] = mood
            # Note: We intentionally exclude artist to find similar songs by different artists
                
            # Use PlaylistExplorer to find similar songs
            similar_songs = self.playlist_explorer.search(criteria)
            # Exclude the seed song itself from recommendations
            similar_songs.discard(seed_song_id)
            return similar_songs
        
        return set()
    
    def _calculate_similarity_score(self, seed_id: str, candidate_id: str) -> Tuple[float, str]:
        """
        Calculate similarity score between seed and candidate songs.
        
        Scoring formula:
        Score = w1*(genre_match: 1/0) + w2*(subgenre_match:1/0) + w3*(mood_match:1/0)
                + w4*(duration_score) + w5*(bpm_score)
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            seed_id (str): ID of the seed song
            candidate_id (str): ID of the candidate song
            
        Returns:
            Tuple[float, str]: (score, reason)
        """
        if seed_id not in self.song_metadata or candidate_id not in self.song_metadata:
            # print(f"DEBUG: Missing metadata for seed={seed_id} or candidate={candidate_id}")
            # print(f"DEBUG: seed_metadata={seed_id in self.song_metadata}, candidate_metadata={candidate_id in self.song_metadata}")
            return 0.0, "Missing metadata"
        
        seed_meta = self.song_metadata[seed_id]
        candidate_meta = self.song_metadata[candidate_id]
        
        # Weight factors
        W_GENRE = 1.0
        W_SUBGENRE = 0.8
        W_MOOD = 0.6
        W_DURATION = 0.5
        W_BPM = 0.4
        
        score = 0.0
        reasons = []
        
        # Genre match
        seed_genre = seed_meta.get('genre', '').lower()
        candidate_genre = candidate_meta.get('genre', '').lower()
        if seed_genre and candidate_genre and seed_genre == candidate_genre:
            score += W_GENRE
            reasons.append("same genre")
        
        # Subgenre match
        seed_subgenre = seed_meta.get('subgenre', '').lower()
        candidate_subgenre = candidate_meta.get('subgenre', '').lower()
        if seed_subgenre and candidate_subgenre and seed_subgenre == candidate_subgenre:
            score += W_SUBGENRE
            reasons.append("same subgenre")
        
        # Mood match
        seed_mood = seed_meta.get('mood', '').lower()
        candidate_mood = candidate_meta.get('mood', '').lower()
        if seed_mood and candidate_mood and seed_mood == candidate_mood:
            score += W_MOOD
            reasons.append("same mood")
        
        # Duration similarity
        seed_duration = seed_meta.get('duration', 0)
        candidate_duration = candidate_meta.get('duration', 0)
        if seed_duration > 0 and candidate_duration > 0:
            duration_diff = abs(candidate_duration - seed_duration)
            if duration_diff <= self.duration_threshold:
                duration_score = max(0, 1 - duration_diff / self.duration_threshold)
                score += W_DURATION * duration_score
                if duration_score > 0.5:
                    reasons.append(f"similar duration (±{duration_diff}s)")
        
        # BPM similarity
        seed_bpm = seed_meta.get('bpm', 0)
        candidate_bpm = candidate_meta.get('bpm', 0)
        if seed_bpm > 0 and candidate_bpm > 0:
            bpm_diff = abs(candidate_bpm - seed_bpm)
            if bpm_diff <= self.bpm_threshold:
                bpm_score = max(0, 1 - bpm_diff / self.bpm_threshold)
                score += W_BPM * bpm_score
                if bpm_score > 0.5:
                    reasons.append(f"similar BPM (±{bpm_diff})")
        
        reason = ", ".join(reasons) if reasons else "minimal similarity"
        return score, reason
    
    def recommend(self, seed_count: Optional[int] = None, top_n: Optional[int] = None, 
                  exclude_active_playlist: bool = True) -> List[Recommendation]:
        """
        Generate smart recommendations based on recent play history.
        
        Time Complexity: O(k * M log N) where k=seed_count, M=candidates per seed, N=top_n
        Space Complexity: O(N) for the result list
        
        Args:
            seed_count (Optional[int]): Number of recent songs to use as seeds
            top_n (Optional[int]): Number of recommendations to return
            exclude_active_playlist (bool): Whether to exclude songs in active playlist
            
        Returns:
            List[Recommendation]: List of recommended songs with scores and reasons
        """
        # Use configured values if not provided
        seed_count = seed_count or self.seed_count
        top_n = top_n or self.top_n
        
        # Get recent seed songs (last k played)
        seed_songs = []
        for song_id, timestamp in reversed(self.play_window):
            if len(seed_songs) >= seed_count:
                break
            if song_id not in seed_songs:  # Avoid duplicates
                seed_songs.append(song_id)
        
        if not seed_songs:
            return []  # No recent plays to base recommendations on
        
        # Debug print
        # print(f"DEBUG: Seed songs: {seed_songs}")
        
        # Get currently active playlist songs if needed
        active_playlist_songs = set()
        if exclude_active_playlist:
            playlist_songs = self.playlist_songs_getter()
            active_playlist_songs = {song.song_id for song in playlist_songs if song.song_id}
        
        # Aggregate candidates and scores across all seeds
        candidate_scores: Dict[str, float] = defaultdict(float)
        candidate_reasons: Dict[str, List[str]] = defaultdict(list)
        
        # Debug print
        # print(f"DEBUG: Processing seeds: {seed_songs}")
        
        for seed_id in seed_songs:
            # Get similar songs
            similar_songs = self._get_similar_songs(seed_id)
            
            # Debug print
            # print(f"DEBUG: Seed {seed_id} found similar songs: {similar_songs}")
            
            # Limit candidates to prevent explosion
            similar_songs_list = list(similar_songs)[:self.max_candidates_per_seed]
            
            # Score each candidate
            for candidate_id in similar_songs_list:
                # Skip filtering
                if candidate_id in self.played_set:
                    # print(f"DEBUG: Skipping {candidate_id} - in played_set")
                    continue  # Recently played
                if self.skipped_tracker.is_recently_skipped(candidate_id):
                    # print(f"DEBUG: Skipping {candidate_id} - is recently skipped")
                    continue  # Recently skipped
                if exclude_active_playlist and candidate_id in active_playlist_songs:
                    # print(f"DEBUG: Skipping {candidate_id} - in active playlist")
                    continue  # In active playlist
                
                # Calculate similarity score
                score, reason = self._calculate_similarity_score(seed_id, candidate_id)
                # print(f"DEBUG: Candidate {candidate_id} got score {score} for seed {seed_id}")
                
                # Only consider candidates with some similarity
                if score > 0:
                    candidate_scores[candidate_id] += score
                    candidate_reasons[candidate_id].append(reason)
                # Debug print
                # else:
                #     print(f"DEBUG: Candidate {candidate_id} got score {score} for seed {seed_id}")
        
        # Sort candidates by score and return top N
        sorted_candidates = sorted(candidate_scores.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for song_id, score in sorted_candidates[:top_n]:
            # Combine reasons
            reasons = list(set(candidate_reasons[song_id]))  # Remove duplicates
            reason = "; ".join(reasons) if reasons else "similar to recent plays"
            
            recommendations.append(Recommendation(
                song_id=song_id,
                score=round(score, 2),
                reason=reason
            ))
        
        return recommendations
    
    def get_popular_songs(self, exclude_recent: bool = True, exclude_skipped: bool = True,
                          top_n: Optional[int] = None) -> List[Recommendation]:
        """
        Fallback method to get popular songs when no similar songs found.
        
        Time Complexity: O(S log S) where S is number of songs with play data
        Space Complexity: O(N) for result list
        
        Args:
            exclude_recent (bool): Whether to exclude recently played songs
            exclude_skipped (bool): Whether to exclude recently skipped songs
            top_n (Optional[int]): Number of songs to return
            
        Returns:
            List[Recommendation]: List of popular songs
        """
        top_n = top_n or self.top_n
        
        # Sort songs by total listen time
        sorted_songs = sorted(self.total_listen_time.items(), key=lambda x: x[1], reverse=True)
        
        recommendations = []
        for song_id, total_time in sorted_songs:
            # Apply filters
            if exclude_recent and song_id in self.played_set:
                continue
            if exclude_skipped and self.skipped_tracker.is_recently_skipped(song_id):
                continue
            
            recommendations.append(Recommendation(
                song_id=song_id,
                score=float(total_time),
                reason=f"popular song (total listen time: {total_time}s)"
            ))
            
            if len(recommendations) >= top_n:
                break
        
        return recommendations