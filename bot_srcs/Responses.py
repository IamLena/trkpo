def letsbot_responses(input_text):
	user_message = str(input_text).lower()

	if user_message in ("hello", "hi", "hey"):
		return "Hello there! Nice to meet you :)"

	if user_message in ("bye", "goodbye"):
		return "Come back soon. I'll wait for you!"

	return "I don't understand you... "
