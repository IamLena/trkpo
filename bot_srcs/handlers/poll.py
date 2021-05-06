from telegram import (
	Poll,
	ParseMode,
	KeyboardButton,
	KeyboardButtonPollType,
	ReplyKeyboardMarkup,
	ReplyKeyboardRemove,
	Update,
)
from telegram.ext import (
	Updater,
	CommandHandler,
	PollAnswerHandler,
	PollHandler,
	MessageHandler,
	Filters,
	CallbackContext,
	ConversationHandler
)
from  context import context_busy
from database.Requests import *

def my_send_poll(update, context, q_id, question, options):
	message = context.bot.send_poll(
		update.effective_chat.id,
		question,
		options,
		is_anonymous=False,
		allows_multiple_answers=True,
	)
	# Save some info about the poll the bot_data for later use in receive_poll_answer
	payload = {
		message.poll.id: {
			"options": options,
			"message_id": message.message_id,
			"chat_id": update.effective_chat.id,
			"answers": 0,
			"q_id": q_id
		}
	}
	context.bot_data.update(payload)

def start_conv(update, context):
	global context_busy
	if context_busy[0]:
		update.message.reply_text('Сначала завершите выполнение предыдущей команды. Если тебе не хочется отвечать на вопросы вызови /cancel.')
		return ConversationHandler.END
	context_busy[0] = True
	update.message.reply_text('Введите id мероприятия и ответься на предлагаемые опросы!')
	return 1

def finish_conv(update, context):
	global context_busy
	context_busy[0] = False
	update.message.reply_text('ну пусть так')
	return ConversationHandler.END


def get_id_and_poll(update, context):
	global context_busy
	meeting_id = update.message.text
	if (meeting_id == '/cancel'):
		return finish_conv(update, context)

	if (get_meeting_info(meeting_id) == {}):
		update.message.reply_text('Похоже, у тебя неверный идентификатор встречи.')
		update.message.reply_text('Если ты хочешь выйти из режима answer_questions вызови /cancel')
		return 1

	q_id_list = get_meeting_questions(meeting_id)
	if (len(q_id_list) == 0):
		update.message.reply_text('Для вас вопросов нет')
		context_busy[0] = False
		return ConversationHandler.END

	for q_id in q_id_list:
		question = get_question_by_id(q_id)
		options = get_options_list(q_id)
		my_send_poll(update, context, q_id, question, options)

	context_busy[0] = False
	return ConversationHandler.END

def receive_poll_answer(update, context):
	answer = update.poll_answer
	poll_id = answer.poll_id
	try:
		options = context.bot_data[poll_id]["options"]
	# this means this poll answer update is from an old poll, we can't do our answering then
	except KeyError:
		return
	q_id = context.bot_data[poll_id]["q_id"]
	selected_options = answer.option_ids

	for op_id in selected_options:
		res = add_answer(q_id, update.poll_answer.user.username, options[op_id])
		# можно тут ошибки чекнуть

# # Close poll after three participants voted
# if context.bot_data[poll_id]["answers"] == 3:
# 	context.bot.stop_poll(
# 		context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
# 	)

def update_answer(question_id):
	answers = get_answers(question_id)
	if answers:
		selected = answers[0][0]
		max_quantity = answers[0][1]
		for answer in answers:
			if answer[1] > max_quantity:
				max_quantity = answer[1]
				selected = answer[0]
		result = select_option(question_id, selected)
		return result
	return -1

poll_handler = ConversationHandler(
	entry_points=[CommandHandler('answer_questions', start_conv)],
	states={
	1: [MessageHandler(Filters.text, get_id_and_poll)]
	},
	fallbacks=[finish_conv]
)

poll_answer_handler = PollAnswerHandler(receive_poll_answer)
