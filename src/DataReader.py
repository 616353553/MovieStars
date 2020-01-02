from Actor import Actor
from Movie import Movie
from Starring import Starring
import json
from pprint import pprint


actors = []
movies = []
starrings = []


def gross_value(movie_name):
    for movie in movies:
        if movie.movie_name == movie_name:
            return movie.gross_value
    return "N/A"


def participate(actor_name):
    movie_names = []
    for starring in starrings:
        if starring.actor_name == actor_name:
            movie_names.append(starring.movie_name)
    return movie_names


def cast(movie_name):
    actor_names = []
    for starring in starrings:
        if starring.movie_name == movie_name:
            actor_names.append(starring.actor_name)
    return actor_names


def top_gross_actors(rank):
    movie_gross_values = {}
    actor_gross_values = {}
    for movie in movies:
        movie_gross_values[movie.movie_name] = movie.gross_value
    for starring in starrings:
        actor_name = starring.actor_name
        gross_value = movie_gross_values[starring.movie_name]
        if actor_name in actor_gross_values:
            actor_gross_values[actor_name] += gross_value
        else:
            actor_gross_values[actor_name] = gross_value
    return sorted(actor_gross_values.items(), key=lambda x: x[1], reverse=True)[:rank]



def olderest_actors(rank):
    actor_ages = {}
    for actor in actors:
        actor_ages[actor.actor_name] = actor.birth_year
    return sorted(actor_ages.items(), key=lambda x: x[1], reverse=True)[:rank]



def movies_for_year(year):
    movie_names = []
    for movie in movies:
        if movie.release_year == year:
            movie_names.append(movie.movie_name)
    return movie_names


def actors_for_year(year):
    actor_names = []
    for actor in actors:
        if actor.birth_year == year:
            actor_names.append(actor.actor_name)
    return actor_names




if __name__ == "__main__":
    with open('data.json') as f:
        data = json.load(f)

    for actor in data["actors"]:
        actors.append(Actor(data=actor))

    for movie in data["movies"]:
        movies.append(Movie(data=movie))

    for starring in data["starrings"]:
        starrings.append(Starring(data=starring))

    print(len(actors))
    print(len(starrings))
    print(len(movies))
    print(gross_value("Iron Man"))
    print(participate("Robert Downey Jr."))
    print(cast("Iron Man"))
    print(top_gross_actors(5))
    print(olderest_actors(2))
    print(movies_for_year("2016"))
    print(actors_for_year("1959"))





