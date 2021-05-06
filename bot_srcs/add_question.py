from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from database.Requests import *

def start_conv(update, context):
	# for test
	# mid = add_meeting("koko", update.message.chat.id)
	# update.message.reply_text(str(mid))
	update.message.reply_text('Все просто пишешь вопрос, а потом список ответов. Но сначала введи идентификатор мероприятия.\n(помни, что если ты хочешь выйти из режима добавления опроса, вызови /cancel)')
	return 1

def finish_conv(update, context):
	update.message.reply_text('Ну как хочешь)')
	return ConversationHandler.END

meeting_id = -1

def get_meet_id(update, context):
	global meeting_id
	meeting_id = update.message.text
	if (meeting_id == '/cancel'):
		return finish_conv(update, context)

	user_id =  update.message.chat.username
	if (add_participant(meeting_id, user_id) == -1):
		update.message.reply_text('Похоже, у тебя неверный идентификатор встречи.')
		return 1

	update.message.reply_text('Супер. А теперь пиши вопрос типа "Что будет кушать?"')
	return 2

question = ""

def get_question(update, context):
	global question
	question = update.message.text
	if (question == '/cancel'):
		return finish_conv(update, context)

	update.message.reply_text('Накидай вариантов через запятую и пробел (пицца, роллы, паста)?')
	return 3

def get_options(update, context):
	options = update.message.text
	if (options == '/cancel'):
		return finish_conv(update, context)

	if (add_question(meeting_id, question, options) == -1):
		update.message.reply_text('Что-то не так. Давай поновой похоже.')
		return ConversationHandler.END

	update.message.reply_text('Ну вот и ладненько. Пойду спрошу у участников, что они об этом думают!')
	return ConversationHandler.END


add_question_handler = ConversationHandler(
	entry_points=[CommandHandler('add_question', start_conv)],
	states={
	1: [MessageHandler(Filters.text, get_meet_id)],
	2: [MessageHandler(Filters.text, get_question)],
	3: [MessageHandler(Filters.text, get_options)]
	},
	fallbacks=[finish_conv]
)
