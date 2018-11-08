import logging
import subprocess

from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=text["start"])
    open(report_dir.format(update.message.chat_id), "w")


def report(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=open(report_dir.format(update.message.chat_id), "r"))


def adjust(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=text["adjust"])


def fortune(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text=subprocess.run(['fortune'], stdout=subprocess.PIPE).stdout.decode('utf-8'))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logging.warning('Update "%s" caused error "%s"', update, error)


def reminder(bot,job):
    bot.send_message(chat_id=update.message.chat_id,text=text["done"])
    bot.send_message(chat_id=update.message.chat_id,text=text["todo"])
    bot.send_message(chat_id=update.message.chat_id,text=text["obstacles"])


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, I didn't understand that command.")


def setTime(bot, update):
    print(update.message.text)


report_dir = "./reports/{}.txt"

text = load(open("text.yml", "r"), Loader=Loader)

SETUP, READY = range(2)

updater = Updater(token='741012984:AAF_qrjF9LiclB-owhFP6Yi7NZ7T-lPhHR0')

dispatcher = updater.dispatcher

job_queue = updater.job_queue

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

start_handler = CommandHandler('start', start)
report_handler = CommandHandler('report', report)
fortune_handler = CommandHandler('fortune', fortune)
adjust_handler = CommandHandler('adjust', adjust)
unknown_handler = MessageHandler(Filters.command, unknown)
unknown_handler = MessageHandler(Filters.text, setTime)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(report_handler)
dispatcher.add_handler(fortune_handler)
dispatcher.add_handler(adjust_handler)
dispatcher.add_handler(unknown_handler)

dispatcher.add_error_handler(error)

updater.start_polling()

updater.idle()