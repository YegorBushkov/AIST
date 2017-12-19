#!/usr/bin/env python3
# @aist2bot - send last photo

# pip3 install pyTelegramBotAPI

import os
import glob
import telebot


token = '4999999:XXXXXXXXXXXXXXXXXXXXXXXXXX'


print('>>> Run AIST2BOT v.1.0 <<<')

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "AIST \n /get - get last image")
	
@bot.message_handler(commands=['get'])
def last_image(message):
    print('>> /get')
    bot.reply_to(message, "AIST last image")
    try:
        list_of_files = glob.glob('img*.png') 
        latest_file = max(list_of_files, key=os.path.getctime)
        print('> find latest image: %s' % latest_file)

        photo = open(latest_file, 'rb')
        bot.send_photo(message.chat.id, photo)
        photo.close()
        print('> image send to telegram')
    except:
        print('> Error')


if __name__ == '__main__':
    bot.polling(none_stop=True)