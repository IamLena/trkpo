from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from telegram import User
from database.Requests import *

def start_conv(update, context):
	update.message.reply_text('Чтобы посмотреть сведения о мероприятии, введи идентификатор встречи. Если ты его не знаешь, выйди из режима просмотра информации с помощью /cancel и вызови /get_id. Получишь список идентификаторов встреч, участником которых ты являешься.')

	return 1

def finish_conv(update, context):
	update.message.reply_text('окей')
	return ConversationHandler.END


def get_id(update, context):
	meeting_id = update.message.text
	if (meeting_id == '/cancel'):
		return finish_conv(update, context)

	m = get_meeting_info(meeting_id)

	if (m == {}):
		update.message.reply_text('Похоже, у тебя неверный идентификатор встречи.')
		return ConversationHandler.END

	msg = '"' + m['name'] + '" состоится ' + m['start_time'] + ' и продлится по плану ' + m['duration'] + '. Местро проведения - ' + m['place'] + '.'
	update.message.reply_text(msg)
	return ConversationHandler.END

# 'id': meeting.uid,
# 'name': meeting.name,
# 'administrator_id': meeting.administrator_id,
# 'start_time': meeting.start_time,
# 'duration': meeting.duration,
# 'place': meeting.place,
# 'questions': parse_questions_answers(meeting),
# 'participants': parse_participants(meeting)}

get_meeting_info_handler = ConversationHandler(
	entry_points=[CommandHandler('get_meeting_info', start_conv)],
	states={
	1: [MessageHandler(Filters.text, get_id)]
	},
	fallbacks=[finish_conv]
)
