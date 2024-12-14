from peewee import Model, CharField, ForeignKeyField, BooleanField
from models.db import db
from models.user import User

class MedicalCondition(Model):
    user = ForeignKeyField(User, backref='medical_conditions')
    fever = BooleanField(default=False)  # 発熱
    vomiting = BooleanField(default=False)  # 嘔吐
    headache = BooleanField(default=False)  # 頭痛
    dizziness = BooleanField(default=False)  # めまい
    other = BooleanField(default=False)  # その他

    class Meta:
        database = db
        table_name = 'medical_condition' 