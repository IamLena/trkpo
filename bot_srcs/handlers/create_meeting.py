from telegram.ext import MessageHandler, Filters, CommandHandler, \
	ConversationHandler
from database.Requests import add_meeting, add_participant, \
	meeting_add_start_time, meeting_add_duration, meeting_add_place
from context import context_busy

meeting_id = -1


def start_conv(update, context):
	global context_busy
	context_busy[0] = True
	update.message.reply_text(
		'Создадим мероприятие! '
		'Чтобы организовать встречу тебе нужно ответить на 3 вопроса'
		' о времени и месте. Начнем с названия. '
		'Придумай что-нибудь лаконичное и яркое! '
		'Чтобы выйти из режима планирования отправь "/cancel"'
	)
	return 1


def finish_conv(update, context):
	global context_busy
	context_busy[0] = False
	# удалить заготовку или предложить пользователю позже ее дополнить
	update.message.reply_text('Ну ладненько. Тогда в другой раз.')
	return ConversationHandler.END


def set_name(update, context):
	global context_busy
	name = update.message.text
	if name[0] == '/':
		if name == '/cancel':
			return finish_conv(update, context)
		update.message.reply_text(
			'Для вызова другой команды, тебе нужно завершить выполнение этой. '
			'Если тебе не хочется отвечать на вопросы вызови /cancel.'
		)
		return 1

	user_id = update.message.chat.username
	global meeting_id
	meeting_id = add_meeting(name, user_id)

	if meeting_id == -1:
		context_busy[0] = False
		update.message.reply_text(
			'Произошла ошибка. Попробуй заново... '
			'Имей в виду, что имя встречи должно соддержать '
			'не более 45 символов'
		)
		return ConversationHandler.END

	if add_participant(meeting_id, user_id) == -1:
		context_busy[0] = False
		update.message.reply_text('Что-то пошло не так...')
		return ConversationHandler.END

	update.message.reply_text(
		'Отлично.	\nКогда встречаемся? '
		'Стоит придерживаться следующего формата - 1 января 2021 в 15:00, '
		'но, конечно, ты можешь ввести любую чепуху. '
		'Если ты не знаешь, пиши /pass.'
	)
	return 2


def set_start_time(update, context):
	global context_busy
	start_time = update.message.text

	if start_time[0] == '/':
		if start_time == '/cancel':
			return finish_conv(update, context)
		if start_time != '/pass':
			update.message.reply_text(
				'Для вызова другой команды, '
				'тебе нужно завершить выполнение этой. '
				'Если тебе не хочется отвечать на вопросы вызови /cancel.'
			)
			return 2

	if start_time != '/pass':
		if meeting_add_start_time(meeting_id, start_time) == -1:
			# обработка ошибки
			context_busy[0] = False
			update.message.reply_text('Что-то пошло не так...')
			return ConversationHandler.END

	update.message.reply_text(
		'Супер! Как долго планируется тусить? /pass чтобы пропустить.')
	return 3


def set_duration(update, context):
	duration = update.message.text
	if duration[0] == '/':
		if duration == '/cancel':
			return finish_conv(update, context)
		if duration != '/pass':
			update.message.reply_text(
				'Для вызова другой команды, '
				'тебе нужно завершить выполнение этой. '
				'Если тебе не хочется отвечать на вопросы вызови /cancel.'
			)
			return 3

	if duration != '/pass':
		if meeting_add_duration(meeting_id, duration) == -1:
			# обработка ошибки
			global context_busy
			context_busy[0] = False
			update.message.reply_text('Что-то пошло не так...')
			return ConversationHandler.END

	update.message.reply_text(
		'Лады. А теперь укажи место. '
		'Ну и конечно ты можешь пропустить и '
		'этот последний вопрос - /pass.'
	)
	return 4


def set_place(update, context):
	global context_busy
	place = update.message.text

	if place[0] == '/':
		if place == '/cancel':
			return finish_conv(update, context)
		if place != '/pass':
			update.message.reply_text(
				'Для вызова другой команды, '
				'тебе нужно завершить выполнение этой.'
				' Если тебе не хочется отвечать на вопросы вызови /cancel.'
			)
			return 4

	if place != '/pass':
		if meeting_add_place(meeting_id, place) == -1:
			# обработка ошибки
			update.message.reply_text('Что-то не так с базой данных')
			context_busy[0] = False
			return ConversationHandler.END

	update.message.reply_text(
		'Мероприятие создано! /get_meeting_info выведит всю информацию о нем.'
	)
	update.message.reply_text(
		'Все пропущенные вопросы можно решить с помощью добавления опроса.'
	)
	update.message.reply_text(
		'Вот идентификатор:\n' + str(meeting_id))
	update.message.reply_text(
		'Отправь его друзьям, чтобы они поучаствовали в опросах и '
		'смогли получить полную информацию о встрече.\n'
		'Если ты хочешь дополнить организацию еще вопросами, '
		'воспользуйся командой /add_question.'
	)

	context_busy[0] = False
	return ConversationHandler.END


create_meeting_handler = ConversationHandler(
	entry_points=[CommandHandler('create_meeting', start_conv)],
	states={
		1: [MessageHandler(Filters.text, set_name)],
		2: [MessageHandler(Filters.text, set_start_time)],
		3: [MessageHandler(Filters.text, set_duration)],
		4: [MessageHandler(Filters.text, set_place)]
	},
	fallbacks=[finish_conv]
)
