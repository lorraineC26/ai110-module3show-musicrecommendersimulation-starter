# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

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

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

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
