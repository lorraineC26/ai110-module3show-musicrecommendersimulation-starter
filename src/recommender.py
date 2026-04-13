from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Score every song against the user profile and return the top k sorted by score."""
        user_dict = user.__dict__
        scored = sorted(
            self.songs,
            key=lambda song: score_song(user_dict, song.__dict__)[0],
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable breakdown of why this song was recommended."""
        _, reasons = score_song(user.__dict__, song.__dict__)
        return " | ".join(reasons)

def load_songs(csv_path: str) -> List[Dict]:
    """Read data/songs.csv and return a list of song dicts with typed numeric fields."""
    import csv
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences (max 4.5 pts) and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Rule 1 — Genre match: +2.0 if exact match, else 0
    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append(f"genre match (+2.0)")
    else:
        reasons.append(f"no genre match (+0.0)")

    # Rule 2 — Mood match: +1.0 if exact match, else 0
    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append(f"mood match (+1.0)")
    else:
        reasons.append(f"no mood match (+0.0)")

    # Rule 3 — Energy proximity: 1.0 × (1 − |song.energy − target_energy|)
    energy_pts = 1.0 * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.2f})")

    # Rule 4 — Acousticness preference: 0.5 × (1 − |song.acousticness − acousticness_pref|)
    acousticness_pref = 0.8 if user_prefs["likes_acoustic"] else 0.2
    acoustic_pts = 0.5 * (1 - abs(song["acousticness"] - acousticness_pref))
    score += acoustic_pts
    reasons.append(f"acousticness preference (+{acoustic_pts:.2f})")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, explanation)."""
    scored = [
        (song, score, " | ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return [(song, score, explanation)
            for song, score, explanation in sorted(scored, key=lambda x: x[1], reverse=True)][:k]
