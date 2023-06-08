from tortoise import fields, Model
from uuid import uuid4


class List(Model):
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name="lists_details")
    list_id = fields.CharField(pk=True, max_length=36, default=uuid4())
    list_title = fields.CharField(max_length=30, null=False)
    list_created = fields.DatetimeField(auto_now_add=True)
    list_modified = fields.DatetimeField(auto_now=True)