from telegram.ext import CommandHandler

def start_command(update, context):
	update.message.reply_text("Привет! Чтобы узнать, зачем нужен этот бот, \
	воспользуйся командой /info. Чтобы узнать, как его использовать, \
	обратись за помощью /help.")


def info_command(update, context):
	update.message.reply_text("Telegram бот, который позволит \
		организовать дружескую встречу. Через серию вопросов бот будет \
		собирать предпочитаемые варианты времяпрепровождения у группы людей, \
		далее на основе результатов опросов составлять план мероприятия.")


def help_command(update, context):
	msg = ("Используй команду /create_meeting, чтобы начать планирование \
		мероприятия.\n\nДля того, чтобы добавить новый опрос, вызови команду \
		/add_question.\nА чтобы на него (них) ответить используй /answer_questions\
		\n\nКоманда /get_id выведит список мероприятий: их названий\
		 и идентификаторов.\n\nЧтобы присоединиться к мероприятию, воспользуйся \
		командой /join.\n\n/get_meeting_info отправит тебе сообщение \
		со всей информацией о запланированной встрече.")
	update.message.reply_text(msg)


start_handler =  CommandHandler('start', start_command)
help_handler =  CommandHandler('help', help_command)
info_handler =  CommandHandler('info', info_command)
