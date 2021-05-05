from telegram.ext import *
from database.Requests import *
from database.CreateDB import *
import Commands as cmd
import Responses as resp
import os

initialization("database/lets.db")

def handle_message(update, context):
	response = resp.letsbot_responses(update.message.text)
	update.message.reply_text(response)


def error(update, context):
	print(f"Обноваление {update} вызвало ошибку {context.error}")


def main():
	apikey = os.getenv("APIKEY")
	if not apikey:
		print("не обрнаружен APIKEY")
		exit(1)
	updater = Updater(apikey, use_context=True)
	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", cmd.start_command))
	dp.add_handler(CommandHandler("info", cmd.info_command))
	dp.add_handler(CommandHandler("help", cmd.help_command))

	dp.add_handler(MessageHandler(Filters.text, handle_message))
	dp.add_error_handler(error)

	print("Бот запущен...")
	updater.start_polling()
	updater.idle()


main()
