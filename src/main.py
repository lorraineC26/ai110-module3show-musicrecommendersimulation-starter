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

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  TOP RECOMMENDATIONS")
    print(f"  Genre: {user_prefs['favorite_genre']}  |  Mood: {user_prefs['favorite_mood']}  |  Energy: {user_prefs['target_energy']}")
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
