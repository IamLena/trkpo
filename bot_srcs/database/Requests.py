from database.Models import *
from peewee import PeeweeException
from uuid import uuid4
import re

"""
Запросы к базе данных
"""


def is_valid_uuid(uuid_for_test: str):
    """
    Проверка правильность строки в формате uuid v4

    :param uuid_for_test: строка, которую нужно проверить
    :type uuid_for_test: str
    :return: True, если строка соответствует формату, иначе - False
    :rtype: bool
    """
    regex = re.compile(r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab]'
                       r'[a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    return bool(regex.match(str(uuid_for_test)))


# Meeting
def add_meeting(name: str, administrator_username: str):
    """
    Добавление нового мероприятия

    :param name: название мероприятия
    :type name: str
    :param administrator_username: username организатора
    :type name: str
    :return: -1, если при добавлении произошла ошибка,
    если успешно, то uid нового мероприятия
    """
    try:
        if isinstance(name, str) and isinstance(administrator_username, str):
            meeting = Meeting.create(uid=uuid4(), name=name,
                                     administrator=administrator_username)
            result = meeting.uid
        else:
            result = -1
    except PeeweeException:
        result = -1
    return result


def meeting_add_start_time(meeting_id: str, start_time: str):
    """
    Добавление даты и времени начала мероприятия

    :param meeting_id: идентификатор мероприятия
    :type meeting_id: str
    :param start_time: дата и время начала
    :type start_time: str
    :return: -1, если возникла ошибка, 0 - успех
    :rtype: int
    """
    try:
        if is_valid_uuid(meeting_id) and isinstance(start_time, str):
            meeting = Meeting.get_by_id(meeting_id)
            meeting.start_time = start_time
            meeting.save()
            result = 0
        else:
            result = -1
    except PeeweeException:
        result = -1
    except DoesNotExist:
        result = -1
    return result


def meeting_add_duration(meeting_id: str, duration: str):
    """
    Добавление продолжительности мероприятия

    :param meeting_id: идентификатор мероприятия
    :type meeting_id: str
    :param duration: продолжительность мероприятия
    :type duration: str
    :return: -1, если возникла ошибка, 0 - успех
    :rtype: int
    """
    try:
        if is_valid_uuid(meeting_id) and isinstance(duration, str):
            meeting = Meeting.get_by_id(meeting_id)
            meeting.duration = duration
            meeting.save()
            result = 0
        else:
            result = -1
    except PeeweeException:
        result = -1
    except DoesNotExist:
        result = -1
    return result


def meeting_add_place(meeting_id: str, place: str):
    """
    Добавление даты и времени начала мероприятия

    :param meeting_id: идентификатор мероприятия
    :type meeting_id: str
    :param place: место
    :type place: str
    :return: 0 - успех, -1, если возникла ошибка
    :rtype: int
    """
    try:
        if is_valid_uuid(meeting_id) and isinstance(place, str):
            meeting = Meeting.get_by_id(meeting_id)
            meeting.place = place
            meeting.save()
            result = 0
        else:
            result = -1
    except PeeweeException:
        result = -1
    except DoesNotExist:
        result = -1
    return result


def parse_questions_answers(meeting):
    """
    Вспомогательная функция
    """
    questions = Question.select().where(Question.meeting_id == meeting)
    result = []
    for row in questions:
        result.append((row.question, row.selected_answer))
    return result


def parse_participants(meeting):
    """
    Вспомогательная функция
    """
    participants = Participant.select().\
        where(Participant.meeting_id == meeting)
    result = []
    for row in participants:
        result.append(row.user)
    return result


