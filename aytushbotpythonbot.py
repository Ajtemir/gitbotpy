from telegram.ext import Updater, CommandHandler
from telegram import message
def greet_user(bot,update):
    text='вызван/start'
    print(text)
    update.message.reply_text(text)

def main():
    mybot = Updater("1379590346:AAF5LcWC9IL9wYrSbPSRzUYuyCu7s4U5h3Q")
    
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))

    mybot.start_polling()
    mybot.idle()

main()