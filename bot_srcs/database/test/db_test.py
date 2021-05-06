import unittest
from database.Requests import *
from database.CreateDB import initialization
import os


meetings = []
test_name = 'название 1'
test_administrator = '@234567'
test_start_time = '23:30'
test_duration = '3'
test_place = 'дом'
test_qid = []


class TestMeetingModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initialization('test_lets.db')
        meeting1 = add_meeting('Тестовое мероприятие 1', '@111')
        meeting2 = add_meeting('Тестовое мероприятие 2', '@222')
        meetings.append(meeting1)
        meetings.append(meeting2)

    @classmethod
    def tearDownClass(cls):
        db.close()
        os.remove('test_lets.db')
        meetings.clear()

    def test_add_meeting_positive(self):
        before_count = len(Meeting.select())
        uid = add_meeting(test_name, test_administrator)

        self.assertTrue(uid != -1)
        self.assertTrue(is_valid_uuid(uid))
        self.assertEqual(len(Meeting.select()), before_count + 1)
        meetings.append(uid)

    def test_add_meeting_negative(self):
        name = 'название 2'
        administrator = 111
        len_before = len(Meeting.select())

        uid = add_meeting(name, administrator)

        self.assertEqual(uid, -1)
        self.assertEqual(len(Meeting.select()), len_before)

    def test_add_meeting_negative2(self):
        name = 123
        administrator = '@123'
        len_before = len(Meeting.select())

        uid = add_meeting(name, administrator)

        self.assertEqual(uid, -1)
        self.assertEqual(len(Meeting.select()), len_before)

    def test_meeting_add_start_time_positive(self):
        uid = meetings[0]

        result = meeting_add_start_time(uid, test_start_time)

        self.assertEqual(result, 0)
        self.assertEqual(str(Meeting.get_by_id(uid).start_time), test_start_time)

    def test_meeting_add_start_time_negative(self):
        start_time = 1234456
        uid = meetings[1]

        result = meeting_add_start_time(uid, start_time)

        self.assertEqual(result, -1)
        self.assertEqual(Meeting.get_by_id(uid).start_time, None)

    def test_meeting_add_start_time_negative2(self):
        start_time = '12'
        uid = 'kek'

        result = meeting_add_start_time(uid, start_time)

        self.assertEqual(result, -1)

    def test_meeting_add_start_time_negative3(self):
        start_time = '12'
        uid = '16fd2706-8baf-433b-82eb-8c7fada847da'

        result = meeting_add_start_time(uid, start_time)

        self.assertEqual(result, -1)

    def test_meeting_add_duration_positive(self):
        uid = meetings[0]

        result = meeting_add_duration(uid, test_duration)

        self.assertEqual(result, 0)
        self.assertEqual(str(Meeting.get_by_id(uid).duration), test_duration)

    def test_meeting_add_duration_negative(self):
        duration = 2
        uid = meetings[1]

        result = meeting_add_duration(uid, duration)

        self.assertEqual(result, -1)
        self.assertEqual(Meeting.get_by_id(uid).duration, None)

    def test_meeting_add_duration_negative2(self):
        duration = '3'
        uid = 'kek'

        result = meeting_add_duration(uid, duration)

        self.assertEqual(result, -1)

    def test_meeting_add_duration_negative3(self):
        duration = '2'
        uid = '16fd2706-8baf-433b-82eb-8c7fada847da'

        result = meeting_add_duration(uid, duration)

        self.assertEqual(result, -1)

    def test_meeting_add_place_positive(self):
        uid = meetings[0]

        result = meeting_add_place(uid, test_place)

        self.assertEqual(result, 0)
        self.assertEqual(Meeting.get_by_id(uid).place, test_place)

    def test_meeting_add_place_negative(self):
        place = 123
        uid = meetings[1]

        result = meeting_add_place(uid, place)

        self.assertEqual(result, -1)
        self.assertEqual(Meeting.get_by_id(uid).place, None)

    def test_meeting_add_place_negative2(self):
        place = 'дом'
        uid = 'kek'

        result = meeting_add_place(uid, place)

        self.assertEqual(result, -1)

    def test_meeting_add_place_negative3(self):
        place = 'дом'
        uid = '16fd2706-8baf-433b-82eb-8c7fada847da'

        result = meeting_add_place(uid, place)

        self.assertEqual(result, -1)

    def test_get_meeting_info_positive(self):
        uid = add_meeting(test_name, test_administrator)
        meeting_add_place(uid, test_place)
        meeting_add_start_time(uid, test_start_time)
        meeting_add_duration(uid, test_duration)

        result = get_meeting_info(uid)

        self.assertFalse(not result)
        self.assertEqual(result['name'], test_name)
        self.assertEqual(result['administrator'], test_administrator)
        self.assertEqual(result['start_time'], test_start_time)
        self.assertEqual(result['duration'], test_duration)
        self.assertEqual(result['place'], test_place)
        self.assertEqual(result['questions'], [])
        self.assertEqual(result['participants'], [])

    def test_get_meeting_info_negative(self):
        uid = '16fd2706-8baf-433b-82eb-8c7fada847da'

        result = get_meeting_info(uid)

        self.assertEqual(result, {})

    def test_get_meeting_info_negative2(self):
        uid = 'kek'

        result = get_meeting_info(uid)

        self.assertEqual(result, {})


class TestParticipantsModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initialization('test_lets.db')
        meeting1 = add_meeting('Тестовое мероприятие 1', '@111')
        meeting2 = add_meeting('Тестовое мероприятие 2', '@222')
        meetings.append(meeting1)
        meetings.append(meeting2)

    @classmethod
    def tearDownClass(cls):
        db.close()
        os.remove('test_lets.db')
        meetings.clear()

    def test_add_participant_positive(self):
        uid = meetings[0]
        test_participant = '@11111'
        before_count = len(Participant.select())

        result = add_participant(uid, test_participant)

        self.assertEqual(result, 0)
        self.assertEqual(len(Participant.select()), before_count + 1)

    def test_add_participant_negative(self):
        uid = 'kek'
        test_participant = '@11111'
        before_count = len(Participant.select())

        result = add_participant(uid, test_participant)

        self.assertEqual(result, -1)
        self.assertEqual(len(Participant.select()), before_count)

    def test_add_participant_negative2(self):
        uid = meetings[1]
        test_participant = 111
        before_count = len(Participant.select())

        result = add_participant(uid, test_participant)

        self.assertEqual(result, -1)
        self.assertEqual(len(Participant.select()), before_count)

    def test_get_meetings_by_user_id_positive(self):
        test_name1, test_name2 = "Проверяем участников 1", "Проверяем участников 2"
        uid1 = add_meeting(test_name1, '@777')
        uid2 = add_meeting(test_name2, '@777')
        user = '@333'
        add_participant(uid1, user)
        add_participant(uid2, user)

        result = get_meetings_by_user_id(user)

        self.assertFalse(not result)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], (test_name1, uid1))
        self.assertEqual(result[1], (test_name2, uid2))

    def test_get_meetings_by_user_id_positive2(self):
        user = '@1000'

        result = get_meetings_by_user_id(user)

        self.assertEqual(result, [])

    def test_get_meetings_by_user_id_negative(self):
        user = 111

        result = get_meetings_by_user_id(user)

        self.assertEqual(result, [])

    def test_get_participants_positive(self):
        uid = add_meeting("Проверяем всех участников", '@777')
        users = ['@111', '@222', '@333']
        for user in users:
            add_participant(uid, user)

        result = get_participants(uid)

        self.assertEqual(len(result), len(users))
        self.assertEqual(result, users)

    def test_get_participants_positive2(self):
        uid = meetings[1]

        result = get_participants(uid)

        self.assertEqual(result, [])

    def test_get_participants_negative(self):
        uid = 'kek'

        result = get_participants(uid)

        self.assertEqual(result, [])


class TestQuestionModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initialization('test_lets.db')
        meeting1 = add_meeting('Тестовое мероприятие 1', '@111')
        meeting2 = add_meeting('Тестовое мероприятие 2', '@222')
        meetings.append(meeting1)
        meetings.append(meeting2)

    @classmethod
    def tearDownClass(cls):
        db.close()
        os.remove('test_lets.db')
        meetings.clear()

    def test_add_question_positive(self):
        uid = meetings[0]
        test_question = 'Как дела?'
        test_options = 'Отлично, Хорошо, Нормально, Не очень'
        before_count = len(Question.select())

        result = add_question(uid, test_question, test_options)

        self.assertNotEqual(result, -1)
        self.assertEqual(len(Question.select()), before_count + 1)
        self.assertEqual(Question.get_by_id(result).question, test_question)
        self.assertEqual(Question.get_by_id(result).option_list, test_options)

    def test_add_question_negative(self):
        uid = meetings[1]
        test_question = 123
        test_options = 'Отлично, Хорошо, Нормально, Не очень'
        before_count = len(Question.select())

        result = add_question(uid, test_question, test_options)

        self.assertEqual(result, -1)
        self.assertEqual(len(Question.select()), before_count)

    def test_add_question_negative2(self):
        uid = meetings[1]
        test_question = 'Как дела?'
        test_options = 123
        before_count = len(Question.select())

        result = add_question(uid, test_question, test_options)

        self.assertEqual(result, -1)
        self.assertEqual(len(Question.select()), before_count)

    def test_add_question_negative3(self):
        uid = '12345-123-123-133'
        test_question = 'Как дела?'
        test_options = 'Отлично, Хорошо, Нормально, Не очень'
        before_count = len(Question.select())

        result = add_question(uid, test_question, test_options)

        self.assertEqual(result, -1)
        self.assertEqual(len(Question.select()), before_count)

    def test_get_meeting_questions_positive(self):
        uid = add_meeting("Тестовое название", test_administrator)
        test_qs = ['Как дела?', 'Как настроение?', 'Как погода?']
        test_os = ['Хорошо, Не очень', 'Хорошее, Плохое', 'Солнечно, Пасмурно']
        ids = []
        for i in range(len(test_qs)):
            ids.append(add_question(uid, test_qs[i], test_os[i]))

        result = get_meeting_questions(uid)

        self.assertEqual(result, ids)

    def test_get_meeting_questions_positive2(self):
        uid = meetings[1]

        result = get_meeting_questions(uid)

        self.assertEqual(result, [])

    def test_get_meeting_questions_negative(self):
        uid = 'kek'

        result = get_meeting_questions(uid)

        self.assertEqual(result, [])

    def test_get_options_list_positive(self):
        uid = meetings[0]
        test_question = 'Как дела?'
        test_options = 'Отлично, Хорошо, Нормально, Не очень'
        qid = add_question(uid, test_question, test_options)
        expected = ['Отлично', 'Хорошо', 'Нормально', 'Не очень']

        result = get_options_list(qid)

        self.assertEqual(result, expected)

    def test_get_options_list_negative(self):
        qid = 12345

        result = get_options_list(qid)

        self.assertEqual(result, [])

    def test_get_options_list_negative2(self):
        qid = 'Hi'

        result = get_options_list(qid)

        self.assertEqual(result, [])

    def test_select_option_positive(self):
        uid = meetings[0]
        test_question = 'Как там на улице?'
        test_options = 'Солнечно, Пасмурно, Ветрено, Тепло'
        qid = add_question(uid, test_question, test_options)
        selected_option = 'Ветрено'

        result = select_option(qid, selected_option)

        self.assertEqual(result, 0)
        self.assertEqual(Question.get_by_id(qid).selected_answer, selected_option)

    def test_select_option_negative(self):
        uid = meetings[0]
        test_question = 'Как там на улице?'
        test_options = 'Солнечно, Пасмурно, Ветрено, Тепло'
        qid = add_question(uid, test_question, test_options)
        selected_option = 'Нормально'

        result = select_option(qid, selected_option)

        self.assertEqual(result, -1)
        self.assertEqual(Question.get_by_id(qid).selected_answer, None)

    def test_select_option_negative2(self):
        qid = 123456
        selected_option = 'Нормально'

        result = select_option(qid, selected_option)

        self.assertEqual(result, -1)

    def test_select_option_negative3(self):
        uid = meetings[0]
        test_question = 'Как там на улице?'
        test_options = 'Солнечно, Пасмурно, Ветрено, Тепло'
        qid = add_question(uid, test_question, test_options)
        selected_option = 123

        result = select_option(qid, selected_option)

        self.assertEqual(result, -1)
        self.assertEqual(Question.get_by_id(qid).selected_answer, None)

    def test_select_option_negative4(self):
        uid = meetings[0]
        test_question = 'Как там на улице?'
        test_options = 'Солнечно, Пасмурно, Ветрено, Тепло'
        qid = add_question(uid, test_question, test_options)
        selected_option = 'Солнечно'

        result = select_option('Hi', selected_option)

        self.assertEqual(result, -1)
        self.assertEqual(Question.get_by_id(qid).selected_answer, None)


class TestAnswerModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        initialization('test_lets.db')
        meeting1 = add_meeting('Тестовое мероприятие 1', '@111')
        meeting2 = add_meeting('Тестовое мероприятие 2', '@222')
        meetings.append(meeting1)
        meetings.append(meeting2)
        test_question = 'Как дела?'
        test_options = 'Отлично, Хорошо, Нормально, Не очень'
        test_qid.append(add_question(meeting1, test_question, test_options))

    @classmethod
    def tearDownClass(cls):
        db.close()
        os.remove('test_lets.db')
        meetings.clear()
        test_qid.clear()

    def test_add_answer_positive(self):
        qid = test_qid[0]
        selected = 'Хорошо'
        user = '@111'
        before_count = len(Answer.select())

        result = add_answer(qid, user, selected)

        self.assertEqual(result, 0)
        self.assertEqual(len(Answer.select()), before_count + 1)

    def test_add_answer_negative(self):
        qid = test_qid[0]
        selected = 'Пойдет'
        user = '@111'
        before_count = len(Answer.select())

        result = add_answer(qid, user, selected)

        self.assertEqual(result, -1)
        self.assertEqual(len(Answer.select()), before_count)

    def test_add_answer_negative2(self):
        qid = 123
        selected = 'Хорошо'
        user = '@111'
        before_count = len(Answer.select())

        result = add_answer(qid, user, selected)

        self.assertEqual(result, -1)
        self.assertEqual(len(Answer.select()), before_count)

    def test_add_answer_negative3(self):
        qid = 'hi'
        selected = 'Хорошо'
        user = '@111'
        before_count = len(Answer.select())

        result = add_answer(qid, user, selected)

        self.assertEqual(result, -1)
        self.assertEqual(len(Answer.select()), before_count)

    def test_add_answer_negative4(self):
        qid = test_qid[0]
        selected = 'Хорошо'
        user = 111
        before_count = len(Answer.select())

        result = add_answer(qid, user, selected)

        self.assertEqual(result, -1)
        self.assertEqual(len(Answer.select()), before_count)

    def test_add_answer_negative5(self):
        qid = test_qid[0]
        selected = 123
        user = '@111'
        before_count = len(Answer.select())

        result = add_answer(qid, user, selected)

        self.assertEqual(result, -1)
        self.assertEqual(len(Answer.select()), before_count)

    def test_get_answers_positive(self):
        test_question = 'Как там на улице?'
        test_options = 'Солнечно, Пасмурно, Ветрено, Тепло'
        qid = add_question(meetings[0], test_question, test_options)
        user = '@222'
        answers = ['Солнечно', 'Ветрено', 'Тепло']
        counts = [3, 6, 1]
        for i in range(len(answers)):
            for j in range(counts[i]):
                add_answer(qid, user, answers[i])

        result = get_answers(qid)

        self.assertEqual(len(result), len(answers))

        for i in range(len(answers)):
            self.assertIn((answers[i], counts[i]), result)

    def test_get_answers_positive2(self):
        test_question = 'Что делаешь?'
        test_options = 'Сплю, Ем, Делаю лабы, Отдыхаю'
        qid = add_question(meetings[0], test_question, test_options)

        result = get_answers(qid)

        self.assertEqual(result, [])

    def test_get_answers_negative(self):
        qid = 111

        result = get_answers(qid)

        self.assertEqual(result, [])

    def test_get_answers_negative2(self):
        qid = 'hi'

        result = get_answers(qid)

        self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
