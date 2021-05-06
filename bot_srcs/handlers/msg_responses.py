from telegram.ext import MessageHandler, Filters

def letsbot_responses(input_text):
	user_message = str(input_text).lower()
	if user_message in ("привет", "здравствуй", "хай"):
		return "Привет! Рад тебя видеть :)"
	if user_message in ("пока", "до свидания"):
		return "Возвращайся поскорее. Я буду ждать тебя!"
	return "Я не понимаю тебя... "

def handle_message(update, context):
	response = letsbot_responses(update.message.text)
	update.message.reply_text(response)

msg_handler = MessageHandler(Filters.text, handle_message)
