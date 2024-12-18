from peewee import Model, ForeignKeyField, BooleanField
from .db import db
from .user import User

class Jibyou(Model):
    user = ForeignKeyField(User, backref='jibyou')
    check = BooleanField()

    class Meta:
        database = db
