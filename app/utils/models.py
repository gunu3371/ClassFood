from tortoise import fields
from tortoise.models import Model


class Meal(Model):
    date = fields.CharField(max_length=10)
    region_code = fields.CharField(max_length=30)
    school_code = fields.CharField(max_length=30)
    diet = fields.JSONField()
    origin = fields.JSONField()
    cal = fields.CharField(max_length=20)
    antelope = fields.JSONField()
