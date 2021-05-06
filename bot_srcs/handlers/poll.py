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
)

from database.Requests import *

def my_send_poll(update, context, question, options):
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
			"questions": options,
			"message_id": message.message_id,
			"chat_id": update.effective_chat.id,
			"answers": 0,
		}
	}
	context.bot_data.update(payload)

def poll(update, context):
	print("hello")
	meeting_id = add_meeting("test", update.message.chat.username)
	add_question(meeting_id, "hey?", "1, 2, 3, 4")
	add_question(meeting_id, "kuku?", "5, 6, 7, 8")
	q_id_list = get_meeting_questions(meeting_id)
	if (len(q_id_list) == 0):
		update.message.reply_text('Для вас вопросов нет')
		return
	for q_id in q_id_list:
		# question = get_name(q_id)
		question = q_id
		options = get_options_list(q_id)
		print(question, options)
		my_send_poll(update, context, question, options)

def receive_poll_answer(update: Update, context: CallbackContext) -> None:
	"""Summarize a users poll vote"""
	answer = update.poll_answer
	poll_id = answer.poll_id
	try:
		questions = context.bot_data[poll_id]["questions"]
	# this means this poll answer update is from an old poll, we can't do our answering then
	except KeyError:
		return
	selected_options = answer.option_ids
	answer_string = ""
	for question_id in selected_options:
		if question_id != selected_options[-1]:
			answer_string += questions[question_id] + " and "
		else:
			answer_string += questions[question_id]
	context.bot.send_message(
		context.bot_data[poll_id]["chat_id"],
		f"{update.effective_user.mention_html()} feels {answer_string}!",
		parse_mode=ParseMode.HTML,
	)
	context.bot_data[poll_id]["answers"] += 1
	# Close poll after three participants voted
	if context.bot_data[poll_id]["answers"] == 3:
		context.bot.stop_poll(
			context.bot_data[poll_id]["chat_id"], context.bot_data[poll_id]["message_id"]
		)

poll_handler = CommandHandler('answer_questions', poll)
poll_answer_handler = PollAnswerHandler(receive_poll_answer)
