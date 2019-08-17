from typing import Optional

from telebot import TeleBot
from flask import Flask, request
from flask_restful import Resource, Api

_app = Flask(__name__)
_api = Api(_app)

_bot: Optional[TeleBot] = None


def _set_bot(bot: TeleBot):
    global _bot
    _bot = bot


class _Main(Resource):
    content_length = None
    content_type = None

    def get(self):
        json_string = request.get_json()
        if json_string:
            _bot.process_new_updates([json_string])
        return '' if json_string is None else json_string


def get_app(bot: TeleBot):
    assert isinstance(bot, TeleBot)
    _set_bot(bot)
    _api.add_resource(_Main, f'/{bot.token}')
    return _app
