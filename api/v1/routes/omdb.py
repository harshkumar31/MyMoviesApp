from sanic import Blueprint, response
from sanic_jwt_extended import jwt_required
from api.v1.managers import SearchClass

searches = Blueprint("search", url_prefix="/search")
obj = SearchClass()


@searches.get("/")
@jwt_required
async def title(request, token):
    res = await obj.title(request, token)
    return response.json(res)


@searches.get("/id/<ids>")
@jwt_required
async def movie_id(request, token, ids):
    res = await obj.movie_id(request, token, ids)
    return response.json(res)


@searches.get("/all/")
@jwt_required
async def all_details(request, token):
    res = await obj.all_details(request, token)
    return response.json(res)


@searches.get("/history")
@jwt_required
async def history(request, token):
    res = await obj.history(request, token)
    return response.json(res)
