from peewee import *
from .db import db
from .user import User

class Appointment(Model):
    user = ForeignKeyField(User, backref='appointments')  # user_idではなくuserとして定義
    appointment_datetime = DateTimeField()
    department = CharField()

    class Meta:
        database = db 