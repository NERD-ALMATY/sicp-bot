import logging

from sicp_bot.utils import get_data_folder_path

formatter = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(
    level=logging.INFO,
    format=formatter,
    filename=f'{get_data_folder_path()}/app.log',
    filemode='w'
)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(logging.Formatter(formatter))
stream_handler.setLevel(logging.INFO)


def get_logger(scope) -> logging.Logger:
    logger = logging.getLogger(scope)
    logger.addHandler(stream_handler)
    return logger
