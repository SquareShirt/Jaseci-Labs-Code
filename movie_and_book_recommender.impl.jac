impl RecommenderApp.start {
    print("This is a movie and book recommender app.");
    print("You will be given movie recommendations and book recommendations according to your preferences.");
    print("Type 'quit' anytime to exit.\n");

    # Step 1: Ask for a movie they like
    print("Name a movie you like?");
    fav_movie = input("> ");
    if fav_movie == "quit" {
        print("Goodbye!");
        disengage;
    }

    # Step 2: Ask for a book they have read
    print("Name a book you have read.");
    fav_book = input("> ");
    if fav_book == "quit" {
        print("Goodbye!");
        disengage;
    }

    # Step 3: Show genres
    print("\nMovie genres: Action, Comedy, Drama, Sci-Fi, Romance");
    print("Enter 2 movie genres you are interested in getting recommendations for (comma separated).");
    movie_genres = input("> ").split(",");
    if "quit" in movie_genres {
        print("Goodbye!");
        disengage;
    }

    print("\nBook genres: Fantasy, Mystery, Biography, Science Fiction, Historical");
    print("Enter 2 book genres you are interested in getting recommendations for (comma separated).");
    book_genres = input("> ").split(",");
    if "quit" in book_genres {
        print("Goodbye!");
        disengage;
    }

    # Step 4: Get recommendations from Gemini
    recommendations = get_recommendations(fav_movie, fav_book, movie_genres, book_genres);

    # Step 5: Display results
    print("\nHere are your recommendations:");
    print(recommendations);

    print("\nThanks for using our recommender app!");
    disengage;
}
