from telegram.ext import MessageHandler, Filters


def letsbot_responses(input_text):
	user_message = str(input_text).lower()
	if user_message in ("привет", "здравствуй", "хай"):
		return "И тебе привет :)"
	if user_message in ("пока", "до свидания"):
		return "Хм... ну я всегда тут. Возвращайся!"
	return \
		"Я не понимаю тебя... " \
		"Может быть /help поможет нам понять друг друга."


def handle_message(update, context):
	response = letsbot_responses(update.message.text)
	update.message.reply_text(response)


msg_handler = MessageHandler(Filters.text, handle_message)
