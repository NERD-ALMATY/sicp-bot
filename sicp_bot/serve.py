from typing import Optional

from telebot import TeleBot
from flask import Flask, request
from flask_restful import Resource, Api, abort

from sicp_bot.logger import get_logger

logger = get_logger(__name__)

_app = Flask(__name__)
_api = Api(_app)

_bot: Optional[TeleBot] = None


def _set_bot(bot: TeleBot):
    global _bot
    _bot = bot


class _Main(Resource):

    def post(self):
        json_string = request.get_json()
        if json_string:
            _bot.process_new_updates([json_string])
            return ''
        else:
            abort(403, error_message='Knock knock, open up the door, it\'s query! (C) DMX')


def get_flask_app(bot: TeleBot):
    assert isinstance(bot, TeleBot)
    _set_bot(bot)
    _api.add_resource(_Main, f'/{bot.token}')
    return _app
