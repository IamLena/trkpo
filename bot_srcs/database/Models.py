from peewee import *

"""
Модели БД
"""

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


class Meeting(BaseModel):
    """Модель мероприятия

    Содержит информацию о мероприятии

    :param uid: идентификатор мероприятия (uuid v4)
    :type uid: UUID
    :param name: название мероприятия (макс. длина - 45 символов)
    :type name: str
    :param administrator: username организатора (макс. длина - 50 символов)
    :type administrator: str
    :param start_time: время начала мероприятия
    :type start_time: datetime
    :param place: место проведения мероприятия
    :type place: str
    :param duration: продолжительность мероприятия
    :type duration: time

    """
    uid = UUIDField(primary_key=True, unique=True)
    name = CharField(max_length=45)
    administrator = CharField(max_length=50)
    start_time = DateTimeField(null=True)
    place = CharField(max_length=45, null=True)
    duration = TimeField(null=True)


class Participant(BaseModel):
    """Модель участника

    Содержит информацию об участниках мероприятия.

    :param meeting_id: Идентификатор мероприятия
    :type meeting_id: UUID
    :param user: username участника
    :type user: str
    """
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
    """Модель вопроса

    Содержит информацию о вопросах мероприятия

    :param question: вопрос
    :type question: str
    :param option_list: варианты ответов (одна строка, через запятую)
    :type option_list: str
    :param meeting_id: идентификатор мероприятия
    :type meeting_id: UUID (foreign key)
    :param selected_answer: ответ, выбранный большинством после опросов
    :type selected_answer: str
    """
    question = CharField(max_length=45)
    option_list = CharField(max_length=100)
    meeting_id = ForeignKeyField(Meeting)
    selected_answer = CharField(max_length=50, null=True)

    class Meta:
        indexes = (
            (('meeting_id', 'question'), True),
        )


class Answer(BaseModel):
    """Модель ответа

    Содержит информацию об ответах на вопрос от пользователей

    :param question_id: id вопроса, на который отвечают
    :type question_id: int
    :param user: username пользователя, который отвечает
    :type user: str
    :param selected_option: выбранный ответ
    :type selected_option: str
    """
    question_id = ForeignKeyField(Question)
    user = CharField(max_length=50)
    selected_option = CharField(max_length=50)


def create_tables():
    """
    Создание таблиц
    """
    with db:
        db.create_tables([Meeting, Participant, Question, Answer])
