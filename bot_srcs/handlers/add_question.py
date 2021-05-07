from telegram.ext import MessageHandler, Filters, CommandHandler, \
	ConversationHandler
from database.Requests import get_meeting_info, add_question, is_administrator
from context import context_busy


def start_conv(update, context):
	global context_busy
	if context_busy[0]:
		update.message.reply_text(
			'Сначала заверши выполнение предыдущей команды. '
			'Если тебе не хочется отвечать на вопросы вызови /cancel.'
		)
		return ConversationHandler.END
	context_busy[0] = True
	update.message.reply_text(
		'Всё просто: пишешь вопрос, а потом список ответов. '
		'Но сначала введи идентификатор мероприятия.\n'
		'(помни, что если ты хочешь выйти из режима добавления опроса, '
		'вызови /cancel)'
	)
	return 1


def finish_conv(update, context):
	global context_busy
	context_busy[0] = False
	update.message.reply_text('Ну как хочешь)')
	return ConversationHandler.END


meeting_id = -1
question = ""


def get_meet_id(update, context):
	global meeting_id
	meeting_id = update.message.text
	if meeting_id[0] == '/':
		if meeting_id == '/cancel':
			return finish_conv(update, context)
		update.message.reply_text(
			'Для вызова другой команды, тебе нужно завершить выполнение этой. '
			'Если тебе не хочется отвечать на вопросы вызови /cancel.'
		)
		return 1

	m = get_meeting_info(meeting_id)
	if m == {}:
		update.message.reply_text(
			'Похоже, у тебя неверный идентификатор встречи.'
		)
		update.message.reply_text(
			'Если ты хочешь выйти из режима add_question, вызови /cancel'
		)
		return 1

	if not is_administrator(meeting_id, update.message.chat.id):
		update.message.reply_text(
			'Ты не являешься организатором этой встречи. '
			'А добавлять вопрос может только он.'
		)
		global context_busy
		context_busy[0] = False
		return ConversationHandler.END

	update.message.reply_text(
		'Супер. А теперь пиши вопрос, типа "Что будем кушать?"'
	)
	return 2


def get_question(update, context):
	global question
	question = update.message.text
	if question[0] == '/':
		if question == '/cancel':
			return finish_conv(update, context)
		update.message.reply_text(
			'Для вызова другой команды, тебе нужно завершить выполнение этой. '
			'Если тебе не хочется отвечать на вопросы вызови /cancel.'
		)
		return 2

	update.message.reply_text(
		'Накидай вариантов через запятую и пробел (пицца, роллы, паста)?'
	)
	return 3


def get_options(update, context):
	options = update.message.text
	if options[0] == '/':
		if options == '/cancel':
			return finish_conv(update, context)
		update.message.reply_text(
			'Для вызова другой команды, тебе нужно завершить выполнение этой. '
			'Если тебе не хочется отвечать на вопросы вызови /cancel.'
		)
		return 3

	global context_busy
	context_busy[0] = False
	if add_question(meeting_id, question, options) == -1:
		update.message.reply_text('Что-то не так. Давай поновой, похоже.')
		return ConversationHandler.END

	update.message.reply_text(
		'Ну вот и ладненько. Спрошу у участников, что они об этом думают! '
		'Пройти опросы можно с помощью команды /answer_questions.'
	)
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
