from os import environ as env_dict
from typing import Callable

from telebot import TeleBot
from telebot.types import Message

from sicp_bot.config import Config
from sicp_bot.db.manager import DBManager
from sicp_bot.db.models import Cowboy
from sicp_bot.explorer import get_explorer_cls
from sicp_bot.logger import get_logger
from sicp_bot.parser import get_parser
from sicp_bot.processor import Processor, Deserializer, Serializer
from sicp_bot.serve import get_flask_app
from sicp_bot.utils import get_data_folder_path, default_message_texts

logger = get_logger(__name__)
DEF_PORT = '8443'
config = Config(**{key: value for (key, value) in env_dict.items() if key in Config.keys()})

parser = get_parser(config.DIR_PATTERN)
db_man: DBManager[Cowboy] = DBManager[Cowboy](path=get_data_folder_path(), object_type=Cowboy, create_if_missing=True)
explorer_cls = get_explorer_cls(config.GITHUB_TOKEN)
processor = Processor(parser=parser, db_man=db_man, explorer_cls=explorer_cls)

bot = TeleBot(config.TELE_TOKEN)

deserializer, serializer = Deserializer(), Serializer()


def authorize(message: Message, func: Callable):
    if message.from_user.id == int(config.ISSUER_ID):
        func()
    else:
        bot.send_message(message.chat.id, f'Unauthorized access!')


@bot.message_handler(commands=['start', 'help'])
def start_help(message: Message) -> None:
    bot.send_message(message.chat.id, default_message_texts['start_text'], parse_mode='Markdown')


@bot.message_handler(commands=['add'])
def pre_add_cowboy(message: Message) -> None:
    authorize(message, lambda:
    bot.register_next_step_handler(bot.send_message(message.chat.id, default_message_texts['add_msg_text']),
                                   add_cowboy))


@bot.message_handler(commands=['del'])
def pre_del_cowboy(message: Message) -> None:
    authorize(message, lambda:
    bot.register_next_step_handler(bot.send_message(message.chat.id, default_message_texts['del_msg_text']),
                                   del_cowboy))


def del_cowboy(message: Message) -> None:
    try:
        cowboy = processor.get_cowboy(message.text)
        if cowboy is None:
            bot.send_message(message.chat.id, f'Cowboy with such username is not found: {message.text}')
        else:
            cowboy_id = processor.delete_cowboy(message.text)
            if cowboy_id is not None:
                bot.send_message(message.chat.id, f'Deleted a cowboy: {cowboy.username}\n with model_id: {cowboy_id}')
            else:
                bot.send_message(message.chat.id, f'Cowboy with such username is not found: {message.text}')
    except Exception as e:
        logger.exception('Couldn\'t delete a cowboy.', exc_info=e)
        bot.send_message(message.chat.id, f'Couldn\'t delete a cowboy.')


def add_cowboy(message: Message) -> None:
    try:
        cowboy_id = processor.create_cowboy(deserializer.to_cowboy(message.text))
        bot.send_message(message.chat.id, f'Created a new cowboy with id: {cowboy_id}')
    except Exception as e:
        logger.exception('Couldn\'t add a cowboy.', exc_info=e)
        bot.send_message(message.chat.id, f'Couldn\'t add a new cowboy.')


@bot.message_handler(regexp='\/get [A-z0-9]*')
def get_cowboy(message: Message):
    username: str = message.text[5:].strip()
    cowboy = processor.get_cowboy(username)
    if isinstance(cowboy, Cowboy):
        ans = serializer.from_cowboy_extended(cowboy)
        bot.send_message(message.chat.id, ans, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f'Cowboy is not found: {username}', parse_mode='Markdown')


@bot.message_handler(regexp='\/leaderboard ([1-9][0-9]+|[1-9])')
@bot.message_handler(regexp='\/leaderboard')
def get_leaderboard(message: Message):
    length: int = 10 if len(message.text) <= 13 else int(message.text[13:].strip())
    bot.send_message(message.chat.id, serializer.leaderboard(processor.get_leaderboard()[:length]),
                     parse_mode='Markdown')


@bot.message_handler(func=lambda message: True)
def repeat_all_messages(message):
    bot.send_message(message.chat.id, 'I don\'t know how to react!')


bot.remove_webhook()

URL_BASE = f'https://{config.HOST}:{DEF_PORT}'
URL_PATH = f'/{config.TELE_TOKEN}/'

cert = f'{get_data_folder_path()}/{config.CERT}'
key = f'{get_data_folder_path()}/{config.KEY}'

if config.DEBUG != '0':
    bot.polling(none_stop=True)
else:
    flask_app = get_flask_app(bot)
    bot.set_webhook(url=URL_BASE + URL_PATH, certificate=open(cert, 'r'))
    flask_app.run(
        host=config.LISTEN,
        port=DEF_PORT,
        ssl_context=(cert, key)
    )