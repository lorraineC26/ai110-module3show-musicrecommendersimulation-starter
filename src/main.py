"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 
    print(f"Load songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "favorite_genre": "rock",
        "favorite_mood":  "energetic",
        "target_energy":  0.75,
        "likes_acoustic": False,
    }

    # Laid-back acoustic fan
    user_prefs_2 = {
        "favorite_genre": "folk",
        "favorite_mood":  "calm",
        "target_energy":  0.30,
        "likes_acoustic": True,
    }

    # Upbeat pop listener
    user_prefs_3 = {
        "favorite_genre": "pop",
        "favorite_mood":  "happy",
        "target_energy":  0.85,
        "likes_acoustic": False,
    }

    # --- Edge cases ---

    # Edge Case 1: Genre and mood point to different songs (no song is both EDM and sad).
    # Genre weight (2.0) is double mood weight (1.0), so the scorer may recommend
    # high-energy EDM to a user who explicitly asked for sad music.
    edge_case_1 = {
        "favorite_genre": "edm",
        "favorite_mood":  "sad",
        "target_energy":  0.9,
        "likes_acoustic": False,
    }

    # Edge Case 2: Acoustic preference fights energy preference.
    # All high-acousticness songs in the dataset are low-energy (0.28–0.47),
    # so likes_acoustic=True and target_energy=0.95 pull toward opposite ends of the catalog.
    edge_case_2 = {
        "favorite_genre": "folk",
        "favorite_mood":  "peaceful",
        "target_energy":  0.95,
        "likes_acoustic": True,
    }

    # Edge Case 3: Mood value that exists in no song ("bored").
    # Mood score will be 0 for every candidate — silent degradation with no warning.
    # Watch whether the top results feel coherent or random.
    edge_case_3 = {
        "favorite_genre": "lofi",
        "favorite_mood":  "bored",
        "target_energy":  0.40,
        "likes_acoustic": True,
    }

    # Edge Case 4: Unreachable energy target (0.0).
    # The lowest-energy song in the dataset is 0.28 (Spacewalk Thoughts),
    # so no song can earn the full +1.0 energy points — every song is penalized.
    edge_case_4 = {
        "favorite_genre": "ambient",
        "favorite_mood":  "chill",
        "target_energy":  0.0,
        "likes_acoustic": True,
    }

    for prefs in [user_prefs, user_prefs_2, user_prefs_3,
                  edge_case_1, edge_case_2, edge_case_3, edge_case_4]:
        recommendations = recommend_songs(prefs, songs, k=5)

        print("\n" + "=" * 50)
        print("  TOP RECOMMENDATIONS")
        print(f"  Genre: {prefs['favorite_genre']}  |  Mood: {prefs['favorite_mood']}  |  Energy: {prefs['target_energy']}")
        print("=" * 50)

        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n#{rank}  {song['title']}  ({song['artist']})")
            print(f"    Score : {score:.2f} / 4.50")
            print("    Why   :")
            for reason in explanation.split(" | "):
                print(f"            - {reason}")
        print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
