from telegram.ext import *
from database.Requests import *
from get_meeting_info import get_meeting_info_handler
from database.CreateDB import *
from join import joinhandler
from get_id import get_id_handler
import Commands as cmd
from create_meeting import create_meeting_conv_handler
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
	dp.add_handler(get_meeting_info_handler)
	dp.add_handler(joinhandler)
	dp.add_handler(get_id_handler)
	dp.add_handler(create_meeting_conv_handler)

	dp.add_handler(MessageHandler(Filters.text, handle_message))
	dp.add_error_handler(error)

	print("Бот запущен...")
	updater.start_polling()
	updater.idle()


main()
