from telegram.ext import *
import Commands as cmd
import Responses as resp
import os

def handle_message(update, context):
	response = resp.letsbot_responses(update.message.text)
	update.message.reply_text(response)

def error(update, context):
	print(f"Update {update} caused error {context.error}")

def main():
	apikey = os.getenv("APIKEY")
	if (not apikey):
		print("APIKEY needed")
		exit(1)
	updater = Updater(apikey, use_context=True)
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", cmd.start_command))
	dp.add_handler(CommandHandler("help", cmd.help_command))
	dp.add_handler(MessageHandler(Filters.text, handle_message))
	dp.add_error_handler(error)

	print("Bot started...")
	updater.start_polling()
	updater.idle()

main()
