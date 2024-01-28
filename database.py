import peewee


db = peewee.SqliteDatabase('users.db')


class User(peewee.Model):
    id = peewee.CharField()
    name = peewee.CharField()
    rank = peewee.IntegerField()
    exp = peewee.IntegerField()
    admin = peewee.BooleanField()
    warns = peewee.IntegerField()
    state = peewee.IntegerField()
    
    class Meta:
        database = db
        