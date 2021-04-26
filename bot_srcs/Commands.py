def start_command(update, context):
	update.message.reply_text("You are ready to plan a party, I see!")

def help_command(update, context):
	update.message.reply_text("use /create_meeting command to start planing.")
