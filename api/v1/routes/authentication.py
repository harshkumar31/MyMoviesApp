from sanic import Blueprint, response
from sanic_jwt_extended import jwt_required, JWT
from api.v1.managers import AuthClass

auth = Blueprint("auth")

obj = AuthClass()


@auth.post("/login")
async def authenticate(request):
    res = await obj.authenticate(request)
    return response.json(res)


@auth.post("/logout")
@jwt_required
async def logout(request, token):
    await JWT.revoke(token)
    return response.json({"data": "Logged out",
                          "success": True})


@auth.post('/signup')
async def register_user(request):
    res = await obj.register_user(request)
    return response.json(res)
