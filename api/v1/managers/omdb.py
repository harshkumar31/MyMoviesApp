import os
from urllib.request import urlopen
import json
import aiohttp
import asyncio
from api.v1.models import History
from datetime import timedelta

URL = f"http://www.omdbapi.com/?apikey={os.getenv('API_KEY')}"


class SearchClass:

    async def title(self, request, token):
        url = URL
        src = ""
        for key, value in request.args.items():
            if key == "title":
                src = value[0]
                url += f"&s={value[0]}"
            elif key == "year":
                url += f"&y={value[0]}"
            elif key == "type":
                url += f"&type={value[0]}"
            elif key == "page":
                url += f"&page={value[0]}"

        await History.create(user_id=token.identity, hist=src)
        res = urlopen(url)
        json_data = json.loads(res.read())
        if json_data['Response'] == "True":
            data = json_data["Search"]
            return {"data": data, "success": True}
        else:
            return {"error": {
                "message": json_data["Error"]},
                "status_code": 400,
                "success": False}

    async def movie_id(self, request, token, ids):
        await History.create(user_id=token.identity, hist=ids)
        redis = request.app.REDIS
        jns = await redis.get(ids)
        if jns is None:
            url = URL + f"&i={ids}"
            res = urlopen(url)
            json_data = json.loads(res.read())
            await redis.set(ids, json.dumps(json_data))
            await redis.expire(ids, timedelta(minutes=10))
            print("not from cache")
        else:
            json_data = json.loads(jns)
            print("from cache")
        if json_data['Response'] == "True":
            dict = {"data": json_data, "success": True}
        else:
            dict = {"error": {
                "message": json_data["Error"]},
                "status_code": 400,
                "success": False}
        return dict

    async def all_details(self, request, token):
        url = URL
        src = ""
        for key, value in request.args.items():
            if key == "title":
                src = value[0]
                url += f"&s={value[0]}"
            elif key == "year":
                url += f"&y={value[0]}"
            elif key == "type":
                url += f"&type={value[0]}"
            elif key == "page":
                url += f"&page={value[0]}"

        await History.create(user_id=token.identity, hist=src)
        res = urlopen(url)
        json_data = json.loads(res.read())
        print(json_data)
        if json_data['Response'] == "True":
            json_search = json_data['Search']
            data = await self.extra_func(json_search, request)
            return {"data": data, "success": True}
        else:
            return {"error": {
                "message": json_data["Error"]},
                "status_code": 400,
                "success": False}

    async def get_tasks(self, session, data):
        # tasks = []
        # for rw in data:
        omdbId = data['imdbID']
        # url = f"http://www.omdbapi.com/?i={omdbId}&apikey=4c92cc0a"
        url = URL + f"&i={omdbId}"
        return session.get(url, ssl=False)
        # return tasks

    async def extra_func(self, data, request):
        lsc = []
        redis = request.app.REDIS
        new_data = []
        for movie in data:
            fetched_movie = await redis.get(movie['imdbID'])
            if fetched_movie is None:
                new_data.append(movie)
            else:
                lsc.append(json.loads(fetched_movie))

        if len(new_data) > 1:
            async with aiohttp.ClientSession() as session:
                tasks = await asyncio.gather(
                    *[self.get_tasks(session, movie) for movie in new_data]
                )
                responses = await asyncio.gather(*tasks)
            pipe1 = redis.pipeline(transaction=True)
            for res in responses:
                data1 = await res.json()
                await pipe1.set(data1['imdbID'], json.dumps(data1))
                await pipe1.expire(data1['imdbID'], timedelta(minutes=10))
                lsc.append(data1)
            await pipe1.execute()

        return lsc

    async def history(self, request, token):
        user_id = token.identity
        hist = await History.filter(user_id=user_id)
        lst = []
        for his in hist:
            lst.append(his.hist)
        return {"data": lst, "success": True}
