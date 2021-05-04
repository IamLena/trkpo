def start_command(update, context):
        update.message.reply_text("Я вижу, вы готовы устроить вечеринку!")

def help_command(update, context):
        update.message.reply_text("Используйте команду /create_meeting, чтобы начать планирование.")
