from telegram.ext import MessageHandler, Filters, CommandHandler, ConversationHandler
from database.Requests import add_participant
from  context import context_busy

def start_conv(update, context):
	global context_busy
	if context_busy[0]:
		update.message.reply_text('Сначала завершите выполнение предыдущей команды. Если тебе не хочется отвечать на вопросы вызови /cancel.')
		return ConversationHandler.END
	context_busy[0] = True
	update.message.reply_text('Чтобы стать участником мероприятия, тебе необходим идентификатор. Попроси его у организатора и отправь мне, я сделаю всю остальную работу :)\nЕсли не хочешь никуда добавляться вызови /cancel')
	return 1

def finish_conv(update, context):
	global context_busy
	context_busy[0] = False
	update.message.reply_text('Не вопрос.')
	return ConversationHandler.END


def get_id(update, context):
	meeting_id = update.message.text
	if (meeting_id == '/cancel'):
		return finish_conv(update, context)

	user_id =  update.message.chat.username
	if (add_participant(meeting_id, user_id) == -1):
		update.message.reply_text('Похоже, у тебя неверный идентификатор встречи.')
		update.message.reply_text('Если ты хочешь выйти из режима join вызови /cancel')
		return 1

	global context_busy
	context_busy[0] = False

	if (add_participant(meeting_id, user_id) == -2):
		update.message.reply_text('Ты уже являешься участником этого мероприятия!')
		return ConversationHandler.END

	update.message.reply_text('Тебя добавили в участники! Теперь ты сможешь поучаствовать в принятии решений и точно не пропустишь всю важную информацию. Чтобы получить сведения о встрече воспользуйся командой /get_meeting_info.')
	return ConversationHandler.END

join_handler = ConversationHandler(
	entry_points=[CommandHandler('join', start_conv)],
	states={
	1: [MessageHandler(Filters.text, get_id)]
	},
	fallbacks=[finish_conv]
)
