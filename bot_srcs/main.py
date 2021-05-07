# third party external libraries
from telegram.ext import Updater
from os import getenv

# database module
from database.CreateDB import initialization

# handlers
from handlers.start_help_info import start_handler, help_handler, info_handler

from handlers.create_meeting import create_meeting_handler
from handlers.get_id import get_id_handler
from handlers.join import join_handler
from handlers.get_meeting_info import get_meeting_info_handler
from handlers.add_question import add_question_handler
from handlers.poll import poll_handler, poll_answer_handler

from handlers.msg_responses import msg_handler
from handlers.error import error_handler

initialization("database/lets.db")


def main():
	apikey = getenv("APIKEY")
	if not apikey:
		print("не обрнаружен APIKEY")
		exit(1)
	updater = Updater(apikey, use_context=True)
	dp = updater.dispatcher

	# order is important!
	dp.add_handler(start_handler)
	dp.add_handler(help_handler)
	dp.add_handler(info_handler)
	dp.add_handler(get_id_handler)

	dp.add_handler(join_handler)
	dp.add_handler(get_meeting_info_handler)
	dp.add_handler(add_question_handler)
	dp.add_handler(create_meeting_handler)

	dp.add_handler(poll_handler)
	dp.add_handler(poll_answer_handler)

	dp.add_handler(msg_handler)
	dp.add_error_handler(error_handler)

	print("Бот запущен...")
	updater.start_polling()
	updater.idle()


main()
