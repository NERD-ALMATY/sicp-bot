from typing import Callable, List

import telebot
from telebot.types import Message

from .db.models import Cowboy
from .logger import get_logger
from .processor import Processor, Serializer, Deserializer
from .utils import default_message_texts

logger = get_logger(__name__)


class Handler:
    def __init__(
        self,
        bot: telebot.TeleBot,
        issuer_id: str,
        processor: Processor,
        serializer: Serializer,
        deserializer: Deserializer,
    ):
        self._bot = bot
        self._issuer_id = issuer_id
        self._processor = processor
        self._deserializer = deserializer
        self._serializer = serializer
        self._functions: List[Callable] = []

        @self._bot.message_handler(commands=["start", "help"])
        def start_help(message: Message) -> None:
            self._bot.send_message(
                message.chat.id,
                default_message_texts["start_text"],
                parse_mode="Markdown",
            )

        @self._bot.message_handler(commands=["add"])
        def pre_add_cowboy(message: Message) -> None:
            if self.authorized(message):
                self._bot.register_next_step_handler(
                    self._bot.send_message(
                        message.chat.id, default_message_texts["add_msg_text"]
                    ),
                    self.add_cowboy,
                )

        @self._bot.message_handler(commands=["del"])
        def pre_del_cowboy(message: Message) -> None:
            if self.authorized(message):
                self._bot.register_next_step_handler(
                    self._bot.send_message(
                        message.chat.id, default_message_texts["del_msg_text"]
                    ),
                    self.del_cowboy,
                )

        @self._bot.message_handler(regexp="/get [A-z0-9]*")
        def get_cowboy(message: Message):
            username: str = message.text[5:].strip()
            cowboy = self._processor.get_cowboy(username)
            if isinstance(cowboy, Cowboy):
                ans = self._serializer.from_cowboy_extended(cowboy)
                self._bot.send_message(
                    message.chat.id, ans, parse_mode="Markdown"
                )
            else:
                self._bot.send_message(
                    message.chat.id,
                    f"Cowboy is not found: {username}",
                    parse_mode="Markdown",
                )

        @self._bot.message_handler(regexp="/leaderboard ([1-9][0-9]+|[1-9])")
        @self._bot.message_handler(regexp="/leaderboard")
        def get_leaderboard(message: Message):
            length: int = 10 if len(message.text) <= 13 else int(
                message.text[13:].strip()
            )
            self._bot.send_message(
                message.chat.id,
                self._serializer.leaderboard(
                    self._processor.get_leaderboard()[:length]
                ),
                parse_mode="Markdown",
            )

        @self._bot.message_handler(func=lambda message: True)
        def repeat_all_messages(message):
            self._bot.send_message(
                message.chat.id, "I don't know how to react!"
            )

        self._functions.extend(
            [
                start_help,
                pre_add_cowboy,
                pre_del_cowboy,
                get_leaderboard,
                get_cowboy,
            ]
        )

    def authorized(self, message: Message) -> bool:
        if message.from_user.id != int(self._issuer_id):
            self._bot.send_message(message.chat.id, f"Unauthorized access!")
            return False
        return True

    def del_cowboy(self, message: Message) -> None:
        if self.authorized(message):
            try:
                cowboy = self._processor.get_cowboy(message.text)
                if cowboy is None:
                    self._bot.send_message(
                        message.chat.id,
                        f"Cowboy with such username is not found: {message.text}",
                    )
                else:
                    cowboy_id = self._processor.delete_cowboy(message.text)
                    if cowboy_id is not None:
                        self._bot.send_message(
                            message.chat.id,
                            f"Deleted a cowboy: {cowboy.username}\n with model_id: {cowboy_id}",
                        )
                    else:
                        self._bot.send_message(
                            message.chat.id,
                            f"Cowboy with such username is not found: {message.text}",
                        )
            except Exception as e:
                logger.exception("Couldn't delete a cowboy.", exc_info=e)
                self._bot.send_message(
                    message.chat.id, f"Couldn't delete a cowboy."
                )

    def add_cowboy(self, message: Message) -> None:
        if self.authorized(message):
            try:
                cowboy_id = self._processor.create_cowboy(
                    self._deserializer.to_cowboy(message.text)
                )
                self._bot.send_message(
                    message.chat.id,
                    f"Created a new cowboy with id: {cowboy_id}",
                )
            except Exception as e:
                logger.exception("Couldn't add a cowboy.", exc_info=e)
                self._bot.send_message(
                    message.chat.id, f"Couldn't add a new cowboy."
                )
