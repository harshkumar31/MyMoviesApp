from tortoise import fields, Model


class Movie(Model):
    list = fields.ForeignKeyField('models.List', on_delete=fields.CASCADE, related_name="lists")
    movie_id = fields.CharField(max_length=30, null=False)
    movie_title = fields.CharField(max_length=200, null=False)