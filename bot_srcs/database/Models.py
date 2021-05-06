from peewee import *

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Meeting(BaseModel):
    """Модель мероприятия
    Содержит информацию о мероприятии
    """
    #: UUID: идентификатор мероприятия (uuid v4)
    uid = UUIDField(primary_key=True, unique=True)
    # str: название мероприятия (макс. длина - 45 символов)
    name = CharField(max_length=45)
    # str: username администратора (макс. длина - 50 символов)
    administrator = CharField(max_length=50)
    # datetime: время начала мероприятия
    start_time = DateTimeField(null=True)
    # str: место проведения мероприятия
    place = CharField(max_length=45, null=True)
    # str: продолжительность мероприятия
    duration = TimeField(null=True)


class Participant(BaseModel):
    meeting_id = ForeignKeyField(Meeting, backref='meetings')
    user = CharField(max_length=50)

    class Meta:
        indexes = (
            (('meeting_id', 'user'), True),
        )

    class Meta:
        indexes = (
            (('meeting_id', 'user'), True),
        )


class Question(BaseModel):
    question = CharField(max_length=45)
    option_list = CharField(max_length=100)
    meeting_id = ForeignKeyField(Meeting)
    selected_answer = CharField(max_length=50, null=True)

    class Meta:
        indexes = (
            (('meeting_id', 'question'), True),
        )


class Answer(BaseModel):
    question_id = ForeignKeyField(Question)
    user = CharField(max_length=50)
    selected_option = CharField(max_length=50)


def create_tables():
    with db:
        db.create_tables([Meeting, Participant, Question, Answer])
