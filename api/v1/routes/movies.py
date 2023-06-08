from sanic import Blueprint, response
from sanic_jwt_extended import jwt_required
from api.v1.managers import MovieClass

movie = Blueprint("movies", url_prefix="/movies")
obj = MovieClass()


# POST api/v1/movies → Add a movie to a list
@movie.post("/")
@jwt_required
async def add_movie(request, token):
    res = await obj.add_movie(request, token)
    return response.json(res)


# DELETE api/v1/movies → Remove a movie from a list
@movie.delete("/")
@jwt_required
async def remove_movie(request, token):
    res = await obj.remove_movie(request, token)
    return response.json(res)


# GET api/v1/movies/?list_name=<list_name>  → get a list of all the movies in a list
@movie.get("/")
@jwt_required
async def movies_in_list(request, token):
    res = await obj.movies_in_list(request, token)
    return response.json(res)
