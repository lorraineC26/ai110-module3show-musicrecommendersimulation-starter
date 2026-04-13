# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MoodMatch 1.0**

---

## 2. Intended Use  

MoodMatch 1.0 recommends songs from a small catalog based on a user's mood, genre, energy level, and acoustic preference.

It generates a ranked list of up to five songs. Each song is scored and the highest-scoring song appears first.

The system assumes each user can be described by four simple inputs: a favorite genre, a mood word, a target energy level (0 to 1), and whether they like acoustic music.

It does not learn over time. It does not remember past listens. It scores each song the same way every time.

This system is built for classroom exploration, not real users. It is meant to show how a basic recommender works — and where simple scoring logic can go wrong.

---

## 3. How the Model Works  

Every song in the catalog has five features: genre, mood, energy level, acousticness, and tempo. The system uses four of those — genre, mood, energy, and acousticness — to score each song.

The user tells the system four things: their favorite genre, their favorite mood, how energetic they want the music to feel (on a scale from 0 to 1), and whether they like acoustic music.

The system then goes through every song and adds up a score based on four rules.

**Rule 1 — Genre.** If the song's genre matches the user's favorite genre, it gets 2 full points. If not, it gets zero. This is the biggest rule.

**Rule 2 — Mood.** If the song's mood label exactly matches the user's mood preference, it gets 1 point. If the words don't match exactly, it gets zero — even if the moods are very similar.

**Rule 3 — Energy.** The system measures how close the song's energy level is to the user's target. A perfect match gives 1 full point. A big difference gives a smaller number.

**Rule 4 — Acousticness.** The system checks whether the song sounds acoustic or not. If the user likes acoustic music, songs that sound acoustic score higher. This rule is worth up to 0.5 points.

All four scores are added together. The maximum possible score is 4.5 points. Songs are then sorted from highest to lowest, and the top five are returned.

The starter logic was already structured around these four rules. One experimental run tested what would happen if the genre weight was cut in half and the energy weight was doubled — that test showed how much the #1 result depends on the genre rule staying as large as it is.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

### Genre Filter Bubble

15 of 17 genres in the catalog have exactly one song. Because genre carries 44% of the total score (2.0 pts), that one song always ranks #1 for any matching user — no matter how badly its energy or mood fits.

- An ambient fan who wants high energy (`target_energy = 0.95`) still gets *Spacewalk Thoughts* (`energy = 0.28`) at #1, because the 2.0pt genre bonus outweighs any energy penalty.
- The system behaves more like a genre lookup table than a true recommender: energy and mood only break ties *within* the top slot, they can never displace it.

### Acousticness Boolean Cliff

`likes_acoustic` maps to either `0.8` (True) or `0.2` (False) — there is no middle ground.

- A listener whose real acoustic preference sits around `0.5` is misrepresented by both options and loses up to **0.15 pts** compared to what a continuous scale would award.
- This means two users with very different acoustic tastes can receive identical acousticness scores if they both fall on the same side of the True/False divide.

### Ignored Song Features

`tempo_bpm`, `valence`, and `danceability` are stored on every song but never used in scoring.

- A user who wants fast-tempo or highly danceable music receives recommendations based only on genre, mood, energy, and acousticness — the extra data is collected but silently discarded.

### Genre Overfitting

The 2.0-pt genre bonus is large enough that a genre match nearly always wins, regardless of how the other signals compare.

- A rock fan with `target_energy = 0.3` still gets *Storm Runner* (`energy = 0.91`) at #1 — an energy gap of 0.61 — because no combination of mood + energy + acousticness from a non-rock song can overcome the head start.
- In practice, genre preference determines the #1 result and the remaining rules only sort positions 2–5.

### Catalog Favors Certain User Types

The catalog is unevenly distributed, which quietly advantages some users over others.

- Lofi fans (3 songs) and pop fans (2 songs) receive meaningfully differentiated top-5 lists; users of any other genre get one genre match and four cross-genre fillers.
- High-energy users (`target_energy > 0.8`) have 6 catalog candidates to compete for their top spots; low-energy users (`target_energy < 0.4`) have only 5, concentrated in softer genres like ambient, classical, and folk.

---

## 7. Evaluation  

Six user profiles were tested across three rounds of experiments. For each run, the goal was to check whether the top result felt like a reasonable match — and to find cases where it clearly did not.

### Profiles Tested

| Profile | Genre | Mood | Energy | Acoustic |
|---|---|---|---|---|
| Main | rock | energetic | 0.75 | No |
| Near-perfect | pop | happy | 0.85 | No |
| Genre/mood conflict | edm | sad | 0.90 | No |
| Unknown mood | folk | calm | 0.30 | Yes |
| Unreachable energy | ambient | chill | 0.00 | Yes |
| Rebalanced weights | rock | energetic | 0.75 | No |

---

### Pairwise Comparisons

**Rock/energetic vs. Pop/happy**  
The pop/happy profile produced the highest score in all tests — *Sunrise City* scored 4.46 out of 4.50, with all four rules contributing. The rock profile scored noticeably lower (3.29) because the only rock song in the catalog has mood "intense", not "energetic", so the mood rule never fired. This comparison shows the system rewards users whose preferences happen to align with a real song almost perfectly, but quietly penalizes users whose mood word is close but not an exact match.

**EDM/sad vs. Folk/calm**  
Both profiles had a mood preference the system failed to satisfy — but for different reasons. The EDM/sad profile got loud dance music (*Hyperdrive*) at #1 because no EDM song is sad, and genre's higher weight overruled the mood request entirely. The folk/calm profile got the right genre (*Willow & Rain*) but the word "calm" does not exist in the catalog, so mood scored zero for every song with no warning. In both cases, the user asked for something the system could not deliver, but the system returned a confident-looking result anyway.

**Ambient/chill/0.0 vs. Rock/energetic/0.75**  
The ambient profile still returned the correct song (*Spacewalk Thoughts*) at #1, but the score was capped at 4.16 instead of the maximum 4.50 — because the catalog's lowest energy is 0.28, so a target of 0.0 is unreachable. The rock profile scored normally with no structural ceiling. This pair reveals that low-energy users are quietly penalized by a catalog that skews toward higher energy, even when the right song exists.

**Baseline weights vs. Rebalanced weights (same rock profile)**  
Running the rock/energetic profile with genre halved (1.0) and energy doubled (2.0) swapped the top two results: *Block Party Anthem* (hip-hop) moved to #1 and *Storm Runner* (rock) dropped to #2. The rest of the top five stayed nearly the same. This shows how sensitive the #1 slot is to a single weight change — and confirms that the original genre weight of 2.0 is what keeps the rock song on top for a self-described rock fan.

---

### What Surprised Me

The most unexpected result was the EDM/sad edge case. The system recommended loud party music to someone who asked for sad songs, and the score (*Hyperdrive* at 3.37) looked high and confident — there was no signal in the output that anything had gone wrong. A real user reading those results would have no idea their mood preference had been ignored. That gap between a confident-looking score and an actually poor recommendation was not obvious until the edge cases were tested deliberately.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
