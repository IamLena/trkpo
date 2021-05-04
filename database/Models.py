from peewee import *

db = SqliteDatabase('lets.db')


class BaseModel(Model):
    class Meta:
        database = db


class Meeting(BaseModel):
    uid = UUIDField(primary_key=True, unique=True)
    name = CharField(max_length=45)
    administrator_id = IntegerField()
    start_time = DateTimeField(null=True)
    place = CharField(max_length=45, null=True)
    duration = TimeField(null=True)


class Participant(BaseModel):
    meeting_id = ForeignKeyField(Meeting, backref='meetings')
    user_id = IntegerField()


class Question(BaseModel):
    question = CharField(max_length=45)
    option_list = CharField(100)
    meeting_id = ForeignKeyField(Meeting)
    selected_answer = CharField(max_length=50, null=True)


class Answer(BaseModel):
    question_id = ForeignKeyField(Question)
    user_id = IntegerField()
    selected_option = CharField(max_length=50)


def create_tables():
    with db:
        db.create_tables([Meeting, Participant, Question, Answer])
