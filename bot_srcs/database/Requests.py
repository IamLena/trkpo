from database.Models import *
from peewee import PeeweeException
from uuid import uuid4
import re


def is_valid_uuid(uuid_for_test: str):
    regex = re.compile(r'^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    return bool(regex.match(str(uuid_for_test)))


# Meeting
def add_meeting(name: str, administrator_username: str):
    try:
        if isinstance(name, str) and isinstance(administrator_username, str):
            meeting = Meeting.create(uid=uuid4(), name=name, administrator=administrator_username)
            result = meeting.uid
        else:
            result = -1
    except PeeweeException:
        result = -1
    return result


def meeting_add_start_time(meeting_id: str, start_time: str):
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
    questions = Question.select().where(Question.meeting_id == meeting)
    result = []
    for row in questions:
        result.append((row.question, row.selected_answer))
    return result


def parse_participants(meeting):
    participants = Participant.select().where(Participant.meeting_id == meeting)
    result = []
    for row in participants:
        result.append(row.user)
    return result


def get_meeting_info(meeting_id: str):
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
    try:
        if is_valid_uuid(meeting_id) and isinstance(participant_username, str):
            Participant.create(meeting_id=meeting_id, user=participant_username)
            result = 0
        else:
            result = -1
    except PeeweeException:
        result = -1
    return result


def get_meetings_by_user_id(user_username: str, administrator=0):
    try:
        if isinstance(user_username, str) and administrator in (0, 1):
            meetings = Meeting.select(Meeting.name,
                                      Meeting.uid).join(Participant).where(Participant.user == user_username)
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
    try:
        if is_valid_uuid(meeting_id):
            participants = Participant.select().where(Participant.meeting_id == meeting_id)
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


# Question
def add_question(meeting_id: str, question: str, options_list: str):
    try:
        if is_valid_uuid(meeting_id) and isinstance(question, str) and isinstance(options_list, str):
            new_question = Question.create(meeting_id=meeting_id, question=question, option_list=options_list)
            result = new_question.id
        else:
            result = -1
    except PeeweeException:
        result = -1
    return result


def get_meeting_questions(meeting_id: str):
    try:
        if is_valid_uuid(meeting_id):
            questions = Question.select().where(Question.meeting_id == meeting_id)
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
    try:
        if isinstance(question_id, int) and isinstance(selected_option, str):
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


# Answer
def add_answer(question_id: int, user_username: str, selected_option: str):
    try:
        if isinstance(question_id, int) and isinstance(user_username, str) and isinstance(selected_option, str):
            options = get_options_list(question_id)
            if selected_option not in options:
                raise PeeweeException
            Answer.create(question_id=question_id, user=user_username, selected_option=selected_option)
            result = 0
        else:
            result = -1
    except PeeweeException:
        result = -1
    return result


def get_answers(question_id: int):
    try:
        if isinstance(question_id, int):
            answers = Answer.select(Answer.selected_option,
                                    fn.COUNT(Answer.id).alias('quantity')
                                    ).where(Answer.question_id == question_id).group_by(Answer.selected_option)
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
