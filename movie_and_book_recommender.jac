"""Movie and Book Recommender App"""

import from byllm.llm { Model }

# Initialize Gemini LLM
glob llm = Model(model_name="gemini/gemini-2.0-flash", verbose=False);

# Function to get recommendations using Gemini
def get_recommendations(movie: str, book: str, movie_genres: list[str], book_genres: list[str]) -> str by llm(prompt_template="""
You are a movie and book recommender system.

The user has given:
- Favorite movie: {movie}
- Favorite book: {book}
- Preferred movie genres: {movie_genres}
- Preferred book genres: {book_genres}

Your task:
1. Recommend exactly 5 movies:
   - 3 movies based on the favorite movie.
   - 2 movies based on the preferred movie genres.

2. Recommend exactly 5 books:
   - 3 books based on the favorite book.
   - 2 books based on the preferred book genres.

Output format must be:

Movies:
1. Title
2. Title
3. Title
4. Title
5. Title

Books:
1. Title
2. Title
3. Title
4. Title
5. Title

Do not include commentary or explanations.
""");

walker RecommenderApp {
    can start with `root entry;
}

with entry:__main__ {
    root spawn RecommenderApp();
}
