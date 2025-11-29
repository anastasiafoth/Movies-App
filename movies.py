
import random
from thefuzz import process
import movie_storage_sql
from datetime import datetime
import movies_web_generator


class Colors:
    """ ANSI color codes as class for easier usage"""
    """ Styleguide:
    BLUE = menu
    WHITE = if background color is different
    PINK = error messages
    DARK_VIOLET = input 
    
    BG_BLUE = only title
    """

    # Text colors
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    PINK = "\033[38;5;207m"
    DARK_VIOLET = "\033[38;5;135m"

    # Style
    BOLD = "\033[1m"

    # Background colors
    BG_BLUE = "\033[44m"

    # Reset
    ENDC = "\033[0m"

def colorize(text, *styles):
    """ Small helper function to avoid repeating long f-strings """

    style_codes = "".join(getattr(Colors, s, "") for s in styles)
    return f"{style_codes}{text}{Colors.ENDC}"


def title_screen():
    menu_items = [
        "Exit",
        "List movies",
        "Add movie",
        "Delete movie",
        "Update movie",
        "Stats",
        "Random movie",
        "Search movie",
        "Movies sorted by rating",
        "Movies sorted by year",
        "Filter movies",
        "Create a rating histogram",
        "Generate website"
    ]

    print(colorize("Menu:", "BLUE", "BOLD"))
    for i, item in enumerate(menu_items):
        print(f"{colorize(str(i), 'BLUE')}. {item}")


def main():
    print(
        f"{colorize("********** My Movies Database **********",
                    "BG_BLUE", "WHITE", "BOLD")}\n"
    )

    while True:
        title_screen()
        user_input = input(
            colorize(f"Enter choice ({colorize("0-12", "BLUE")}): ").strip()
        )
        if not user_input.isdigit():
            print(colorize("Please enter a number!", "PINK"))
            continue
        user_input = int(user_input)

        if not (0 <= user_input <= 12):
            print(colorize("Please enter a number between 0 and 12.", "PINK"))
            continue

        movies = movie_storage_sql.list_movies()

        if user_input == 0:
            print("Bye!")
            break
        elif user_input == 1:
            print_list_movies(movies)
        elif user_input == 2:
            add_movie(movies)
        elif user_input == 3:
            delete_movie(movies)
        elif user_input == 4:
            update_movie(movies)
        elif user_input == 5:
            stats(movies)
        elif user_input == 6:
            random_movie(movies)
        elif user_input == 7:
            search_for_movie(movies)
        elif user_input == 8:
            sorted_movies_by_rating(movies)
        elif user_input == 9:
            sorted_movies_by_year(movies)
        elif user_input == 10:
            filter_movies(movies)
        elif user_input == 11:
            create_rating_histogram(movies)
        elif user_input == 12:
            movies_web_generator.main(movies)

        input(f"\n{colorize("Press enter to continue", "BLUE", "BOLD")}")


def list_movies(movies):
    """Sorts all movies by title and calculates the total of movies"""
    sorted_movies_by_title = dict(sorted(movies.items()))
    total_movies = len(movies)
    return sorted_movies_by_title, total_movies


def print_list_movies(movies):
    """Prints sorted movies by title and total of movies"""
    if not movies:
        print(colorize("No movies available!", "PINK"))

    sorted_movies_by_title, total_movies = list_movies(movies)
    print(colorize(f"{total_movies} movies in total", "BOLD"))

    for movie, data in sorted_movies_by_title.items():
        print(f'{data["title"]} ({data["year"]}) : {data["rating"]}')


def add_movie(movies):
    """
        Adds new movie with name and rating
        The first movie was created in 1895
    """

    while True:
        movie_title = input(colorize("Enter new movie name: ","DARK_VIOLET")).strip()
        for movie, data in movies.items():
            if movie_title.lower().strip() == data["title"].lower().strip():
                print(f"This movie already exists {data["title"]}.")

            elif not movie_title:
                print("please enter a valid name.")
                continue

        break

    movie_storage_sql.add_movie(movie_title)


