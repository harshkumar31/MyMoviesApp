from sanic import Blueprint, response
from sanic_jwt_extended import jwt_required
from api.v1.managers import ListClass

lists = Blueprint("lists", url_prefix="/mylists")
obj = ListClass()

# GET api/v1/mylists/all → Get a list of all my lists
@lists.get("/all")
@jwt_required
async def list_of_lists(request, token):
    res = await obj.list_of_lists(request,token)
    return response.json(res)


# GET api/v1/mylists/<list-id>
@lists.get("/<id>")
@jwt_required()
async def list_details(request, token, id):
    res = await obj.list_details(request,token,id)
    return response.json(res)


# POST api/v1/mylists
@lists.post("/")
@jwt_required()
async def create_list(request, token):
    res = await obj.create_list(request,token)
    return response.json(res)


# PUT api/v1/mylists/<list-id>
@lists.put("/<id>")
@jwt_required()
async def update_list(request, token, id):
    res = await obj.update_list(request,token,id)
    return response.json(res)


# DELETE api/v1/mylists
@lists.delete("/")
@jwt_required()
async def delete_list(request, token):
    res = await obj.delete_list(request,token)
    return response.json(res)


