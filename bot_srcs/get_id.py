from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from database.Requests import *

def get_id_function(update, context):
	user_id = update.message.chat.id
	list = get_meetings_by_user_id(user_id)
	length = len(list)
	if (length == 0):
		msg = 'Ты пока не являешься участником какого-либо мероприятия. \
		Присоединись к встрече с помощью /join или создай свою тусовку - /create_meeting.'
	else:
		msg = 'Список твоих мероприятий:'
		for meet in list:
			msg += '\n' + meet[0] + ': ' + str(meet[1])
	update.message.reply_text(msg)
	return 1

get_id_handler = CommandHandler('get_id', get_id_function)
