from sanic import Sanic, Blueprint
from tortoise.contrib.sanic import register_tortoise
import json
from api import api
from sanic_jwt_extended import JWT
from sanic_jwt_extended.blacklist import InMemoryBlacklist
from dotenv import load_dotenv
import os
import aioredis
app = Sanic(__name__)
app.blueprint(api)

load_dotenv()

register_tortoise(
        app,
        db_url=f"{os.getenv('DATABASE')}://{os.getenv('USERNAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB')}",
        modules={
            "models": ["api.v1.models"]},
        generate_schemas=True
    )


@app.listener("before_server_start")
async def before(app, loop):
    redis = aioredis.from_url('redis://localhost', decode_responses=True)
    app.REDIS = redis
    with JWT.initialize(app) as manager:
        manager.config.secret_key = os.getenv('SECRET')
        manager.config.use_blacklist = True
        manager.config.blacklist_class = InMemoryBlacklist


@app.listener("after_server_stop")
async def end(app, loop):
    await app.REDIS.close()


if __name__ == '__main__':
    app.run(debug=True)