def get_meeting_info(meeting_id: str):
    """
    Получение информации о мероприятии

    :param meeting_id: идентификатор мероприятия
    :type meeting_id: str
    :return: возвращает словарь, где ключи - это атрибуты мероприятия:
    'id' - uid мероприятия (str);
    'name' - название мероприятия (str);
    'administrator' - username организатора (str);
    'start_time' - дата и время начала мероприятия (str);
    'duration' - продолжительность (str);
    'place' - место проведения (str);
    'questions' - вопросы мероприятия ([(question, selected answer), (), ...]);
    'participants' - участники мероприятия ([user_name1, user_name2, ...]).
    Пустой словарь, если возникла ошибка.
    :rtype: dict
    """
    try:
        if is_valid_uuid(meeting_id):
            meeting = Meeting.get_by_id(meeting_id)
            result = {'id': str(meeting.uid),
                      'name': meeting.name,
                      'administrator': meeting.administrator,
                      'start_time': str(meeting.start_time),
                      'duration': str(meeting.duration),
                      'place': meeting.place,
                      'questions': parse_questions_answers(meeting),
                      'participants': parse_participants(meeting)}
        else:
            result = {}
    except PeeweeException:
        result = {}
    except DoesNotExist:
        result = {}
    return result


# Participant
def add_participant(meeting_id: str, participant_username: str):
    """
    Добавление участников мероприятия

    :param meeting_id: идентификатор мероприятия
    :type meeting_id: str
    :param participant_username: username частника
    :type participant_username: str
    :return: -1, если возникла ошибка,
    -2, если участник уже состоит в мероприятии,
     0 - учестник успешно добавлен
    :rtype: int
    """
    try:
        if is_valid_uuid(meeting_id) and isinstance(participant_username, str):
            Participant.create(meeting_id=meeting_id,
                               user=participant_username)
            result = 0
        else:
            result = -1
    except PeeweeException as exc:
        if exc.args[0] == 'UNIQUE constraint failed: ' \
                          'participant.meeting_id, participant.user':
            result = -2
        else:
            result = -1
    return result


def get_meetings_by_user_id(user_username: str, administrator=0):
    """
    Получение списка всех мероприятий, в которых участвует пользователь

    :param user_username: username пользователя
    :type user_username: str
    :param administrator: тип запроса:
    0 - мероприятия, в которых пользователь просто участник,
    1 - мероприятия, в которых пользователь организатор
    :type administrator: (0, 1)
    :return: список мероприятий, если ошибка, то []
    :rtype: list
    """
    try:
        if isinstance(user_username, str) and administrator in (0, 1):
            meetings = Meeting.select(Meeting.name,
                                      Meeting.uid).join(Participant).\
                where(Participant.user == user_username)
            result = []
            for meeting in meetings:
                if administrator != 0:
                    if meeting.administrator == user_username:
                        result.append((meeting.name, meeting.uid))
                else:
                    result.append((meeting.name, meeting.uid))
        else:
            result = []
    except PeeweeException:
        result = []
    except DoesNotExist:
        result = []
    return result


def get_participants(meeting_id: str):
    """
    Получение списка всех участников мероприятия

    :param meeting_id: идентификатор мероприятия
    :type meeting_id: str
    :return: список username участников, если ошибка, то []
    :rtype: list
    """
    try:
        if is_valid_uuid(meeting_id):
            participants = Participant.select().\
                where(Participant.meeting_id == meeting_id)
            result = []
            for row in participants:
                result.append(row.user)
        else:
            result = []
    except PeeweeException:
        result = []
    except DoesNotExist:
        result = []
    return result


def is_administrator(meeting_id: str, user_name: str):
    """
    Проверка, является ли пользователем организатором указанного мероприятия

    :param user_name: username пользователя
    :type user_name: str
    :param meeting_id: идентификатор мероприятия
    :type meeting_id: str
    :return: True, если является, иначе - False
    :rtype: bool
    """
    try:
        if is_valid_uuid(meeting_id):
            meeting = Meeting.get_by_id(meeting_id)
            if meeting.administrator == user_name:
                result = True
            else:
                result = False
        else:
            result = False
    except PeeweeException:
        result = False
    except DoesNotExist:
        result = False
    return result


# Question
def add_question(meeting_id: str, question: str, options_list: str):
    """
    Добавление вопроса к мероприятию

    :param question: вопрос
    :type question: str
    :param meeting_id: идентификатор мероприятия
    :type meeting_id: str
    :param options_list: варианты ответа (через запятую)
    :type options_list: str
    :return: id нового вопроса,
     -2 если такой вопрос уже есть для этого мероприятия,
     -1 в случае ошибки
    :rtype: int
    """
    try:
        if is_valid_uuid(meeting_id) and isinstance(question, str) and \
                isinstance(options_list, str):
            new_question = Question.create(meeting_id=meeting_id,
                                           question=question,
                                           option_list=options_list)
            result = new_question.id
        else:
            result = -1
    except PeeweeException as exc:
        if exc.args[0] == 'UNIQUE constraint failed: ' \
                          'question.meeting_id, question.question':
            result = -2
        else:
            result = -1
    return result


