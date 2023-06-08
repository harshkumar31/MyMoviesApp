from tortoise import fields, Model
class History(Model):
    user = fields.ForeignKeyField('models.User', on_delete=fields.CASCADE, related_name="user_history")
    hist = fields.CharField(max_length=60, null=False)
    time_searched = fields.DatetimeField(auto_now_add=True)