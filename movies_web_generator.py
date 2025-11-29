
def serialize_movie(movies):
    output = ""

    for id, data in movies.items():
        title = data["title"]
        year = data["year"]
        poster = data["poster"]
        rating = data["rating"]

        output += "<li>\n <div class='movie'>\n"

        if poster:
            output += f"<img class='movie-poster' src='{poster}' title>\n"
        if title:
            output += f"<div class='movie-title'>{title}</div>\n"
        if year:
            output += f"<div class='movie-year'>{year}</div>\n"
        if rating:
            output += f"<div class='movie-rating'>Rating: {rating}</div>\n"

        output += '</div>\n </li>\n'

    return output


def load_html(file_path):
    with open(file_path, "r") as file:
        return file.read()


def write_html(movies,html):

    output = serialize_movie(movies)

    html = html.replace("__TEMPLATE_TITLE__", "My Movie Collection")
    html = html.replace("__TEMPLATE_MOVIE_GRID__", output)

    with open("_static/index.html", "w") as file:
        file.write(html)


def main(movies):

    html = load_html("_static/index_template.html")
    write_html(movies,html)
    print("Website was successfully generated to the file index.html.")


if __name__ == "__main__":
    main()