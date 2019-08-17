from os import environ as env_dict
from typing import Callable

from telebot import TeleBot
from telebot.types import Message

from sicp_bot.config import Config
from sicp_bot.db.manager import DBManager
from sicp_bot.db.models import Cowboy
from sicp_bot.explorer import get_explorer_cls
from sicp_bot.parser import get_parser
from sicp_bot.processor import Processor, Deserializer, Serializer
from sicp_bot.utils import get_data_folder_path

start_text = """ Hey, cowboy! Happy to see ya!
This is bot was created to involve people solve SICP exercises with fun. 
Here are the commands you can run:
/start - show this message.
/help - show this message.
/get {username} - get user profile.
/leaderboard [size] - get leaderboard with size.

If you are an admin:
/add - add new user(follow the messages).
/del - del existing user(follow the messages).

Hope you're going to enjoy using it!
maintainer: @arpanetus
repository: [github.com/nerd-iitu/sicp-bot](https://github.com/nerd-iitu/sicp-bot)
"""

add_msg_text = """Here's the syntax to add:
username: arpanetus
name: arpanetus
repo: sicp-ans
"""

del_msg_text = """Simply place the username:
arpanetus
"""

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
        bot.reply_to(message, f'Unauthorized access!')


@bot.message_handler(commands=['start','help'])
def start_help(message: Message) -> None:
    bot.send_message(message.chat.id, start_text, parse_mode="Markdown")

@bot.message_handler(commands=['add'])
def pre_add_cowboy(message: Message) -> None:
    authorize(message, lambda:
    bot.register_next_step_handler(bot.reply_to(message, add_msg_text), add_cowboy))


@bot.message_handler(commands=['del'])
def pre_del_cowboy(message: Message) -> None:
    authorize(message, lambda:
    bot.register_next_step_handler(bot.reply_to(message, del_msg_text), del_cowboy))


def del_cowboy(message: Message) -> None:
    try:
        cowboy = processor.get_cowboy(message.text)
        if cowboy is None:
            bot.reply_to(message, f'Cowboy with such username is not found: {message.text}')
        else:
            cowboy_id = processor.delete_cowboy(message.text)
            if cowboy_id is not None:
                bot.reply_to(message, f'Deleted a cowboy: {cowboy.username}\n'
                f'with model_id: {cowboy_id}')
            else:
                bot.reply_to(message, f'Cowboy with such username is not found: {message.text}')
    except Exception:
        bot.reply_to(message, f'Couldn\'t delete a cowboy.')


def add_cowboy(message: Message) -> None:
    try:
        cowboy_id = processor.create_cowboy(deserializer.to_cowboy(message.text))
        bot.reply_to(message, f'Created a new cowboy with id: {cowboy_id}')
    except Exception:
        bot.reply_to(message, f'Couldn\'t add a new cowboy.')


@bot.message_handler(regexp='\/get [A-z0-9]*')
def get_cowboy(message: Message):
    username: str = message.text[5:].strip()
    cowboy = processor.get_cowboy(username)
    if isinstance(cowboy, Cowboy):
        ans = serializer.from_cowboy_extended(cowboy)
        bot.reply_to(message, ans, parse_mode="Markdown")
    else:
        bot.reply_to(message, f"Cowboy is not found: {username}", parse_mode="Markdown")


@bot.message_handler(regexp='\/leaderboard ([1-9][0-9]+|[1-9])')
@bot.message_handler(regexp='\/leaderboard')
def get_leaderboard(message: Message):
    length: int = 10 if len(message.text) <= 13 else int(message.text[13:].strip())
    bot.reply_to(message, serializer.leaderboard(processor.get_leaderboard()[:length]), parse_mode="Markdown")


bot.polling(none_stop=True)
