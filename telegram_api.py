
import os
import telebot

from dotenv import load_dotenv


load_dotenv()
bot_token = os.environ['TG_BOT_TOKEN']
bot = telebot.TeleBot(bot_token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Hi Michael! chat id: {message.chat.id}')

bot.polling()