def delete_movie(movies):
    while True:
        movie_to_delete = input(
            colorize("Enter movie name to delete: ", "DARK_VIOLET")
        )
        if movie_to_delete == "":
            print("Please enter a valid Movie name.")
        else:
            break

    all_titles = [data["title"] for data in movies.values()]
    # Fuzzy search if no exact matches found
    if movie_to_delete not in all_titles:
        for id, data in movies.items():
            match = process.extract(movie_to_delete, data.values(), limit=1)

            while True:
                input_typo = input(colorize(f"The movie {movie_to_delete} does not exist. Did you mean: {match[0][0]} (yes|no)?: ", "PINK"))
                if "y" in input_typo.lower():
                    movie_to_delete = match[0][0]
                    break
                elif "n" in input_typo.lower():
                    print("No movie was deleted.")
                    return
                else:
                    print("Please type in (yes|no)")

    id = 0
    for movie, data in movies.items():
        if movie_to_delete == data["title"]:
            id = movie

    movie_storage_sql.delete_movie(id)
    print(f"The movie {movie_to_delete} was successfully deleted.")


def update_movie(movies):
    """Updates movie in databank with new rating"""

    while True:
        movie_to_update = input(
            colorize("Enter movie name you would like to update: ", "DARK_VIOLET")
        )
        if movie_to_update == "":
            print("Please enter valid movie name.")
        else:
            break

    all_titles = [data["title"] for data in movies.values()]

    for id, data in movies.items():
        match = process.extract(movie_to_update, data.values(), limit=1)
    if movie_to_update not in all_titles:
            input_typo = input(
                colorize(f"The movie {movie_to_update} does not exist. Did you mean: {match[0][0]} (yes|no)?: ", "PINK"))
            if "y" in input_typo.lower():
                movie_to_update = match[0][0]
    try:
        new_rating = float(input(f"Current movie rating is: {data["rating"]}\nEnter new movie rating (0-10): "))
    except ValueError:
        print("Please enter a number")
        return
    except KeyError:
        print(colorize("Movie doesn´t exist.", "PINK"))
        return

    id = 0
    for movie, data in movies.items():
        if movie_to_update == data["title"]:
            id = movie

    if 0 <= new_rating <= 10:
        movie_storage_sql.update_movie(id, movie_to_update, new_rating)
        print(f"The movie {movie_to_update} was successfully updated "
              f"with the new rating: {new_rating}")
    else:
        print(colorize("Rating is out of range.", "PINK"))


