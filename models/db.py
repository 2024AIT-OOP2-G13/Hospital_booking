from peewee import SqliteDatabase

# データベース接続の定義
db = SqliteDatabase('my_database.db', check_same_thread=False)