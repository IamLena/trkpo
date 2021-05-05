from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from database.Requests import *

def start_conv(update, context):
	# for test
	# mid = add_meeting("koko", update.message.chat.id)
	# update.message.reply_text(str(mid))
	update.message.reply_text('Чтобы стать участником мероприятия, тебе необходим идентификатор. Попроси его у организатора и отправь мне, я сделаю всю остальную работу :)\nЕсли не хочешь никуда добавляться вызови /cancel')
	return 1

def finish_conv(update, context):
	update.message.reply_text('Не вопрос.')
	return ConversationHandler.END


def get_id(update, context):
	meeting_id = update.message.text
	if (meeting_id == '/cancel'):
		return finish_conv(update, context)

	user_id =  update.message.chat.id
	if (add_participant(meeting_id, user_id) == -1):
		update.message.reply_text('Похоже, у тебя неверный идентификатор встречи.')
		return 1

	update.message.reply_text('Тебя добавили в участники! Теперь ты сможешь поучаствовать в принятии решений и точно не пропустишь всю важную информацию. Чтобы получить сведения о встрече воспользуйся командой /get_meeting_info.')
	return ConversationHandler.END

joinhandler = ConversationHandler(
	entry_points=[CommandHandler('join', start_conv)],
	states={
	1: [MessageHandler(Filters.text, get_id)]
	},
	fallbacks=[finish_conv]
)
