from telebot import TeleBot

from .config import Config
from .db.manager import DBManager
from .db.models import Cowboy
from .explorer import get_explorer_cls
from .handler import Handler
from .logger import get_logger
from .parser import get_parser
from .processor import Processor, Serializer, Deserializer
from .serve import get_flask_app
from .utils import get_data_folder_path

logger = get_logger(__name__)


def start(config: Config):
    bot = TeleBot(config.TELE_TOKEN)

    Handler(
        bot=bot,
        issuer_id=config.ISSUER_ID,
        processor=Processor(
            parser=get_parser(config.DIR_PATTERN),
            db_man=DBManager[Cowboy](
                path=get_data_folder_path(),
                object_type=Cowboy,
                create_if_missing=True,
            ),
            explorer_cls=get_explorer_cls(config.GITHUB_TOKEN),
        ),
        serializer=Serializer(),
        deserializer=Deserializer(),
    )

    DEF_PORT = "8443"
    URL_BASE = f"https://{config.HOST}"
    URL_PATH = f"/{config.TELE_TOKEN}"

    cert = f"{get_data_folder_path()}/{config.CERT}"

    bot.remove_webhook()

    if config.DEBUG != "0":
        logger.info("Running in a DEBUG mode.")
        bot.polling(none_stop=True)
    else:
        logger.info("Running in a PRODUCTION mode.")
        flask_app = get_flask_app(bot)
        bot.set_webhook(url=URL_BASE + URL_PATH, certificate=open(cert, "rb"))
        flask_app.run(host=config.LISTEN, port=DEF_PORT)
