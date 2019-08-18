import logging

from sicp_bot.utils import get_data_folder_path

stream_handler = logging.StreamHandler()
file_handler = logging.FileHandler(f'{get_data_folder_path()}/app.log')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler.setLevel(logging.WARNING)
file_handler.setLevel(logging.ERROR)
stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

def get_logger(scope):
    logger = logging.getLogger(scope)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
