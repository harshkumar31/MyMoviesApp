from api.v1.models import List
from tortoise.timezone import datetime
from uuid import uuid4


class ListClass:

    async def list_of_lists(self, request, token):
        userid = token.identity
        data = await List.filter(user_id=userid)
        lst = []
        for row in data:
            ls = {}
            ls["title"] = row.list_title
            ls["list_id"] = row.list_id
            lst.append(ls)
        return {"data": lst,
                "success": True}

    async def list_details(self, request, token, id):
        data = await List.get_or_none(list_id=id)
        if data:
            ls = {}
            ls["title"] = data.list_title
            ls["list_id"] = data.list_id
            ls["list_created"] = str(data.list_created)
            ls["list_modified"] = str(data.list_modified)
            return {"data": ls, "success": True}
        return {"error": {
            "error": {
                "message": "List does not exists",
                "details": "List with the given id does not exists"
            },
            "status_code": 404,
            "success": False
        }}

    async def create_list(self, request, token):
        name = request.json.get("name", None)
        user_id = token.identity
        lst = await List.filter(user_id=user_id, list_title=name)
        if lst:
            return {"error": {
                "error": {
                    "message": "List already exists",
                    "details": "Lists with same name cannot be created"
                },
                "status_code": 409,
                "success": False
            }}
        await List.create(list_id=str(uuid4()), list_title=name, user_id=user_id)
        return {"data": f"List {name} created",
                "success": True}

    async def update_list(self, request, token, id):
        nme = request.json.get("name", None)
        user_id = token.identity
        lst = await List.filter(user_id=user_id, list_title=nme)
        if lst:
            return {"error": {
                "error": {
                    "message": "List name already exists",
                    "details": "Lists with same name cannot be create"
                },
                "status_code": 409,
                "success": False
            }}
        await List.filter(list_id=id).update(list_title=nme, list_modified=datetime.now())
        return {"data": "list details updated",
                "success": True}

    async def delete_list(self, request, token):
        name = request.json.get("name", None)
        user_id = token.identity
        lst = await List.get_or_none(user_id=user_id, list_title=name)
        if lst is None:
            return {"error": {
                "error": {
                    "message": "List does not exist",
                    "details": "List which is not present, cant be deleted"
                },
                "status_code": 404,
                "success": False
            }}
        # await List.filter(list_id=lst.list_id).delete()
        await lst.delete()
        return {"data": f"List {name} deleted",
                "success": True}