def get_meeting_questions(meeting_id: str):
    """
    Получение списка id всех вопросов мероприятия

    :param meeting_id: идентификатор мероприятия
    :type meeting_id: str
    :return: список id вопросов, если ошибка, то []
    :rtype: list
    """
    try:
        if is_valid_uuid(meeting_id):
            questions = Question.select().\
                where(Question.meeting_id == meeting_id)
            result = []
            for row in questions:
                result.append(row.id)
        else:
            result = []
    except PeeweeException:
        result = []
    except DoesNotExist:
        result = []
    return result


def get_options_list(question_id: int):
    """
    Получение списка всех вариантов ответа на вопрос

    :param question_id: идентификатор вопроса
    :type question_id: str
    :return: список ответов, если ошибка, то []
    :rtype: list
    """
    try:
        if isinstance(question_id, int):
            question = Question.get_by_id(question_id)
            result = question.option_list.split(sep=', ')
        else:
            result = []
    except PeeweeException:
        result = []
    except DoesNotExist:
        result = []
    return result


def select_option(question_id: int, selected_option: str):
    """
    Выбор варианта ответа вопроса (после опросов)

    :param question_id: идентификатор вопроса
    :type question_id: str
    :param selected_option: выбранный ответ
    :type selected_option: str
    :return: 0 - успех, иначе -1
    :rtype: int
    """
    try:
        if isinstance(question_id, int) and \
                isinstance(selected_option, str):
            options = get_options_list(question_id)
            if selected_option not in options:
                raise PeeweeException
            question = Question.get_by_id(question_id)
            question.selected_answer = selected_option
            question.save()
            result = 0
        else:
            result = -1
    except PeeweeException:
        result = -1
    except DoesNotExist:
        result = -1
    return result


def get_question_by_id(question_id: int):
    """
    Получение текста вопроса по его id

    :param question_id: идентификатор вопроса
    :type question_id: str
    :return: в случае успеха - текст вопроса, иначе - пустая строка
    :rtype: str
    """
    try:
        if isinstance(question_id, int):
            question = Question.get_by_id(question_id)
            result = question.question
        else:
            result = ''
    except PeeweeException:
        result = ''
    except DoesNotExist:
        result = ''
    return result


# Answer
def add_answer(question_id: int, user_username: str, selected_option: str):
    """
    Добавление ответа

    :param question_id: идентификатор вопроса
    :type question_id: str
    :param user_username: username пользователя
    :type user_username: str
    :param selected_option: выбранный ответ
    :type selected_option: str
    :return: 0 - в случае успеха, -1 иначе
    :rtype: int
    """
    try:
        if isinstance(question_id, int) and \
                isinstance(user_username, str) and \
                isinstance(selected_option, str):
            options = get_options_list(question_id)
            if selected_option not in options:
                raise PeeweeException
            Answer.create(question_id=question_id,
                          user=user_username,
                          selected_option=selected_option)
            result = 0
        else:
            result = -1
    except PeeweeException:
        result = -1
    return result


def get_answers(question_id: int):
    """
    Получение количества каждого из ответов на вопрос

    :param question_id: идентификатор вопроса
    :type question_id: str
    :return: [(answer1, quantity1), ((answer2, quantity2)), ...] - успех,
    иначе - []
    :rtype: list
    """
    try:
        if isinstance(question_id, int):
            answers = Answer.select(Answer.selected_option,
                                    fn.COUNT(Answer.id).alias('quantity')
                                    ).\
                where(Answer.question_id == question_id).\
                group_by(Answer.selected_option)
            result = []
            for answer in answers:
                result.append((answer.selected_option, answer.quantity))
        else:
            result = []
    except PeeweeException:
        result = []
    except DoesNotExist:
        result = []
    return result
