from sqlalchemy import create_engine, text
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

# Define the database URL
DB_URL = "sqlite:///movies.db"

# Create the engine
engine = create_engine(DB_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_image_url TEXT
        )
    """))
    connection.commit()


def fetch_movie(title):
    """Fetches data from API based on movie title"""
    URL = f"http://www.omdbapi.com/?apikey={API_KEY}&t=" + title

    result = {}
    try:
        res = requests.get(URL)
        if res.ok:
            result = res.json()
        else:
            print("Movie not found in OMDb.")

    except requests.exceptions.Timeout:
            print("Error: The request to OMDb timed out.")
            return {}

    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the OMDb API (no internet or server unreachable).")
        return {}

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error: {e}")
        return {}

    return result


def list_movies():
    """Retrieve all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(text("SELECT id, title, year, rating, poster_image_url FROM movies"))
        movies = result.fetchall()

    return {row[0]: {"title": row[1], "year": row[2], "rating": row[3], "poster": row[4]} for row in movies}


def add_movie(title):
    """Add a new movie to the database."""

    result = fetch_movie(title)
    title = result.get('Title')
    year = result.get('Year')
    rating = (
    result.get("Ratings", [{}])[0].get("Value")
    if result.get("Ratings")
    else None
)
    poster = result.get('Poster')

    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster_image_url) VALUES (:title, :year, :rating, :poster_image_url)"),
                               {"title": title, "year": year, "rating": rating, "poster_image_url": poster})
            connection.commit()

        except Exception as e:
            print(f"Error: {e}")


def delete_movie(id):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE id=:id"),
                               {"id": id})
            connection.commit()

            title = connection.execute(text("SELECT title FROM movies WHERE :id"))
            print(f"Movie '{title}' deleted successfully.")
        except Exception as e:
            print(f"Error: {e}")


def update_movie(id, title, rating):
    """Update a movie's rating in the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET title = :title, rating = :rating WHERE id = :id"),
                               {"id": id, "title": title, "rating": rating})
            connection.commit()
            print(f"Movie '{title}' updated successfully.")
        except Exception as e:
            print(f"Error: {e}")

