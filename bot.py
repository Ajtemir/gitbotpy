
from glob import glob
import logging
from random import choice
import settings

from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler



logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )



def greet_user(bot,update, user_data):
    # emo = emojize(choice(settings.USER_EMOJI), use_aliases=True)
    emo = get_user_emo(user_data)
    user_data['emo']=emo
    text = 'Привет {}'.format(emo)
    
    
    # text='Вызван/start'
    # print(text)
    # bot.sendMessage(chat_id=update.message.chat_id, text="Здравствуйте.")

def talk_to_me(bot, update, user_data):
    emo = get_user_emo(user_data)
    user_text = "Hello, {},{}! You wrote:{} .".format(update.message.chat.first_name,user_data['emo'],update.message.text)
    # print(user_text)
    logging.info("User:%s,Chat id: %s, Message: %s", update.message.chat.username,
                update.message.chat.id, update.message.text)

    update.message.reply_text(user_text)

def send_cat_picture(bot,update, user_data):
    cat_list = glob ('images/cat*.jp*g')
    cat_pic = choice(cat_list)
    bot.send_photo(chat_id=update.message.chat.id,photo=open(cat_pic,'rb'),reply_markup=get_keyboard())

def change_avatar(bot,update,user_data):
    if 'emo' in user_data:
        del user_data['emo']
    emo = get_user_emo(user_data)
    update.message.reply_text('готово:{}'.format(emo),reply_markup=get_keyboard())    

def get_contact(bot,update,user_data):
    print(update.message.contact)
    update.message.reply_text('готово:{}'.format(get_user_emo(user_data)),reply_markup=get_keyboar())

def get_location(bot,update,user_data):
    print(update.message.location)
    update.message.reply_text('готово:{}'.format(get_user_emo(user_data)),reply_markup=get_keyboard())

def get_user_emo(user_data):
    if 'emo' in user_data:
        return user_data['emo']
    else:
        user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases=True)
        return user_data['emo']

def get_keyboard():
    contact_button = KeyboardButton('Прислать контакты', request_contact=True)
    location_button = KeyboardButton('Прислать координаты', request_location=True)
    my_keyboard = ReplyKeyboardMarkup([
                                        ['Прислать котика','Сменить аватарку'],
                                        [contact_button, location_button]
                                         ], resize_keyboard=True
                                        )
    return my_keyboard

    update.message.reply_text(text,reply_markup=my_keyboard)




def main():
    mybot = Updater(settings.API_KEY ,request_kwargs=settings.PROXY)
    
    logging.info('bot starting')

    dp=mybot.dispatcher
    dp.add_handler(CommandHandler('start',greet_user, pass_user_data=True))
    dp.add_handler(CommandHandler('cat',send_cat_picture, pass_user_data=True))
    dp.add_handler(RegexHandler('^(Прислать котика)$',send_cat_picture,pass_user_data=True))
    dp.add_handler(RegexHandler('^(Сменить аватарку)$',change_avatar, pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.contact,get_contact,pass_user_data=True))
    dp.add_handler(MessageHandler(Filters.location,get_location,pass_user_data=True))


    dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))
    
    mybot.start_polling()
    mybot.idle()

main()


# 3 telegram 2 emoji




