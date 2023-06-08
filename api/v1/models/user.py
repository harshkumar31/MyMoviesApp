from tortoise import fields, Model
from uuid import uuid4


class User(Model):
    user_id = fields.CharField(pk=True, max_length=36, default=uuid4())
    email = fields.CharField(unique=True, max_length=30, null=False)
    password_hash = fields.CharField(max_length=150, null=False)
    first_name = fields.CharField(max_length=30, null=False)
    last_name = fields.CharField(max_length=30, null=False)
    user_created = fields.DatetimeField(auto_now_add=True)

    def __json__(self):
        return {
            'user_id': self.user_id
        }

    def to_dict(self):
        return {
            'user_id': self.user_id
        }