def stats(movies):
    """Shows average rating and median rating"""

    if not movies:
        print(colorize("No movies available!", "PINK"))
        return

    ratings = []

    #rating is now showing as "8.7/10" so we have to get the pure rating
    for id, data in movies.items():
        ratings.append(float(data["rating"][:-3]))

    # Average rating
    average_rating = sum(ratings) / len(ratings)
    print(f"Average rating: {average_rating:.1f}")

    # Median
    ratings.sort()
    n = len(ratings)
    if n % 2 == 0:
        median = (ratings[n // 2 - 1] + ratings[n // 2]) / 2
    else:
        median = ratings[n // 2]
    print(f"Median rating: {median:.1f}")

    # Best movie based on ratings
    best_rating = max(ratings)

    for name, data in movies.items():
        if data["rating"] == best_rating:  # Prints all movies with the same best_rating
            print(f"Best movie: {data["title"]} ({data["year"]}), {best_rating:.1f}")

    # Worst movie based on ratings
    worst_rating = min(ratings)

    for name, data in movies.items():
        if data["rating"] == worst_rating:  # Prints all movies with the same worst_rating
            print(f"Worst movie: {data["title"]} ({data["year"]}), {worst_rating:.1f}")


def random_movie(movies):
    """Generates random movie from databank"""
    if not movies:
        print(colorize("No movies available!", "PINK"))
        return

    random_movie_choice = random.choice(list(movies.items()))
    print(
        f"Your movie to watch: {random_movie_choice[1]["title"]}({random_movie_choice[1]["year"]}), with the rating: {random_movie_choice[1]["rating"]} "
    )  # Getting the name and the matching rating


def search_for_movie(movies):
    """ Searches for search query of user in movie databank """
    #optionally let the user pick one to open/print details.
    while True:
        user_input_search_query = input(
            colorize("Enter part of movie name: ", "DARK_VIOLET")
        )
        if user_input_search_query == "":
            print("Please enter a valid movie name.")
        else:
            break
    # Normal search
    found_movies = []
    for id, data in movies.items():
        if user_input_search_query.lower() in data["title"].lower():
            found_movies.append(data["title"])
            print(f"{data["title"]} ({data["year"]}), rating: {data["rating"]}")

    # Fuzzy search if no exact matches found
    if not found_movies:
        print(colorize(f"The movie {user_input_search_query} does not exist.", "PINK"))
        matches = process.extract(user_input_search_query, movies.keys(), limit=3)

        for match, score in matches:
            if score > 60:  # Similarity %
                matched_movie = input(colorize(f"Did you mean: {match} (yes|no): ", "PINK"))
                if "y" in  matched_movie.lower():
                    print(f"{match} ({movies[match]["year"]}), rating: {movies[match]["rating"]}")


def sorted_movies_by_rating(movies):
    """Sorts movies by rating from top to flop"""
    for name, data in sorted(movies.items(), key=lambda x: x[1]["rating"], reverse=True):
        print(f"{data["title"]} ({data["year"]}), {data["rating"]}")

def sorted_movies_by_year(movies):
    """Sorts movies chronologically"""
    first_or_last = input("Do you want the latest movies first? (Yes/No): ")
    if "y" in first_or_last.lower():
        for name, data in sorted(movies.items(), key=lambda x: x[1]["year"], reverse=True):
            print(f"{data["title"]} ({data["year"]}), {data["rating"]}")

    elif "n" in first_or_last.lower():
        for name, data in sorted(movies.items(), key=lambda x: x[1]["year"], reverse=False):
            print(f"{data["title"]} ({data["year"]}): {data["rating"]}")
    else:
        print("No valid input was found.")
        return

def filter_movies(movies):
    """
    filters movies by 3 inputs
    1. minimal rating
    2. start year
    3. end year
    and prints an output at the end with those criteria
    """
    current_year = datetime.now().year

    while True:
        minimum_rating = input("Enter minimum rating (leave blank for no minimum rating): ")
        if minimum_rating == "":
            minimum_rating = 0
        else:
            try:
                minimum_rating = float(minimum_rating)
                if not 0 <= minimum_rating <= 10:
                    raise ValueError
            except ValueError:
                print("Please enter a valid number (0-10)")
                continue

        start_year = input("Enter start year (leave blank for no start year): ")
        end_year = input("Enter end year (leave blank for no end year): ")

        if start_year == "":
            start_year = 1895
        else:
            try:
                start_year = int(start_year)
            except ValueError:
                print("Please enter a valid year (YYYY)")
                break
        if end_year == "":
            end_year = current_year
        else:
            try:
                end_year = int(end_year)
            except ValueError:
                print("Please enter a valid year (YYYY)")
                break


        if start_year <= end_year:
            print(f"Filtered Movies:")
            for id, data in sorted(movies.items(), key=lambda x: float(x[1]["rating"][:-3]), reverse=True):
                if float(data["rating"][:-3]) >= minimum_rating and start_year <= data["year"] <= end_year:
                    print(f"{data["title"]} ({data["year"]}): {data["rating"]}")
        else:
            print()
            break
        return

def create_rating_histogram(movies):
    import matplotlib.pyplot as plt
    #Consider lazy import of matplotlib inside the function; handle empty dataset;
    # note that plt.show () blocks in some environments, saving alone might be sufficient.
    ratings = []
    if not movies:
        print(colorize("No movies available to create histogram.", "PINK"))
        return
    else:
        for name, data in movies.items():
            ratings.append(data["rating"])

    plt.figure(figsize=(8, 5))  # Size in inch width, height
    plt.hist(ratings, bins=10, color="blue")  # added other color
    plt.title("Rating histogram")  # Title of histogram
    plt.xlabel("Rating")  # X
    plt.ylabel("Count")  # Y
    plt.tight_layout()  # Automatically adjusts the spacing so that titles and axis labels are not cut off
    plt.savefig(
        "af_movie_databank_rating_histogram.png", dpi=150
    )  # Saves the histogram png under the name with the given resolution
    plt.show()  # Shows histogram



if __name__ == "__main__":
    main()
