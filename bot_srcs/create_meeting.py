from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, ConversationHandler
from database.Requests import *

def start_conv(update, context):
	update.message.reply_text('Создадим мероприятие! \
	Чтобы организовать встречу тебе нужно ответить на 3 вопроса \
	о времени и месте. Начнем с названия. Придумай что-нибудь лаконичное и яркое! Чтобы выйти из режима планирования отправь "/cancel"')
	return 1

def finish_conv(update, context):
	# удалить заготовку или предложить пользователю позже ее дополнить
	update.message.reply_text('Ну ладненько. Тогда в другой раз.')
	return ConversationHandler.END

def set_name(update, context):
	name = update.message.text
	if (name == '/cancel'):
		return finish_conv(update, context)

	user_id =  update.message.chat.id # user_id =  update.message.from.id syntax error
	global meeting_id
	meeting_id = add_meeting(name, user_id)

	if (meeting_id == -1):
		update.message.reply_text('Произошла ошибка. Попробуй заново... Имей в виду, что имя встречи должно соддержать не более 45 символов')
		return ConversationHandler.END

	if (add_participant(meeting_id, user_id) == -1):
		update.message.reply_text('Что-то пошло не так...')
		return ConversationHandler.END

	update.message.reply_text('Отлично.\nКогда встречаемся? Стоит придерживаться следующего формата - 1 января 2021 в 15:00, но конечно ты можешь ввести любую чепуху.')
	return 2

def set_start_time(update, context):
	start_time = update.message.text

	if (start_time == '/cancel'):
		return finish_conv(update, context)

	if (meeting_add_start_time(meeting_id, start_time) == -1):
		# обработка ошибки
		update.message.reply_text('Что-то пошло не так...')
		return ConversationHandler.END

	update.message.reply_text('Супер! Как долго планируется тусить?')
	return 3

def set_duration(update, context):
	duration = update.message.text

	if (duration == '/cancel'):
		return finish_conv(update, context)

	if (meeting_add_duration(meeting_id, duration) == -1):
		# обработка ошибки
		update.message.reply_text('Что-то пошло не так...')
		return ConversationHandler.END

	update.message.reply_text('Лады. А теперь укажи место.')
	return 4

def set_place(update, context):
	place = update.message.text

	if (place == '/cancel'):
		return finish_conv(update, context)

	if (meeting_add_place(meeting_id, place) == -1):
		# обработка ошибки
		update.message.reply_text('Что-то не так с базой данных')

	else:
		update.message.reply_text('Мероприятие создано!')
		m = get_meeting_info(meeting_id)
		msg = '"' + m['name'] + '" состоится ' + m['start_time'] + ' и продлится по плану ' + m['duration'] + '. Местро проведения - ' + m['place'] + '.'
		update.message.reply_text(msg)
		update.message.reply_text('Вот идентификатор:\n' + str(meeting_id))
		update.message.reply_text('Отправь его друзьям, чтобы они поучаствовали в опросах и смогли получить полную информацию о встрече.\nЕсли ты хочешь дополнить организацию еще вопросами, воспользуйся командой /add_question.')

	return ConversationHandler.END

create_meeting_conv_handler = ConversationHandler(
	entry_points=[CommandHandler('create_meeting', start_conv)],
	states={
	1: [MessageHandler(Filters.text, set_name)],
	2: [MessageHandler(Filters.text, set_start_time)],
	3: [MessageHandler(Filters.text, set_duration)],
	4: [MessageHandler(Filters.text, set_place)]
	},
	fallbacks=[finish_conv]
)
