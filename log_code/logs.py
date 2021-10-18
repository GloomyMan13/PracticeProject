import logging.config
from log_code.log_config import config
import functools


def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger('debug_log')
    logging.config.dictConfig(config)
    return logger


def exception(function):
    """
    Decorator, that adds in logs all Exceptions
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except:
            err = function.__name__ + '\n\n'
            logger.exception(err)

            raise

    return wrapper
