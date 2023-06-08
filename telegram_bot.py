
import os
import telebot

from dotenv import load_dotenv


load_dotenv()
bot_token = os.environ['TG_BOT_TOKEN']
bot = telebot.TeleBot(bot_token)




def send_message(message_text):
    bot.send_message(1365913221, message_text)


def main():
    send_message('Hi Michael!')



if __name__ == '__main__':
    main()
