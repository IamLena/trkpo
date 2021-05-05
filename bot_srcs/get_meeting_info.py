from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import User
from database.Requests import *

def start_conv(update, context):
	# for test
	mid = add_meeting("koko", update.message.chat.id)
	update.message.reply_text(str(mid))
	update.message.reply_text('Чтобы посмотреть сведения о мероприятии, введи идентификатор встречи. Если ты его не знаешь, выйди из режима просмотра информации с помощью /cancel и вызови /get_id. Получишь список идентификаторов встреч, участником которых ты являешься.')

	return 1

def finish_conv(update, context):
	update.message.reply_text('окей')
	return ConversationHandler.END

def form_output(meeting):
	msg = '"' + meeting['name'] + '"\n'
	if (meeting['start_time']):
		msg += "Время: " + meeting['start_time'] + '\n'
	if (meeting['duration']):
		msg += "Продолжительность: " + meeting['duration'] + '\n'
	if (meeting['place']):
		msg += "Место: " + meeting['place'] + '\n'
	if (meeting['questions']):
		for q in meeting['questions']:
			msg += q[0] + ': ' + q[1] + '\n'
	if (meeting['participants']):
		msg += 'Участники:\n'
		for p in meeting['participants']:
			msg += '@' + p + '\n'
	msg += "По всем вопросам обращаться к @" + str(meeting['administrator_id'])
	return msg

def get_id(update, context):
	meeting_id = update.message.text
	if (meeting_id == '/cancel'):
		return finish_conv(update, context)

	m = get_meeting_info(meeting_id)

	if (m == {}):
		update.message.reply_text('Похоже, у тебя неверный идентификатор встречи.')
		return 1

	update.message.reply_text(form_output(m))
	return ConversationHandler.END

get_meeting_info_handler = ConversationHandler(
	entry_points=[CommandHandler('get_meeting_info', start_conv)],
	states={
	1: [MessageHandler(Filters.text, get_id)]
	},
	fallbacks=[finish_conv]
)
