def letsbot_responses(input_text):
	user_message = str(input_text).lower()

	if user_message in ("привет", "здравствуй", "хай"):
		return "Привет! Рад тебя видеть :)"

	if user_message in ("пока", "до свидания"):
		return "Возвращайся поскорее. Я буду ждать тебя!"
	
	return "Я не понимаю тебя... "
