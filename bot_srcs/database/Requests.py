from database.Models import *
from peewee import PeeweeException
from uuid import uuid4


def add_meeting(name: str, administrator_id: int):
    try:
        meeting = Meeting.create(uid=uuid4(), name=name, administrator_id=administrator_id)
        result = meeting.uid
    except PeeweeException as exc:
        print(exc)
        result = -1
    return result


def meeting_add_start_time(meeting_id, start_time):
    try:
        meeting = Meeting.get_by_id(meeting_id)
        meeting.start_time = start_time
        meeting.save()
        result = 0
    except PeeweeException or DoesNotExist:
        result = -1
    return result


def meeting_add_duration(meeting_id, duration):
    try:
        meeting = Meeting.get_by_id(meeting_id)
        meeting.duration = duration
        meeting.save()
        result = 0
    except PeeweeException or DoesNotExist:
        result = -1
    return result


def meeting_add_place(meeting_id, place):
    try:
        meeting = Meeting.get_by_id(meeting_id)
        meeting.place = place
        meeting.save()
        result = 0
    except PeeweeException or DoesNotExist:
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
        result.append(row.user_id)
    return result


def get_meeting_info(meeting_id):
    try:
        meeting = Meeting.get_by_id(meeting_id)
        result = {'id': meeting.uid,
                  'name': meeting.name,
                  'administrator_id': meeting.administrator_id,
                  'start_time': meeting.start_time,
                  'duration': meeting.duration,
                  'place': meeting.place,
                  'questions': parse_questions_answers(meeting),
                  'participants': parse_participants(meeting)}
    except PeeweeException or DoesNotExist:
        result = {}
    return result


def add_participant(meeting_id, participant_id):
    try:
        Participant.create(meeting_id=meeting_id, user_id=participant_id)
        result = 0
    except PeeweeException:
        result = -1
    return result


def get_meetings_by_user_id(user_id, administrator=0):
    try:
        meetings = Meeting.select(Meeting.name, Meeting.uid).join(Participant).where(Participant.user_id == user_id)
        result = []
        for meeting in meetings:
            if administrator != 0:
                if meeting.administrator_id == user_id:
                    result.append((meeting.name, meeting.uid))
            else:
                result.append((meeting.name, meeting.uid))
    except PeeweeException or DoesNotExist:
        result = []
    return result


def get_participants(meeting_id):
    try:
        participants = Participant.select().where(Participant.meeting_id == meeting_id)
        result = []
        for row in participants:
            result.append(row.user_id)
    except PeeweeException or DoesNotExist:
        result = []
    return result


def add_question(meeting_id, question, options_list):
    try:
        new_question = Question.create(meeting_id=meeting_id, question=question, option_list=options_list)
        result = new_question.id
    except PeeweeException as exc:
        print(exc)
        result = -1
    return result


def get_meeting_questions(meeting_id):
    try:
        questions = Question.select().where(Question.meeting_id == meeting_id)
        result = []
        for row in questions:
            result.append(row.id)
    except PeeweeException or DoesNotExist:
        result = []
    return result


def get_options_list(question_id):
    try:
        question = Question.get_by_id(question_id)
        result = question.option_list.split(sep=', ')
    except PeeweeException or DoesNotExist:
        result = []
    return result


def select_option(question_id, selected_option):
    try:
        question = Question.get_by_id(question_id)
        question.selected_answer = selected_option
        question.save()
        result = 0
    except PeeweeException or DoesNotExist:
        result = -1
    return result


def add_answer(question_id, user_id, selected_option):
    try:
        options = get_options_list(question_id)
        if selected_option not in options:
            raise PeeweeException
        answer = Answer.create(question_id=question_id, user_id=user_id, selected_option=selected_option)
        result = 0
    except PeeweeException:
        result = -1
    return result


def get_answers(question_id):
    try:
        answers = Answer.select(Answer.selected_option,
                                fn.COUNT(Answer.id).alias('quantity')
                                ).where(Answer.question_id == question_id).group_by(Answer.selected_option)
        result = []
        for answer in answers:
            result.append((answer.selected_option, answer.quantity))
    except PeeweeException or DoesNotExist:
        result = []
    return result
